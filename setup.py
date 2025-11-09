#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="image-resizer-nautilus",
    version="1.0.0",
    description="Nautilus extension for resizing images with right-click menu",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Faghmie Davids",
    author_email="faghmie@gmail.com",
    url="https://github.com/faghmie/image-resizer-nautilus",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        "PyGObject>=3.38.0",
    ],
    extras_require={
        'dev': ['build', 'twine', 'wheel'],
    },
    entry_points={
        'console_scripts': [
            'image-resizer-gui=image_resizer_nautilus.image_resizer:main',
            'image-resizer-setup=image_resizer_nautilus.extension_setup:main',
            'image-resizer-uninstall=image_resizer_nautilus.uninstall:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: GNOME",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment :: GNOME",
    ],
)