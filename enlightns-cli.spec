# Created by pyp2rpm-2.0.0
%global pypi_name enlightns-cli

Name:           python-%{pypi_name}
Version:        0.0.21
Release:        1%{?dist}
Summary:        EnlightNS.com Command Line Interface

License:        GPLv3+
URL:            http://enlightns.com/
Source0:        https://pypi.python.org/packages/source/e/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
 
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
See the long description on https://github.com/EnlightNS/enlightns-cli

%package -n     python2-%{pypi_name}
Summary:        EnlightNS.com Command Line Interface
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python-setuptools
%description -n python2-%{pypi_name}
See the long description on https://github.com/EnlightNS/enlightns-cli

%package -n     python3-%{pypi_name}
Summary:        EnlightNS.com Command Line Interface
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-setuptools
%description -n python3-%{pypi_name}
See the long description on https://github.com/EnlightNS/enlightns-cli


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%py3_install
cp %{buildroot}/%{_bindir}/enlightns-cli %{buildroot}/%{_bindir}/enlightns-cli-3
ln -sf %{_bindir}/enlightns-cli-3 %{buildroot}/%{_bindir}/enlightns-cli-%{python3_version}

%py2_install
cp %{buildroot}/%{_bindir}/enlightns-cli %{buildroot}/%{_bindir}/enlightns-cli-2
ln -sf %{_bindir}/enlightns-cli-2 %{buildroot}/%{_bindir}/enlightns-cli-%{python2_version}


%files -n python2-%{pypi_name} 
%doc README.rst LICENSE
%{_bindir}/enlightns-cli
%{_bindir}/enlightns-cli-2
%{_bindir}/enlightns-cli-%{python2_version}
%{python2_sitelib}/enlightns_cli
%{python2_sitelib}/enlightns_cli-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name} 
%doc README.rst LICENSE
%{_bindir}/enlightns-cli-3
%{_bindir}/enlightns-cli-%{python3_version}
%{python3_sitelib}/enlightns_cli
%{python3_sitelib}/enlightns_cli-%{version}-py?.?.egg-info

%changelog
* Fri Sep 18 2015 John Doe <john@doe.com> - 0.0.21-1
- Initial package.
