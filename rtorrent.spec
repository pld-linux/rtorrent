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
# keep stable line, see URL below
Version:	0.9.6
Release:	1
Epoch:		5
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://rtorrent.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	5e7550f74e382a6245412c615f45444d
Source1:	rtorrent-tmux@.service
Patch0:		%{name}-colors.patch
Patch1:		%{name}-ssl-no-verify.patch
Patch2:		%{name}-ip_filter.patch
Patch3:		%{name}-build.patch
URL:		https://github.com/rakshasa/rtorrent/wiki
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	cppunit-devel >= 1.9.6
BuildRequires:	curl-devel >= 7.15.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libtorrent-devel = 1:0.13.6
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
%if %{with xmlrpc}
BuildRequires:	xmlrpc-c-server-devel >= 1.14.2
%endif
BuildRequires:	zlib-devel
Requires:	curl-libs >= 7.15.4
Requires:	libtorrent = 1:0.13.6
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
%if %{with colors}
%patch0 -p1
%endif
%patch1 -p1
# broke, see TODO
#%patch2 -p1
%patch3 -p1

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
install -d $RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README doc/rtorrent.rc
%attr(755,root,root) %{_bindir}/rtorrent
%{systemdunitdir}/rtorrent-tmux@.service
