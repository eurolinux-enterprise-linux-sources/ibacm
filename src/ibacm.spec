%define ver 1.0.5

Name: ibacm
Version: 1.0.5
Release: 1%{?dist}
Summary: InfiniBand Communication Manager Assistant

Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/rdmacm/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libibverbs-devel >= 1.1-1

%description
ibacm assists with establishing communication over Infiniband.

%package svc
Summary: IB CM pre-connection service application
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release} %{_includedir}/infiniband/verbs.h

%description svc
Application daemon for IB CM pre-connection services.

%prep
%setup -q -n %{name}-%{ver}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/ib_acme
%{_sbindir}/ib_acm
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_includedir}/infiniband/acm.h

%changelog
