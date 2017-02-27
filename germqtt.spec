Name:		germqtt
Version:	0.1.0
Release:	2%{?dist}
Summary:	Publish a gerrit event stream on MQTT

License:	Apache
URL:		http://openstack.org
Source0:	https://tarballs.openstack.org/germqtt/germqtt-%{version}.tar.gz
Source1:        germqtt.service

BuildRequires:	python2-devel
BuildRequires:  python-pbr
BuildRequires:	python-hacking
BuildRequires:	python-coverage
BuildRequires:	python-setuptools
BuildRequires:	python-sphinx
BuildRequires:	systemd

Requires:	python2-gerritlib
Requires:	python-pbr
Requires:	python-six
Requires:	python-paho-mqtt
Requires:	python-daemon

%description
Germqtt is a tool for publishing a gerrit event stream into MQTT.

%prep
%autosetup -n germqtt-%{version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# We handle requirements ourselves, remove requirements.txt
rm -rf requirements.txt test-requirements.txt

%build
%py2_build


%install
%py2_install
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
mkdir -p %{buildroot}/%{_sysconfdir}/
install -p -D -m 644 etc/germqtt.conf %{buildroot}/%{_sysconfdir}/%{name}/germqtt.conf

%check
%{__python2} setup.py test

%pre
getent group germqtt >/dev/null || groupadd -r germqtt
getent passwd germqtt >/dev/null || \
useradd -r -g germqtt -G germqtt -d /usr/share/germqtt -s /sbin/nologin \
-c "germqtt daemon" germqtt
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{python2_sitelib}/
%{_bindir}/germqtt
%config(noreplace) %{_sysconfdir}/*
%{_unitdir}/*

%changelog
* Mon Feb 27 2017 Matthieu Huin <mhuin@redhat.com> - 0.1.0-2
- Add service file, conf installation, cleanup scripts

* Fri Feb 24 2017 Matthieu Huin <mhuin@redhat.com> - 0.1.0-1
- Initial package
