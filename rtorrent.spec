Summary:	rTorrent - a console-based BitTorrent client
Name:		rtorrent
Version:	0.2.5
Release:	0.1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	f92d692abae64b617b57a7a711ea5208
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	curl-devel >= 7.12
BuildRequires:	libstdc++-devel
BuildRequires:	libtorrent-devel >= 0.6.5
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rTorrent is a console-based BitTorrent client. It aims to be a
fully-featured and efficient client with the ability to run in the
background using screen. It supports fast-resume and session
management.

%prep
%setup -q

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
