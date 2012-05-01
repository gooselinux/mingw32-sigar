%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}
%global shortname sigar

Name:		mingw32-%{shortname}
Version:	1.6.5
Release:	0.1.git833ca18%{?dist}.4
Summary:	System Information Gatherer And Reporter for Windows

%global sigar_suffix  0-g4b67f57
%global sigar_hash    833ca18

Group:		Development/Libraries

License:	ASL 2.0
URL:		http://sigar.hyperic.com/

# Once 1.6.5 is released, we can use tarballs from GitHub:
#    Source0:	http://download.github.com/hyperic-sigar-{name}-{version}-{sigar_suffix}.tar.gz
#
# Until then the tarball can be re-generated with:
#    git clone git://github.com/hyperic/sigar.git
#    cd sigar
#    git archive --prefix=sigar-1.6.5/ 833ca18 | bzip2 > sigar-1.6.5-833ca18.tbz2
#
# The diff from 1.6.4 is too huge to contemplate cherrypicking from
Source0:	%{shortname}-%{version}-%{sigar_hash}.tbz2
Patch1:		sigar-mingw.patch
#Source0:	http://prdownloads.sourceforge.net/sourceforge/%{shortname}/hyperic-%{shortname}-%{version}-src.tar.gz
BuildRoot:	%{_tmppath}/%{shortname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	mingw32-gcc cmake
BuildRequires:  redhat-rpm-config make
BuildRequires:  mingw32-filesystem >= 57

BuildArch:      noarch

%description
The Sigar API provides a portable interface for gathering system
information such as:
- System memory, swap, CPU, load average, uptime, logins
- Per-process memory, CPU, credential info, state, arguments,
  environment, open files
- File system detection and metrics
- Network interface detection, configuration info and metrics
- Network route and connection tables

This information is available in most operating systems, but each OS
has their own way(s) providing it. SIGAR provides developers with one
API to access this information regardless of the underlying platform.

#The core API is implemented in pure C with bindings currently
#implemented for Java, Perl and C#.

%prep
# When using the GitHub tarballs, use:
# setup -q -n hyperic-{shortname}-{sigar_hash}
%setup -q -n %{shortname}-%{version}
%patch1 -p1

%build
PATH=%{_mingw32_bindir}:$PATH

mkdir build
pushd build
%{_mingw32_cmake} ..
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog README LICENSE NOTICE AUTHORS
%{_mingw32_bindir}/libsigar.dll
%{_mingw32_libdir}/libsigar.dll.a
%{_mingw32_includedir}/sigar*.h

%changelog
* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.6.5-0.1.git833ca18.4
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.6.5-0.1.git833ca18.3
- The use of ExclusiveArch conflicts with noarch, using an alternate COLLECTION to limit builds
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.6.5-0.1.git833ca18.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.6.5-0.1.git833ca18.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Wed Dec 1 2010 Andrew Beekhof <andrew@beekhof.net> - 1.6.5-0.1.git833ca18
- Initial checkin
