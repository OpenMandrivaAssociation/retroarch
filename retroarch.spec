%define build_ffmpeg 1
%define build_shaders 0

Summary:	A modular multi-system emulator system
Name:		retroarch
Version:	0.9.9
Release:	2
Group:		Emulators
License:	GPLv3
Url:		http://www.libretro.org
Source0:	http://themaister.net/retroarch-dl/%{name}-%{version}.tar.gz
Source1:	%{name}.png
Source2:	%{name}-shaders.tar.bz2
Patch0:		retroarch-0.9.9-ffmpeg.patch
BuildRequires:	imagemagick
%if %{build_shaders}
# for shaders support, requires non-free repo
BuildRequires:	cg-devel
%endif
%if %{build_ffmpeg}
# ffmpeg part
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libswscale)
%endif
# The rest
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(zlib)
Requires:	libretro
Suggests:	retroarch-phoenix

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

%prep
%setup -q -a2
%patch0 -p1

%build
# Quickbuild script, not autotools
./configure \
	--prefix=%{_prefix} \
	--enable-al \
	--enable-alsa \
	--enable-fbo \
%if %{build_ffmpeg}
	--enable-ffmpeg \
%else
	--disable-ffmpeg \
%endif
	--enable-netplay \
	--enable-pulse \
	--enable-sdl \
	--enable-sdl_image \
	--enable-threads \
	--enable-xinerama \
	--enable-zlib \
%if %{build_shaders}
	--enable-cg \
%else
	--disable-cg \
%endif
	--disable-egl \
	--disable-jack \
	--disable-oss \
	--disable-python \
	--disable-vg
%make

%install
%makeinstall_std

# Set path where to search for libretro
sed -i s,.*libretro_path.*,"libretro_path = \"%{_libdir}/libretro\"",g %{buildroot}%{_sysconfdir}/%{name}.cfg
sed -i s,.*video_shader_dir.*,"video_shader_dir = \"%{_var}/games/%{name}/shaders\"",g %{buildroot}%{_sysconfdir}/%{name}.cfg

# install menu entry
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=RetroArch
Comment=A modular multi-system emulator system
Exec=%{_bindir}/%{name}
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF

install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%if %{build_shaders}
mkdir -p %{buildroot}%{_var}/games/%{name}/shaders
cp -r retroarch-shaders/* %{buildroot}%{_var}/games/%{name}/shaders/
%endif

%files
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%{_bindir}/%{name}
%{_bindir}/%{name}-joyconfig
%{_bindir}/%{name}-zip
%{_bindir}/retrolaunch
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%if %{build_shaders}
%dir %attr(0777,root,root) %{_var}/games/%{name}/shaders
%{_var}/games/%{name}/shaders/*
%endif
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-joyconfig.1*

