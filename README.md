# NNIX

## Spec
Text editor for programmers using tkinter, tree_sitter, pexpect

Supports syntax highlighting for languages using tree sitter(by default: python, C(++), HTML, PHP, rust)

Has various themes (see [screenshots](docs/README.md))

Has pretty much anything you'd expect from a simple text editor, you can edit files, comment lines, run some commands and see their outputs, (regex and normal)search and replace

It's configurable, you can set your own keybinds and configure some parts of how the editor looks

If you dare you can create your own themes by editing [the theme config](src/theme_conf.json)


## Usage

python3 main.py [filename(s)]

python3 src/main.py [filename(s)]


## installation

not necessary but do run `pip3 install -r requirements.txt`


## Docs

### Keybinds

see [keybinds](docs/keybinds.md) or look at keybind config [keybind config](src/keybind_conf.json)


### Themeing

see [themes](docs/themes.md) or look at theme config [theme conf](src/theme_conf.json)


### Configuration

see [config](docs/conf.md) and look at [the actual config file](src/conf)


### Showcase

see [showcase and screenshots](docs/README.md)


## Programmer docs

[Plugins](docs/plugins.md)

[Language support](docs/highlighting.md) also see [lexer.py](src/lexer.py) and [tree sitter queries](src/ts_queries)

[Custom widgets](docs/widget.md) also see [widgets.py](src/widgets.py)

[Non widgets](docs/arch.md)
