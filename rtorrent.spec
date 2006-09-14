#
# Conditional build:
%bcond_with	colors		# with color version
#
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.6.2
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	b199ca24ba4a5c0f59b587cd4fa11670
Patch0:		%{name}-inttypes.patch
Patch1:		%{name}-client_info.patch
Patch100:	%{name}-colors.patch
Patch101:	%{name}-dns_peer_info.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtorrent-devel >= 0.10.2
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
rTorrent to konsolowy klient BitTorrenta. Jego celem jest byæ pe³nym i
wydajnym klientem, z mo¿liwo¶ci± uruchamiania go w tle przy u¿yciu
screena. Obs³uguje szybkie wznawianie i zarz±dzanie sesjami.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%if %{with colors}
%patch100 -p1
#%patch101 -p1
%endif

%build
cp /usr/share/automake/config.sub .
%configure \
	CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
	--%{?debug:en}%{!?debug:dis}able-debug
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
