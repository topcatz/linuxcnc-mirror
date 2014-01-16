#!/bin/sh
rm -f bitops
set -e
gcc -I../../include bitops.c -o bitops
./bitops
