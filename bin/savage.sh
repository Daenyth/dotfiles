#!/bin/bash

#Copied from official /usr/bin/savage launcher
cd "/opt/savage"
LD_LIBRARY_PATH=libs:$LD_LIBRARY_PATH
xinit ./silverback.bin "$@" -- :1
exit $?

