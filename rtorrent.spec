#
# Conditional build:
%bcond_with	xmlrpc		# build xmlrpc-c support (unstable!)
%bcond_without	colors		# without color support
%bcond_without	ipv6		# without IPv6 support
#
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl.UTF-8):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.8.2
Release:	1
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	a2456182e1767e5aed7341dbbd058f60
Patch0:		%{name}-gcc43.patch
Patch1:		%{name}-fix_start_stop_filter.patch
Patch100:	%{name}-colors.patch
Patch101:	%{name}-ssl-no-verify.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtorrent-devel >= 0.12.0
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
%if %{with xmlrpc}
BuildRequires:	xmlrpc-c-devel
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
%patch0 -p1
%patch1 -p1
%if %{with colors}
%patch100 -p1
%endif
%patch101 -p1

%build
cp /usr/share/automake/config.sub .
%configure \
	CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--%{?with_ipv6:en}%{!?with_ipv6:dis}able-ipv6 \
	--%{?with_xmlrpc:en}%{!?with_xmlrpc:dis}able-xmlrpc-c

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
