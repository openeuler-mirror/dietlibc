%global fixcflags       -fomit-frame-pointer -fno-exceptions -fno-asynchronous-unwind-tables %xtra_fixcflags -Os -g3 -Werror-implicit-function-declaration -Wno-unused -Wno-switch
%global basemakeflags   prefix=%pkglibdir BINDIR=%{_bindir} MAN1DIR=%{_mandir}/man1 CFLAGS="$RPM_OPT_FLAGS %fixcflags $XTRA_CFLAGS" PDIET=%pkglibdir STRIP=:

%global pkglibdir       /usr/lib/dietlibc

%ifarch x86_64
%bcond_without          ssp
%else
%bcond_with             ssp
%endif

Name:           dietlibc
Version:        0.34
Release:        2
Summary:        A libc optimized for small size
License:        GPLv2
URL:            http://www.fefe.de/dietlibc/
Source0:        https://www.fefe.de/dietlibc/%{name}-%{version}.tar.xz
Source1:        http://www.fefe.de/dietlibc/%{name}-%{version}.tar.xz.sig

Patch0001:      dietlibc-insecure-defpath.patch

Obsoletes:      dietlibc-lib < %{version}-%{release}

BuildRequires:  gcc gdb

Requires:       %{name}-devel = %{version}-%{release}

%description
The diet libc is a libc that is optimized for small size. It can be used to create small statically
linked binaries for Linux on alpha, arm, hppa, ia64, i386, mips, s390, sparc, sparc64, ppc and x86_64.

%package        devel
Summary:        Development documents for %{name}
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-header < %{version}-%{release}
Provides:       %{name}-header = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release} %{name}-static%{?_isa} = %{version}-%{release}

%description    devel
The package provides libraries and some other development documents for developing applications
that use %{name}.

%package        help
Summary:        Help documents for %{name}

%description    help
The package provides man pages and some other help information for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}

%if %{without ssp}
sed -i -e 's!^#define WANT_SSP$!// \0!g;
           s!.*\(#define WANT_STACKGAP\).*!\1!g' dietfeatures.h
%global xtra_fixcflags  -fno-stack-protector
%else
%global xtra_fixcflags  %nil
%endif

sed -i -e '/#define \(WANT_LARGEFILE_BACKCOMPAT\)/d' dietfeatures.h
sed -i -e '/#define \(WANT_VALGRIND_SUPPORT\)/d' dietfeatures.h

%build
%make_build %basemakeflags all

%install
install -d -m755 $RPM_BUILD_ROOT/etc
%make_install %basemakeflags

ln -s lib-%{_arch} ${RPM_BUILD_ROOT}%pkglibdir/lib-%{_arch}-%{_vendor}

chmod a-x $RPM_BUILD_ROOT%pkglibdir/lib-*/*.o

%check
XTRA_CFLAGS='-fno-builtin'
%make_build %basemakeflags -C test all DIET=$(echo `pwd`/bin-*/diet) -k || :
%make_build %basemakeflags -C test/inet all DIET=$(echo `pwd`/bin-*/diet) || :

cd test
ulimit -m $[ 128*1024 ] -v $[ 256*1024 ] -d $[ 128*1024 ] -s 512

%files
%doc AUTHOR COPYING
%{_bindir}/*
%exclude %{_bindir}/dnsd

%files devel
%pkglibdir

%files help
%doc BUGS CAVEAT CHANGES FAQ PORTING README* SECURITY THANKS TODO
%doc %{_mandir}/*/*

%changelog
* Thu Feb 27 2020 zhouyihang<zhouyihang1@huawei.com> - 0.34-2
- Package init
