#!/bin/bash -e

export DOCKER_BUILDKIT=1

# Make sure we're in the correct spot
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd)"
cd $DIR

# Create temp build dir if non-existent
BUILD_DIR="$DIR/build"
mkdir -p $BUILD_DIR $OUTPUT_DIR

# Copy rootfs image to build dir
cp $DIR/../jtag/rootfs.tar.gz $BUILD_DIR

# Get statically linked programs if non-existent
if [ ! -f $BUILD_DIR/gdb ]; then
  echo "Downloading GDB"
  wget -O $BUILD_DIR/gdb https://github.com/hugsy/gdb-static/raw/master/gdb-7.10.1-arm6v
fi

if [ ! -f $BUILD_DIR/strace ]; then
  echo "Downloading strace"
  wget -O $BUILD_DIR/strace https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/arm/strace
fi

# timezone
cp /etc/localtime $BUILD_DIR

# Register qemu multiarch
if [ "$(uname -p)" != "aarch64" ]; then
  docker run --rm --privileged multiarch/qemu-user-static:register --reset
fi

# Start docker build
echo "Building image"
export DOCKER_CLI_EXPERIMENTAL=enabled
docker build -f Dockerfile.vatech -t vatech $BUILD_DIR
