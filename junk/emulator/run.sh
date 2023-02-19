#!/bin/bash -e

docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it vatech /bin/bash