%define name     rtpproxy
%define ver      1.2.1
%define rel      1.0

Name:           %name
Version:        %ver
Release:        %rel%{?dist}
Summary:        A symmetric RTP proxy
Group:          Applications/Internet
License:        BSD
URL:            http://www.rtpproxy.org/
Source0:        http://www.b2bua.org/chrome/site/rtpproxy-%{version}.tar.gz
Patch1:         rtpproxy-patch.patch
Packager:       Alfred E. Heggestad <aeh@db.org>
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is symmetric RTP proxy designed to be used in conjunction with
the SIP Express Router (SER) or any other SIP proxy capable of
rewriting SDP bodies in SIP messages that it processes.

%debug_package
%prep
%setup -q
ln -s %{_builddir}/%{name}-%{version} %{_builddir}/rtpproxy
tar -xvf %{_sourcedir}/srtp-1.4.2.tgz -C %{_builddir}/rtpproxy
mkdir %{_builddir}/rtpproxy/lib
%patch1 -p0

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/etc/init.d
install -m755 rpm/rtpproxy.init \
              $RPM_BUILD_ROOT/etc/init.d/rtpproxy
mkdir -p $RPM_BUILD_ROOT/etc/openbranch
> $RPM_BUILD_ROOT/etc/openbranch/rtpproxy.cfg

%post

%preun
if [ "$1" = "0" ]; then
        service %name stop >/dev/null 2>&1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README 
%{_mandir}/man8/*
%attr(755,root,root) %{_bindir}/rtpproxy
%attr(755,root,root) %{_bindir}/makeann
%config %attr(755,root,root) /etc/init.d/*
%config %attr(644,root,root) /etc/openbranch/rtpproxy.cfg
%{_libdir}/* 


%changelog
* Mon Jan 12 2009 Alfred E. Heggestad <aeh@db.org>
- Updated for version 1.2

* Tue Jan 30 2007 Alfred E. Heggestad <aeh@db.org> - 0.3.1
- Initial build.
