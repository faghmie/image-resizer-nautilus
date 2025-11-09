.PHONY: all deb rpm clean

all: deb rpm

deb:
	./build-deb.sh

rpm:
	./build-rpm.sh

clean:
	rm -rf debian/ rpm-build/ build/ dist/ *.egg-info/
	rm -f ../image-resizer-nautilus_* *.deb *.rpm

test-deb:
	# Test installation of built deb package
	sudo dpkg -i ../image-resizer-nautilus_*.deb

test-rpm:
	# Test installation of built rpm package
	sudo rpm -ivh rpm-build/RPMS/noarch/image-resizer-nautilus-*.rpm

uninstall-deb:
	sudo dpkg -r image-resizer-nautilus

uninstall-rpm:
	sudo rpm -e image-resizer-nautilus