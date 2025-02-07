# OLD LEXER

before using tree sitter we used a homebrewed lexer, which you can still use

### HOW?

- rename `src/lexer.py` to something else
- rename `src/old_lexer.py` to `lexer.py`
- that's it


the homebrewed lexer only supports highlighting for C(++) languages really, you can use it on others, but it's gonna look off and the actual lexing for the autocomplete features is not going to work properly

highlighting for other langauges has been lost to time and refactoring( rip `highlighter.py` you still exist, but your entire concept was wrong)