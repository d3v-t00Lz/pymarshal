# Packaging
This document describes how to create packages for various platforms from
your Python code.

## Docker
```
# Build the desired image
make docker-cli
make docker-rest
# Or
ORG=my-docker-registry.something.org make docker-cli

# Upload to your registry
# (requires that you first tag the image appropriately for the Docker registry)
docker push $DOCKER_TAG

# Run locally, the Dockerfile is designed to take arguments as a CLI,
# change the Dockerfile as needed for your use-case
docker run someorg/pytemplate-cli version
```

## Windows
From a Windows computer:
```
# First read windows/README.md for instructions on how to install dependencies

# Create a single file .exe
# Or use any other spec
pyinstaller windows/onefile-qt.spec

# Create an installer
python windows/release.py
```

## MacOS
From a MacOS computer:
```
# Install depdencies, first time only
./macos/homebrew_deps.sh

# Create an app bundle packaged in a DMG for MacOS
python3 macos/release.py
```

## pypi / pip
```
# Upload your package to PyPi so that anybody can install using pip.
#
# NOTE: This means the entire public internet.  Do not enable the pypi
#       option in tools/fork.py for private/proprietary Python packages.
#
# Requires `twine` to be installed, and a local twine config with your
# pypi username and password
make pypi
```

## Linux
### AppImage
See `appimage/README.md` for instructions.  Also see `appimage/release.py -h`.

### RPM distros (Red Hat, CentOS, Fedora, Rocky, Alma, etc...)
```
# Remember to edit rpm.spec to include the correct information and dependencies
make rpm
```

### DEB distros (Debian, Ubuntu, etc...)
```
# Remember to edit debian/control to include the correct information
# and dependencies
make deb
```

