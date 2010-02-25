%define realname snack
Summary:	Sound toolkit
Name:		tcl-%{realname}
Version:	2.2.10
Release:	0.1
License:	GPL v2+
Group:		Libraries
URL:		http://www.speech.kth.se/snack/
Source0:	http://www.speech.kth.se/snack/dist/snack%{version}.tar.gz
# Source0-md5:	98da0dc73599b3a039cba1b7ff169399
Patch1:		snack-extracflags.patch
Patch2:		snack-shared-stubs.patch
Patch3:		snack-newALSA.patch
BuildRequires:	alsa-lib-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	python-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	xorg-lib-libXft-devel
Requires:	tcl(abi) = %{tcl_version}
Provides:	%{realname} = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Snack Sound Toolkit is designed to be used with a scripting
language such as Tcl/Tk or Python. Using Snack you can create powerful
multi-platform audio applications with just a few lines of code. Snack
has commands for basic sound handling, such as playback, recording,
file and socket I/O. Snack also provides primitives for sound
visualization, e.g. waveforms and spectrograms. It was developed
mainly to handle digital recordings of speech, but is just as useful
for general audio. Snack has also successfully been applied to other
one-dimensional signals. The combination of Snack and a scripting
language makes it possible to create sound tools and applications with
a minimum of effort. This is due to the rapid development nature of
scripting languages. As a bonus you get an application that is
cross-platform from start. It is also easy to integrate Snack based
applications with existing sound analysis software.

%package devel
Summary:	Development files for Snack Sound Toolkit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development files for the Snack Sound Toolkit.

%package -n python-%{realname}
Summary:	Python bindings for Snack Sound Toolkit
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-%{realname}
This package contains python bindings for the Snack Sound Toolkit.
Tcl, Tk, and Tkinter are also required to use Snack.

%prep
%setup -q -n %{realname}%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
chmod -x generic/*.c generic/*.h unix/*.c COPYING README demos/python/*
iconv -f iso-8859-1 -t utf-8 -o README{.utf8,}
mv README{.utf8,}
sed -i -e 's|\r||g' demos/python/*.txt

%build
cd unix/
%configure \
	--disable-static \
	--with-tcl=%{_libdir} \
	--with-tk=%{_libdir} \
	--with-ogg-include=%{_includedir} \
	--with-ogg-lib=%{_libdir} \
	--enable-alsa \

%{__make} EXTRACFLAGS="%{optflags}"
cd ../python
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd unix
%{__make} install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
cd -

cd python
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_libdir}/%{realname}2.2 $RPM_BUILD_ROOT%{tcl_sitearch}/%{realname}2.2
chmod -x $RPM_BUILD_ROOT%{tcl_sitearch}/%{realname}2.2/snack.tcl
cd -

# Devel bits
install -d $RPM_BUILD_ROOT%{_includedir}
install -p generic/*.h $RPM_BUILD_ROOT%{_includedir}
install -p unix/snackConfig.sh $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%{_libdir}/libsnackstub2.2.so
%{tcl_sitearch}/%{realname}2.2/

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/snackConfig.sh

%files -n python-%{realname}
%defattr(644,root,root,755)
%doc doc/python-man.html demos/python/
%{py_sitedir}/tkSnack*
