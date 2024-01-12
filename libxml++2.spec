#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	apidocs		# apidocs
#
Summary:	C++ interface for working with XML files
Summary(pl.UTF-8):	Interfejs C++ do pracy z plikami XML
Name:		libxml++2
Version:	2.42.3
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://download.gnome.org/sources/libxml++/2.42/libxml++-%{version}.tar.xz
# Source0-md5:	054ba226bf5f9c8876d280688de3b2f1
URL:		http://libxmlplusplus.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
%{?with_apidocs:BuildRequires:	docbook-dtd50-xml}
%{?with_apidocs:BuildRequires:	docbook-style-xsl-nons}
%{?with_apidocs:BuildRequires:	doxygen >= 1:1.8.9}
BuildRequires:	glibmm-devel >= 2.32.0
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.7.7
%{?with_apidocs:BuildRequires:	libxslt-progs}
BuildRequires:	mm-common >= 0.9.10
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glibmm >= 2.32.0
Requires:	libxml2 >= 1:2.7.7
Obsoletes:	libxml++ < 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libxml++ is a C++ interface for the libxml XML parser library.

%description -l pl.UTF-8
libxml++ jest interfejsem C++ do biblioteki libxml.

%package devel
Summary:	Header files for libxml++
Summary(pl.UTF-8):	Pliki nagłówkowe do libxml++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glibmm-devel >= 2.32.0
Requires:	libstdc++-devel >= 6:4.6
Requires:	libxml2-devel >= 1:2.7.7
Obsoletes:	libxml++-devel < 3.0

%description devel
Header files for libxml++.

%description devel -l pl.UTF-8
Pliki nagłówkowe do libxml++.

%package static
Summary:	Static libxml++ libraries
Summary(pl.UTF-8):	Biblioteka statyczna libxml++
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	libxml++-static-devel < 3.0

%description static
Static libxml++ libraries.

%description static -l pl.UTF-8
Biblioteka statyczna libxml++.

%package apidocs
Summary:	libxml++ API documentation
Summary(pl.UTF-8):	Dokumentacja API libxml++
Group:		Documentation
Obsoletes:	libxml++-apidocs < 3.0
BuildArch:	noarch

%description apidocs
libxml++ API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libxml++.

%package examples
Summary:	libxml++ - example programs
Summary(pl.UTF-8):	libxml++ - przykładowe programy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	libxml++-examples < 3.0
BuildArch:	noarch

%description examples
libxml++ - example programs.

%description examples -l pl.UTF-8
libxml++ - przykładowe programy.

%prep
%setup -q -n libxml++-%{version}

%build
mm-common-prepare --copy --force
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_apidocs:--disable-documentation} \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libxml++-2.6.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libxml++-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxml++-2.6.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxml++-2.6.so
%{_libdir}/libxml++-2.6
%{_includedir}/libxml++-2.6
%{_pkgconfigdir}/libxml++-2.6.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxml++-2.6.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_datadir}/devhelp/books/libxml++-2.6
%{_docdir}/libxml++-2.6
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
