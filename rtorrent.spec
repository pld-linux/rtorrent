#
# Conditional build:
%bcond_with	colors		# with color version
#
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.2.6
Release:	2
License:	GPL v2
Group:		Applications/Networking
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	819b99453abc33a7a934dcacae3a73d5
Patch0:		%{name}-colors.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtorrent-devel >= 0.6.6
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
Requires:	libtorrent >= 0.6.6
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
%patch0 -p1
%endif

%build
%configure \
	CXXFLAGS="%{rpmcxxflags} -I%{_includedir}/ncurses" \
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
