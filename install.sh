#!/bin/bash
pip3 install pyinstaller
p=/usr/local/bin/

python3 -OO compile.py

cp src/. backup/
sudo cp dist/main $p/nix
echo "copied executable to $p"