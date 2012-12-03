%define		pre	~rc2
%define		rev	594

Summary:	LASH Audio Session Handler
Name:		lash
Version:	0.6.0
Release:	0.%{pre}.1
License:	GPL v2+
Group:		Applications/Sound
Source0:	http://download.savannah.gnu.org/releases/lash/%{name}-%{version}%{pre}.tar.bz2
# Source0-md5:	af1dc4f4ceb284b1b0845de4f4c2fe47
URL:		http://lash.nongnu.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gtk+-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LASH Audio Session Handler consists of a daemon, a client library and
a some clients that implement a session management system for audio
applications on Linux.

%package libs
Summary:	LASH Audio Session Handler library
Group:		Libraries

%description libs
LASH Audio Session Handler library.

%package devel
Summary:	Header files for LASH library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libuuid-devel

%description devel
Header files for LASH library.

%package -n python-lash
Summary:	Python bindings for LASH library
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-lash
Python bindings for LASH library.

%prep
%setup -qn %{name}-%{version}.%{rev}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
%{__make} \
	pkgpyexecdir="\$(pyexecdir)"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgpyexecdir="\$(pyexecdir)"

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_lash.la

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.SECURITY TODO
%attr(755,root,root) %{_bindir}/lash_control
%attr(755,root,root) %{_bindir}/lash_panel
%attr(755,root,root) %{_bindir}/lash_save_button
%attr(755,root,root) %{_bindir}/lash_shell
%attr(755,root,root) %{_bindir}/lash_simple_client
%attr(755,root,root) %{_bindir}/lash_simple_client_newapi
%attr(755,root,root) %{_bindir}/lash_synth
%attr(755,root,root) %{_bindir}/lashd
%{_datadir}/dbus-1/services/org.nongnu.lash.service
%{_datadir}/lash

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/liblash.so.1
%attr(755,root,root) %{_libdir}/liblash.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblash.so
%{_libdir}/liblash.la
%{_includedir}/lash-1.0
%{_pkgconfigdir}/lash-1.0.pc

%files -n python-lash
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_lash.so
%{py_sitedir}/lash.py[co]

