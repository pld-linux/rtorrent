#
# Conditional build:
%bcond_with	colors		# with color version
#
%define		_libver		0.6.7
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.2.7
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	e315ede1ccba95b94b9f5652c423f464
Patch0:		%{name}-colors.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtorrent-devel >= %{_libver}
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
Requires:	libtorrent >= %{_libver}
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
%if %{with colors}
%patch0 -p1
%endif

%build
%configure \
	CXXFLAGS="%{rpmcflags} -I%{_includedir}/ncurses" \
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
