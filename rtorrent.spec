#
# Conditional build:
%bcond_with	colors		# with color version
%bcond_with	ipv6		# with IPv6 support (default IPv4-only)
#
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.7.1
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	98b97730c36828e662a2355cb2b11309
Patch100:	%{name}-colors.patch
Patch101:	%{name}-dns_peer_info.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtorrent-devel >= 0.11.1
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rTorrent is a console-based BitTorrent client. It aims to be a
fully-featured and efficient client with the ability to run in the
background using screen. It supports fast-resume and session
management.

%description -l pl
rTorrent to konsolowy klient BitTorrenta. Jego celem jest by� pe�nym i
wydajnym klientem, z mo�liwo�ci� uruchamiania go w tle przy u�yciu
screena. Obs�uguje szybkie wznawianie i zarz�dzanie sesjami.

%prep
%setup -q
%if %{with colors}
%patch100 -p1
#%patch101 -p1
%endif

%build
cp /usr/share/automake/config.sub .
%configure \
	CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--%{?with_ipv6:en}%{!?with_ipv6:dis}able-ipv6

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
