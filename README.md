# NNIX

## Spec
Text editor for programmers using tkinter, tree_sitter, pexpect

Supports syntax highlighting for languages using tree sitter(by default: python, C(++), HTML, PHP, rust)

Has various themes (see [screenshots](docs/README.md))

Has pretty much anything you'd expect from a simple text editor, you can edit files, comment lines, run some commands and see their outputs, (regex and normal)search and replace

It's configurable, you can set your own keybinds and configure some parts of how the editor looks

If you dare you can create your own themes by editing [the theme config](src/theme_conf.json)


## ONLY WORKS ON LINUX
- because of `python-magic`, which can on windows be patched with `python-magic-bin`
- because of pexpect

## Usage

requires >=python3.10 (because of tree-sitter, they like breaking backwards compatibility)
if you have an older version of python <python3.10, check out [switching to the older lexer](docs/old_lexer.md)

python3 main.py [filename(s)]

python3 src/main.py [filename(s)]


## installation

not necessary but do run `pip3 install -r requirements.txt`


## Docs

### Keybinds

see [keybinds](docs/keybinds.md) or look at keybind config [keybind config](src/keybind_conf.json)


### Commands

see [command entry](docs/command_entry.md)

### Themeing

see [themes](docs/themes.md) or look at theme config [theme conf](src/theme_conf.json)


### Configuration

see [config](docs/conf.md) and look at [the actual config file](src/conf)


### Showcase

see [showcase and screenshots](docs/README.md)


## Programmer docs

You will need to understand (tk)inter first, so read the docs for that first(there's a bunch of them these are my favourite)
- [anzeljg @New Mexico Tech](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html)
- [epydoc](https://epydoc.sourceforge.net/stdlib/Tkinter-module.html)
- [atsushi @kyoto](https://www.cc.kyoto-su.ac.jp/~atsushi/Programs/VisualWorks/CSV2HTML/CSV2HTML_PyDoc/Tkinter.html)

[Plugins](docs/plugins.md)

[Language support](docs/highlighting.md) also see [lexer.py](src/lexer.py) and [tree sitter queries](src/ts_queries)

[Custom widgets](docs/widget.md) also see [widgets.py](src/widgets.py)

[Non widgets](docs/arch.md)
