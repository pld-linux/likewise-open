#
Summary:	Likewise - Linux authentication on a Microsoft network using AD
Name:		likewise-open
Version:	4.0.0
Release:	0.1
License:	GPL v3
Group:		Applications
Source0:	http://www.likewisesoftware.com/bits/%{name}-%{version}.tar.gz
# Source0-md5:	089a479054ddb308702110fa365c31c8
URL:		http://www.likewisesoftware.com/
BuildRequires:	autoconf
BuildRequires:	cups-devel
BuildRequires:	samba-devel
BuildRequires:	krb5-devel
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

%build
cd winbindd/source
%{__autoconf} -I m4 -I lib/replace
%{__autoheader}
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
%configure \
	--with-configdir=%{_sysconfdir}/samba \
	--with-lockdir=/var/lib/%{name} \
	--with-logfilebase=/var/log/%{name} \
	--with-piddir=/var/run
cd -

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
