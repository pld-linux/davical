# TODO:
# - package docs?
# - test lighttpd config
Summary:	CalDAV Server
Summary(pl.UTF-8):	Serwer CalDAV
Name:		davical
Version:	1.0.2
Release:	0.7
License:	GPL v2
Group:		Applications
Source0:	http://debian.mcmillan.net.nz/packages/davical/%{name}-%{version}.tar.gz
# Source0-md5:	340ab213a6303742c66a8028989c2027
Source1:	%{name}.conf
Source2:	%{name}-lighttpd.conf
URL:		http://davical.org/
Patch0:		%{name}-php_data_dir.patch
Patch1:		%{name}-conf_path.patch
Patch2:		awl_version.patch
BuildRequires:	gettext-tools
BuildRequires:	php-awl >= 0.49
BuildRequires:	php-pear-PhpDocumentor
Requires:	perl(DBD::Pg)
Requires:	perl(YAML)
Requires:	perl-base
Requires:	php-awl >= 0.48
Requires:	php-pcre
Requires:	php-pdo-pgsql
Requires:	php-session
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	webserver(indexfile)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps

%description
The DAViCal CalDAV Server is a repository for calendar, todo and
journal entries to be accessed via CalDAV clients such as Evolution,
Sunbird, Lightning, Mulberry, Chandler, Apple iCal or the iPhone.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i 's#^AWL_LOCATION="\.\./awl"$#AWL_LOCATION=%{php_data_dir}/awl#' scripts/po/rebuild-translations.sh
sed -i /^================================================================/q COPYING

%build
# we can force awl_version if required
# AWL_VERSION="0.50" scripts/build-always.sh < inc/always.php.in > htdocs/always.php
scripts/build-always.sh < inc/always.php.in > htdocs/always.php
phpdoc -c docs/api/phpdoc.ini
scripts/po/rebuild-translations.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_webapps}/%{name}
install -d $RPM_BUILD_ROOT%{_appdir}

cp -a config/example-config.php $RPM_BUILD_ROOT%{_webapps}/%{name}/config.php
cp -a config/example-administration.yml $RPM_BUILD_ROOT%{_webapps}/%{name}/administration.yml
cp -a inc $RPM_BUILD_ROOT%{_appdir}
cp -a htdocs $RPM_BUILD_ROOT%{_appdir}
cp -a dba $RPM_BUILD_ROOT%{_appdir}

rm -rf $RPM_BUILD_ROOT%{_appdir}/dba/windows
rm -f $RPM_BUILD_ROOT%{_appdir}/inc/always.php.in*

install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{name}/httpd.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{name}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_webapps}/%{name}/lighttpd.conf

cp -a locale $RPM_BUILD_ROOT%{_datadir}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{name}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{name}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{name}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{name}

%triggerin -- lighttpd
%webapp_register lighttpd %{name}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{name}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc COPYING ChangeLog CREDITS README TODO scripts/*.php
%dir %attr(750,root,http) %{_sysconfdir}/webapps/%{name}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{name}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{name}/administration.yml
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{name}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{name}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{name}/lighttpd.conf
%dir %{_appdir}
%dir %{_appdir}/dba
%{_appdir}/dba/*.sql
%{_appdir}/dba/*.txt
%{_appdir}/dba/patches
%{_appdir}/dba/views
%attr(755,root,root) %{_appdir}/dba/create-database.sh
%attr(755,root,root) %{_appdir}/dba/update-davical-database
%{_appdir}/htdocs
%{_appdir}/inc
