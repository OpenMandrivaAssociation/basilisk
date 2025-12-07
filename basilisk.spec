# set to nil when packaging a release, 
# or the long commit tag for the specific git branch
%define commit_tag %{nil}

# when using a commit_tag (i.e. not nil) add a commit date
# decoration ~0.yyyyMMdd to Version number
%define commit_date %{nil}

%define moz_ver 52.9.0

# style the commit date when using a tag instead of a release
%define basilisk_ver 2025.10.10

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%ifarch %{x86_64}
%define build_arch x86_64
%endif

%ifarch %{aarch64}
%define build_arch aarch64
%endif

Name:           basilisk
Release:        1
Summary:        An independent browser derived from Firefox/Mozilla community code.
Group:          Internet
License:        MPL-2.0
URL:            https://basilisk-browser.org

# change the source URL depending on if the package is a release version or a git version
%if "%{commit_tag}" != "%{nil}"
Version:        %{basilisk_ver}
Source0:        https://repo.palemoon.org/Basilisk-Dev/Basilisk/archive/%{commit_tag}.tar.gz#/%{name}-%{?commit_date}.tar.gz
%else
Version:        %{basilisk_ver}
Source0:        https://repo.palemoon.org/Basilisk-Dev/Basilisk/archive/v%version.tar.gz#/%name-%version.tar.gz
%endif

# Required for building the browser (latest release)
Source1:        https://repo.palemoon.org/MoonchildProductions/UXP/archive/RB_20251019.tar.gz
Source2:        .mozconfig
Source3:        basilisk.desktop
Source4:        official.tar.xz

BuildRequires:  pkgconfig(gtk+-3.0) pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(python2)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(sqlite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  python2
BuildRequires:  yasm
BuildRequires:  make
BuildRequires:  zip
BuildRequires:  m4

%description
%summary

%files
%license LICENSE
%doc README.md AUTHORS
%{_prefix}/local/bin/%name
%{_prefix}/local/lib/%name-%{moz_ver}
%{_prefix}/local/share/
%{_iconsdir}/hicolor/
%{_datadir}/applications/%name.desktop

%package devel
Summary:        Development package for %name
Requires:       %name = %version
%description devel
%summary

%files devel
%{_prefix}/local/include/
%{_prefix}/local/lib/%name-devel-%{moz_ver}

%prep
%autosetup -p1 -n %name
tar -xf %{S:1} --strip-components=1 -C %{_builddir}/%name/platform/
tar -xf %{S:4} -C %{_builddir}/%name/%name/branding/

# plans to merge in upstream, per Basilisk-Dev
# awaiting MR
patch -p1 < patches/0001-goanna-disable-pref.diff

cp %{S:2} %{_builddir}/%name
./mach clobber

%build
./mach build

%install
DESTDIR=%{buildroot} ./mach install
install -m 644 -D %{S:3} %{buildroot}/%{_datadir}/applications/%name.desktop

# icons
for s in 16 32 48 256; do
	install -D -m 644 \
		%name/branding/official/default$s.png \
		%{buildroot}/%{_iconsdir}/hicolor/${s}x${s}/apps/%name.png
done

install -D -m 644 %name/branding/official/mozicon128.png \
                  %{buildroot}/%{_iconsdir}/hicolor/128x128/mozicon128.png

