#
# Conditional build:
%bcond_without	xmlrpc		# xmlrpc-c support
%bcond_without	lua		# Lua scripting support
%bcond_without	tests		# unit tests
#
Summary:	rTorrent - a console-based BitTorrent client
Summary(pl.UTF-8):	rTorrent - konsolowy klient BitTorrenta
Name:		rtorrent
Version:	0.16.21
Release:	1
Epoch:		5
License:	GPL v2+
Group:		Applications/Networking
#Source0Download: https://github.com/rakshasa/rtorrent/releases
Source0:	https://github.com/rakshasa/rtorrent/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4e9099f695978407794c705b74c6c00e
Source1:	rtorrent-tmux@.service
URL:		https://github.com/rakshasa/rtorrent/wiki
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%if %{with tests}
BuildRequires:	cppunit-devel >= 1.9.6
%endif
BuildRequires:	curl-devel >= 7.15.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libtorrent-devel = 1:0.16.21
%if %{with lua}
BuildRequires:	lua54
BuildRequires:	lua54-devel
%endif
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
%if %{with xmlrpc}
BuildRequires:	xmlrpc-c-server-devel >= 1.14.2
%endif
BuildRequires:	zlib-devel
Requires:	curl-libs >= 7.15.4
%requires_eq_to libtorrent libtorrent-devel
Suggests:	tmux
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

%build
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
	--enable-debug%{!?debug:=no} \
	--with-lua%{!?with_lua:=no} \
	--with-xmlrpc-c%{!?with_xmlrpc:=no}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md doc/rtorrent.rc
%attr(755,root,root) %{_bindir}/rtorrent
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lua
%{_datadir}/%{name}/lua/rtorrent.lua
%{systemdunitdir}/rtorrent-tmux@.service
