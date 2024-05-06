%global commit0 a6dccbbf5a955489d20d996234b6ebb481183ed7
%global date 20240416
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global debug_package %{nil}
%global dkms_name ivsc

Name:       dkms-%{dkms_name}
Version:    0
Release:    1.%{date}git%{shortcommit0}%{?dist}
Summary:    Driver for Intel Vision Sensing Controller(IVSC)
License:    GPLv3
URL:        https://github.com/intel/ivsc-driver
BuildArch:  noarch

Source0:    %{url}/archive/%{commit0}.tar.gz#/ivsc-driver-%{shortcommit0}.tar.gz
Source1:    dkms-no-weak-modules.conf
Patch0:     %{name}-conf.patch

Provides:   %{dkms_name}-kmod = %{version}
Requires:   %{dkms_name}-kmod-common = %{version}
Requires:   dkms

%description
Driver for Intel Vision Sensing Controller(IVSC).

%prep
%autosetup -p1 -n ivsc-driver-%{commit0}

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%if 0%{?fedora}
# Do not enable weak modules support in Fedora (no kABI):
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
* Mon May 06 2024 Simone Caronni <negativo17@gmail.com> - 0-1.20240416gita6dccbb
- First build.
