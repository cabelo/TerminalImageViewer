# norootforbuild
Summary: Small C++ program to display images in a (modern) terminal
Name: tiv
Version: 1.0.0
Release: 2
License: Apache-2.0
Packager:  Alessandro de Oliveira Faria (A.K.A CABELO) <cabelo@opensuse.org>
#Source0:  %{name}-%{version}.tar.gz
Source:  %{name}-git.tar.gz
URL: https://github.com/stefanhaustein/TerminalImageViewer
BuildRoot: %{_tmppath}/%{name}-%{version}-build   
#BuildRequires: -post-build-checks -rpmlint-Factory -rpmlint-mini  -rpmlint
Requires: ImageMagick  
BuildRequires: gcc-c++ pkgconfig ImageMagick  

%if 0%{?centos} || 0%{?rhel}
BuildRequires: libstdc++-devel libstdc++
%endif

%if  0%{?mageia} 
BuildRequires: libstdc++-devel libstdc++
%endif
#BuildRequires: libX11-devel
#%else
#BuildRequires: xorg-x11-devel 
#%endif
#Prefix: %{_prefix}
Group: Productivity/Graphics/Viewers

%description
There are various similar tools (such as timg) using the unicode half block character to display two 24bit pixels per character cell. This program enhances the resolution by mapping 4x8 pixel cells to different unicode characters, using the following algorithm:

For each 4x8 pixel cell of the (potentially downscaled) image:

    Find the color channel (R, G or B) that has the biggest range of values for the current cell
    Split this range in the middle and create a corresponding bitmap for the cell
    Compare the bitmap to the assumed bitmaps for various unicode block graphics characters
    Re-calculate the foreground and background colors for the chosen character
There are various similar tools (such as timg) using the unicode half block character to display two 24bit pixels per character cell. This program enhances the resolution by mapping 4x8 pixel cells to different unicode characters.

%prep
cd $RPM_SOURCE_DIR
if [ -s tiv.tar.gz ] ; then
	if [ -d tiv ] ; then rm -rf tiv ; fi
	tar zxf tiv.tar.gz
else
	if [ -f tiv-git.tar.gz ] ; then
		if [ -d tiv ] ; then rm -rf tiv ; fi
		mkdir tiv
		cd tiv
		tar zxf ../tiv-git.tar.gz --strip=1
                ls -l
	elif [ -d tiv ] ; then
		cd tiv
		git pull
		cd ..
	else
		git clone https://github.com/stefanhaustein/TerminalImageViewer
	fi
fi


#%setup -q
#%setup -qn TerminalImageViewer
#%setup 

%build
cd $RPM_SOURCE_DIR/tiv
#cd $RPM_SOURCE_DIR
cd src/main/cpp

%if 0%{?suse_version} >= 1500
make %{?_smp_mflags}
%endif

%if 0%{?rhel_version} ||  0%{?centos_ver} ||  0%{?suse_version} < 1500
g++ -Wall -fpermissive -fexceptions -O2 -c tiv.cpp -o tiv.o
g++ tiv.o -o tiv -lstdc++ -pthread -s
#g++ tiv.o -o tiv -lstdc++fs -pthread -s
%endif

%if 0%{?mageia}
g++ -std=gnu++11  -Wall -fpermissive -fexceptions -O2 -c tiv.cpp -o tiv.o
g++ tiv.o -o tiv -lstdc++ -pthread -s
%endif

%install
cd $RPM_SOURCE_DIR/tiv
#cd $RPM_SOURCE_DIR
cd src/main/cpp
install -d %{buildroot}/usr/bin
install -d %{buildroot}/usr/share/licenses/tiv 
#%if 0%{?suse_version} >= 1500
%if 0%{?sle_version} 
install -d %{buildroot}/usr/share/doc/packages/tiv
%else
install -d %{buildroot}/usr/share/doc/tiv/
%endif
cp tiv %{buildroot}/usr/bin/tiv
cp ../../../LICENSE %{buildroot}/usr/share/licenses/tiv
#%if 0%{?suse_version} >= 1500
%if 0%{?sle_version} 
cp ../../../README.md %{buildroot}/usr/share/doc/packages/tiv
%else
cp ../../../README.md %{buildroot}/usr/share/doc/tiv/
%endif
%post
%postun

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_bindir}/tiv

%changelog
* Wed Mar 13 2019 Brasil/East 2019  <cabelo@opensuse.org>
- Create package in openSuse Build : Alessandro de Oliveira Faria.



