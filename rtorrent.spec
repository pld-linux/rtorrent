# TODO:
# - ip_filter patch is broken (doesn't handle ipv6 addresses. Also causes
#   "rtorrent: CommandMap::insert(...) tried to insert an already existing key." error)
#
# Conditional build:
%bcond_without	xmlrpc		# build xmlrpc-c support
%bcond_without	colors		# without color version
%bcond_without	ipv6		# without IPv6 support
#
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl.UTF-8):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.8.7
Release:	1
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	d78f00dcf741c01254de72c0d3836761
Patch0:		%{name}-colors.patch
Patch1:		%{name}-ssl-no-verify.patch
Patch2:		%{name}-ip_filter.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libtorrent-devel >= 0.12.6
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
# broke, see TODO
#%patch2 -p1

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
