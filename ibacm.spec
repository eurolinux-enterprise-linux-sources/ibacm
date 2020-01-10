%global _hardened_build 1

Name: ibacm
Version: 1.2.0
Release: 1%{?dist}
Summary: InfiniBand Communication Manager Assistant
Group: System Environment/Daemons
License: GPLv2 or BSD
Url: https://github.com/ofiwg/ibacm
Source: https://github.com/ofiwg/${name}/archive/v%{version}.tar.gz
Source1: ibacm.service
Patch0001: 0001-Coverity-and-compile-warning-fixes.patch
BuildRequires: libibverbs-devel >= 1.2.0
BuildRequires: libibumad-devel
BuildRequires: systemd-units
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

# libibacmp.so is a plugin for the ibacm daemon, not a public library.
# Do not advertise it in RPM metadata:
%global _privatelibs libibacmp[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
The ibacm daemon helps reduce the load of managing path record lookups on
large InfiniBand fabrics by providing a user space implementation of what
is functionally similar to an ARP cache.  The use of ibacm, when properly
configured, can reduce the SA packet load of a large IB cluster from O(n^2)
to O(n).  The ibacm daemon is started and normally runs in the background,
user applications need not know about this daemon as long as their app
uses librdmacm to handle connection bring up/tear down.  The librdmacm
library knows how to talk directly to the ibacm daemon to retrieve data.

%package devel
Summary: Headers file needed when building apps to talk directly to ibacm
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Most applications do not need to know how to talk directly to the ibacm
daemon, but it does have a socket that it listens on, and it has a
specific protocol for incoming/outgoing data.  So if you wish to build
the ability to communicate directly with ibacm into your own application,
the protocol used to communicate with it, and the data structures
involved, are in this header file.  Please note that this is an unsupported
method of using this daemon.  The only supported means of using this is
via librdmacm.  As such, even though this header file is provided, no
further documentation is available.  One must read the source if they
wish to make use of this header file.

%prep
%setup -q
%patch0001 -p1

%build
./autogen.sh
%configure CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
make %{?_smp_mflags}
util/ib_acme -D . -O
# Fixup a multilib conflict in ibacm_opts.cfg:
sed -i -e '/^# Specifies the directory of the provider libraries$/ a\
# Use /usr/lib64/ibacm on 64bit, /usr/lib/libacm on 32bit.
' -e 's%^\(# provider_lib_path /usr/\)lib\(64\)\?/ibacm$%\1lib64/ibacm%' ibacm_opts.cfg

%install
make DESTDIR=%{buildroot} install
rm -fr %{buildroot}%{_sysconfdir}/init.d
find %{buildroot} -name '*.la' -delete
install -D -m 644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/ibacm_opts.cfg
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/ibacm.service

%post
%systemd_post ibacm.service

%preun
%systemd_preun ibacm.service

%postun
%systemd_postun_with_restart ibacm.service

%files
%doc AUTHORS README
%license COPYING
%{_bindir}/ib_acme
%{_sbindir}/ibacm
%{_sysconfdir}/rdma
%config(noreplace)%{_sysconfdir}/rdma/ibacm_opts.cfg
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_unitdir}/ibacm.service
%{_libdir}/ibacm

%files devel
%{_includedir}/infiniband/acm.h
%{_includedir}/infiniband/acm_prov.h

%changelog
* Thu Apr 21 2016 Honggang Li <honli@redhat.com> - 1.2.0-1
- Update to latest upstream release version 1.2.0.
- Related: bz1273143

* Tue Aug 04 2015 Michal Schmidt <mschmidt@redhat.com> - 1.1.0-1
- Update to upstream release 1.1.0.
- Resolves: bz1249809

* Fri Jul 17 2015 Michal Schmidt <mschmidt@redhat.com> - 1.0.10-0.3.20150717git825da3ccd2
- Put libibacmp.so in the main package, it's needed at runtime.
- No need to run ldconfig, the .so is not in the linker path.
- Filter the plugin from RPM provides.
- Related: bz1169952

* Fri Jul 17 2015 Michal Schmidt <mschmidt@redhat.com> - 1.0.10-0.2.20150717git825da3ccd2
- Fixup multilib conflict in ibacm_opts.cfg.
- Related: bz1169952

* Fri Jul 17 2015 Michal Schmidt <mschmidt@redhat.com> - 1.0.10-0.1.20150717git825da3ccd2
- Update to pre-release git snapshot of 1.0.10.
- Adds libibacmp shared library.
- Rebase coverity patch.
- Minor spec file cleanup.
- Resolves: bz1169952

* Fri Jun 05 2015 Doug Ledford <dledford@redhat.com> - 1.0.9-2
- Build on s390
- Related: bz1186159

* Thu Oct 09 2014 Doug Ledford <dledford@redhat.com> - 1.0.9-1
- Update to latest upstream release
- Make sure build is hardened
- Resolves: bz1092538

* Wed Jan 22 2014 Doug Ledford <dledford@redhat.com> - 1.0.8-4
- Fix Requires for scriptlets
- Resolves: bz1056590

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.8-3
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 Doug Ledford <dledford@redhat.com> - 1.0.8-2
- Fixes for coverity scan defects found
- Related: bz839190

* Tue Nov 26 2013 Doug Ledford <dledford@redhat.com> - 1.0.8-1
- Update to official 1.0.8 release
- Related: bz839190

* Tue Mar 26 2013 Doug Ledford <dledford@redhat.com> - 1.0.8-0.git7a3adb7.1
- Add one additional patch from upstream
- Convert to systemd unit file
- Resolves: bz839190

* Mon Oct 15 2012 Doug Ledford <dledford@redhat.com> - 1.0.8-0.git7a3adb7
- Update to latest upstream via git repo
- Resolves: bz866222, bz866223

* Thu Apr 05 2012 Doug Ledford <dledford@redhat.com> - 1.0.5-3
- Until the next upstream release, the pid file is in a wonky location.
  Make the init script know about that location so we can stop properly.
- Resolves: bz808599

* Thu Apr 05 2012 Doug Ledford <dledford@redhat.com> - 1.0.5-2
- Don't install the address file or config file, the config file isn't
  strictly needed and defaults will be used if it isn't installed, but
  with the address file we specifically need to build one based upon
  the machine where the program is installed, a default file is not only
  not helpful, but it messes up the daemon.
- Related: bz700285

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 1.0.5-1
- Ininital version for rhel6
- Related: bz700285

