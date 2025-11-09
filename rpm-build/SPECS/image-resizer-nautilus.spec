Name:           image-resizer-nautilus
Version:        1.0.0
Release:        3%{?dist}
Summary:        Nautilus extension for resizing images with right-click menu

License:        GPL-3.0+
URL:            https://github.com/yourusername/image-resizer-nautilus
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       nautilus
Requires:       nautilus-python
Requires:       python3-gobject
Requires:       ImageMagick
Requires:       python3-pillow

%description
A context menu extension for Nautilus file manager that allows
users to resize images through a simple GUI interface.

%prep
%autosetup -n %{name}-%{version}

%build
# Empty - pure Python package

%install
rm -rf %{buildroot}

# Install Python package
python3 setup.py install --root=%{buildroot}

# Install nautilus extension - FIXED: Use exact Python version
mkdir -p %{buildroot}%{_datadir}/nautilus-python/extensions
ln -sf %{python3_sitelib}/image_resizer_nautilus/nautilus_extension.py \
    %{buildroot}%{_datadir}/nautilus-python/extensions/image-resizer-extension.py

%post
echo "Setting up Image Resizer Nautilus Extension..."
if command -v nautilus >/dev/null 2>&1; then
    nautilus -q >/dev/null 2>&1 && echo "Nautilus restarted" || echo "Could not restart nautilus"
fi

%postun
if command -v nautilus >/dev/null 2>&1; then
    nautilus -q >/dev/null 2>&1 || true
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/image-resizer-gui
%{_bindir}/image-resizer-setup
%{_bindir}/image-resizer-uninstall
%{python3_sitelib}/image_resizer_nautilus/
%{python3_sitelib}/*.egg-info/
%{_datadir}/nautilus-python/extensions/image-resizer-extension.py

%changelog
* Thu Nov 07 2024 Your Name <your.email@example.com> - 1.0.0-3
- Fix symlink path to use exact Python version

* Thu Nov 07 2024 Your Name <your.email@example.com> - 1.0.0-2
- Fix nautilus extension symlink path

* Thu Nov 07 2024 Your Name <your.email@example.com> - 1.0.0-1
- Initial package release