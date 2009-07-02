#
Summary:	Likewise - Linux authentication on a Microsoft network using AD
Name:		likewise-open
Version:	4.0.0
Release:	0.2
License:	GPL v3
Group:		Applications
Source0:	http://www.likewisesoftware.com/bits/%{name}-%{version}.tar.gz
# Source0-md5:	089a479054ddb308702110fa365c31c8
Patch0:		%{name}-chmod.patch
URL:		http://www.likewisesoftware.com/
BuildRequires:	autoconf
BuildRequires:	cups-devel
BuildRequires:	libgdiplus-devel
BuildRequires:	mono-compat-links
BuildRequires:	mono-csharp
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	samba-devel
BuildRequires:	heimdal-devel
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Likewise Open enables Linux authentication on a Microsoft network
using Active Directory. A user can now interactively log in to the
Linux machine using Active Directory credentials, and can access any
kerberized services that the Linux machine hosts.

%prep
%setup -q -n %{name}-%{version}-release
%patch0 -p1

%build
cd winbindd/source
%configure \
	--with-configdir=%{_sysconfdir}/samba \
	--with-lockdir=%{_var}/lib/%{name} \
	--with-logfilebase=%{_var}/log/%{name} \
	--with-piddir=%{_var}/run \
	--with-privatedir=%{_sysconfdir}/samba \
	--enable-require-wrfile-keytab \
	--with-ads \
	--with-fhs \
	--without-readline \
	--with-included-popt \
	--with-pam \
	--with-shared-modules=idmap_lwopen \
	--enable-cups \
	--enable-iprint \
	--with-syslog \
	--with-acl-support \
	--enable-require-wrfile-keytab
cd -
cd domainjoin
%{__autoconf}
%{__autoheader}
%configure 

cd -

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/bin
install -d $RPM_BUILD_ROOT/%{_lib}/security

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT/usr/lib/samba/security/pam_lwidentity.so $RPM_BUILD_ROOT/%{_lib}/security

%ifarch %{x8664}
install -d $RPM_BUILD_ROOT%{_libdir}/samba
%{__mv} $RPM_BUILD_ROOT/usr/lib/samba/libwbclient.so $RPM_BUILD_ROOT%{_libdir}/samba/libwbclient.so
%{__mv} $RPM_BUILD_ROOT/usr/lib/samba/idmap $RPM_BUILD_ROOT%{_libdir}/samba/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/domainjoin-cli
%attr(755,root,root) %{_bindir}/lwiinfo
%attr(755,root,root) %{_bindir}/lwimsg
%attr(755,root,root) %{_bindir}/lwinet
%attr(755,root,root) %{_libdir}/samba/libwbclient.so  
%attr(755,root,root) %{_sbindir}/likewise-winbindd
%{_includedir}/samba/wbclient.h
%attr(755,root,root) /%{_lib}/security/pam_lwidentity.so
%dir %{_libdir}/samba/idmap
%attr(755,root,root) %{_libdir}/samba/idmap/lwopen.so
