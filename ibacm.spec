Name: ibacm
Version: 1.0.8
Release: 0.git7a3adb7%{?dist}
Summary: InfiniBand Communication Manager Assistant
Group: System Environment/Daemons
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/rdmacm/%{name}-%{version}-0.git7a3adb7.tar.gz
Source1: ibacm.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libibverbs-devel >= 1.1-1, autoconf, libtool, libibumad-devel
Requires(post): chkconfig
Requires(preun): chkconfig
ExcludeArch: s390 s390x

%description
The ib_acm daemon helps reduce the load of managing path record lookups on
large InfiniBand fabrics by providing a user space implementation of what
is functionally similar to an ARP cache.  The use of ib_acm, when properly
configured, can reduce the SA packet load of a large IB cluster from O(n^2)
to O(n).  The ib_acm daemon is started and normally runs in the background,
user applications need not know about this daemon as long as their app
uses librdmacm to handle connection bring up/tear down.  The librdmacm
library knows how to talk directly to the ib_acm daemon to retrieve data.

%package devel
Summary: Headers file needed when building apps to talk directly to ib_acm
Requires: %{name} = %{version}-%{release}

%description devel
Most applications do not need to know how to talk directly to the ib_acm
daemon, but it does have a socket that it listens on, and it has a
specific protocol for incoming/outgoing data.  So if you wish to build
the ability to communicate directly with ib_acm into your own application,
the protocol used to communicate with it, and the data structures
involved, are in this header file.  Please note that this is an unsupported
method of using this daemon.  The only supported means of using this is
via librdmacm.  As such, even though this header file is provided, no
further documentation is available.  One must read the source if they
wish to make use of this header file.

%prep
%setup -q -n %{name}-%{version}

%build
./autogen.sh
%configure CFLAGS="$CXXFLAGS -fno-strict-aliasing" LDFLAGS=-lpthread
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -fr %{buildroot}/etc/init.d
install -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ibacm

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
	chkconfig --add ibacm
fi

%preun
if [ $1 = 0 ]; then
	chkconfig --del ibacm
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/ib_acme
%{_sbindir}/ibacm
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_initrddir}/ibacm

%files devel
%defattr(-,root,root,-)
%{_includedir}/infiniband/acm.h

%changelog
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

