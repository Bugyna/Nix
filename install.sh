#!/bin/bash
p=/usr/local/bin

sudo cp n $p/nix
sudo cp src/* $p/Nix
sudo cp $p/Nix/main.py $p/Nix/nix
sudo chmod a+rwx $p/Nix/*

