%define  oname RetroArch

Summary:	A modular multi-system emulator system
Name:		retroarch
Version:	1.8.4
Release:	1
License:	GPLv3+
Group:		Emulators
Url:		http://www.libretro.org
Source0:	https://github.com/libretro/RetroArch/archive/v%{version}/%{oname}-%{version}.tar.gz
BuildRequires:	imagemagick
#BuildRequires:	cg-devel
BuildRequires:  mbedtls-devel
BuildRequires:  pkgconfig(caca)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:  pkgconfig(dri)
BuildRequires:	pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  egl-devel
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(udev)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-egl-backend)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
#Qt
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Network)

Recommends:	libretro
Recommends:	retroarch-phoenix

%description
RetroArch is a modular multi-system emulator system that is designed to be
fast, lightweight, and portable. It has features few other emulators frontends
have, such as real-time rewinding and game-aware shading.

For each emulator 'core', RetroArch makes use of a library API that we like
to call 'libretro'.

Think of libretro as an interface for emulator and game ports. You can make
a libretro port once and expect the same code to run on all the platforms
that RetroArch supports. It's designed with simplicity and ease of use in
mind so that the porter can worry about the port at hand instead of having
to wrestle with an obfuscatory API.

%files
%doc COPYING README.md
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%{_bindir}/%{name}
%{_bindir}/%{name}-cg2glsl
#{_bindir}/%{name}-joyconfig
#{_bindir}/retrolaunch
%{_datadir}/applications/%{name}.desktop
#{_datadir}/pixmaps/%{name}.png
/usr/share/pixmaps/retroarch.svg
#(_datadir)/pixmaps/retroarch.svg
#dir %attr(0777,root,root) %{_var}/games/%{name}/shaders
#{_var}/games/%{name}/shaders/*
%{_mandir}/man6/retroarch*


#----------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}

%build
# Quickbuild script, not autotools
./configure \
	--prefix=%{_prefix} \
	--enable-al \
	--enable-alsa \
	--enable-ffmpeg \
	--enable-networking \
	--enable-pulse \
	--enable-qt \
	--enable-sdl2 \
	--enable-threads \
	--enable-xinerama \
	--enable-zlib \
	--disable-cg \
	--enable-egl \
	--disable-jack \
	--disable-oss \
	--disable-vg
%make_build

%install
%make_install

# Set path where to search for libretro
sed -i s,.*libretro_path.*,"libretro_path = \"%{_libdir}/libretro\"",g %{buildroot}%{_sysconfdir}/%{name}.cfg
sed -i s,.*video_shader_dir.*,"video_shader_dir = \"%{_var}/games/%{name}/shaders\"",g %{buildroot}%{_sysconfdir}/%{name}.cfg

# install menu entry
#mkdir -p %{buildroot}%{_datadir}/applications/
#cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
#[Desktop Entry]
#Name=RetroArch
#Comment=A modular multi-system emulator system
#Exec=%{_bindir}/%{name}
#Icon=%{_datadir}/pixmaps/%{name}.png
#Terminal=false
#Type=Application
#Categories=Game;Emulator;
#EOF

#install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png
