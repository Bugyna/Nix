#!/bin/bash
p=/usr/local/bin

sudo cp src/*.py backup/
echo "source was backed up in /backup"
sudo cp src/main.py src/highlighter.py src/lexer.py src/handlers.py src/widgets.py src/parser.py src/gr.py src/ascii_art.py src/keybinds_conf.json $p/Nix
sudo cp $p/Nix/main.py $p/Nix/nix
sudo chmod a+rwx $p/Nix/*

