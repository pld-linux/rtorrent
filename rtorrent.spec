#
# Conditional build:
%bcond_with	xmlrpc		# build xmlrpc-c support
%bcond_without	colors		# without color version
%bcond_without	ipv6		# without IPv6 support
#
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl.UTF-8):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.8.2
Release:	4
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	a2456182e1767e5aed7341dbbd058f60
Patch0:		%{name}-colors.patch
Patch1:		%{name}-ssl-no-verify.patch
Patch2:		%{name}-gcc43.patch
Patch3:		%{name}-fix_start_stop_filter.patch
Patch4:		%{name}-fix_conn_type_seed.patch
Patch5:		%{name}-fix_load_cache.patch
Patch6:		%{name}-ip_filter.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtorrent-devel >= 0.12.2
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
%if %{with xmlrpc}
BuildRequires:	xmlrpc-c-devel >= 1.14.2
%endif
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rTorrent is a console-based BitTorrent client. It aims to be a
fully-featured and efficient client with the ability to run in the
background using screen. It supports fast-resume and session
management.

%description -l pl.UTF-8
rTorrent to konsolowy klient BitTorrenta. Jego celem jest być pełnym i
wydajnym klientem, z możliwością uruchamiania go w tle przy użyciu
screena. Obsługuje szybkie wznawianie i zarządzanie sesjami.

%prep
%setup -q
%if %{with colors}
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--%{?with_ipv6:en}%{!?with_ipv6:dis}able-ipv6 \
	--with%{!?with_xmlrpc:out}-xmlrpc-c

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO doc/rtorrent.rc
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/rtorrent.1*
