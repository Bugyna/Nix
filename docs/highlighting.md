# LEXER/HIGHLIGHTER

## ADDING LANGUAGE SUPPORT

- Adding a language for highlighting is pretty easy as you just have to download the proper `tree-sitter` package with the correct grammar adding queries you'd like and renaming some of the capture names in the query file to the ones supported by this highlighter, and then adding a bunch of `if-else` statements to `lexer.py` so the correct configuration loads for the correct language
- Do not fret there is a slight tutorial for this
- First I will go over adding the config loading in `lexer.py`


## Modifying lexer.py

- To add support for your language of choice you will have to modify the `LEXER` class in `lexer.py`
#### - Importing the grammar
- At the start of the file import your grammar
- e.g `import tree_sitter_python as tspython`
- Then construct the `tree_sitter.Language`
- `PYTHON_LANGUAGE = tree_sitter.Language(tspython.language())`
- that's it for this part

#### - Next you want to modify `LEXER.set_language(self, lang_type)`

- Again pretty much the same
- You will check for you lang_type(which is the extension of the file usually) (so for `main.py` it's the `py` part, `main.pyw` -> `pyw`)
- There's sometimes many extensions for one language so just put them all in a list
- Here you can specify:
	- `build_argv` which is a variable that refers to what action should be done when running `TEXT.make`, which is a function that can be bound as keyboard shortcut (the default keybind is `<Shift-Enter>`)
	- So for the C language you want to set it to `make` and it will run the `make` command in the command line
	- For rust it might be `cargo build` etc.
	- `run_argv` is similar, but you can set it to a command that runs some command that runs your project(this can again be bound as a keyboard shortcut) (the default keybind is `<Control-Enter>`)
	- So for C you might want to run a specific executable `./main`
	- Or something like `cargo run` for rust
	- YOU SHOULD ALSO SET THE COMMENTS SIGN(S) YOUR LANGUAGE USES
	- you can set `self.comment_sign` which is for the single line comment sign
	- `//` for C or `#` for python
	- you can set `self.multiline_comment_sign` which is for the start sign of a multiline comment
	- `/*` for C or `<!--` for HTML
	- you can set `self.multiline_comment_sign_end` which is for the end sign of a multiline comment
	- `*/` for C or `-->` for HTML
	- IN CASE YOUR LANGUAGE ONLY USES MULTILINE COMMENT SIGNS YOU CAN SET `self.force_multiline_comment=True` WHICH FORCES MULTILINE COMMENTS (THE DEFAULT OPTION IS TO USE SINGLE LINE COMMENTS FOR EVERYTHING)
	- IN CASE YOUR LANGUAGE USES TREE-SITTER INJECTIONS(LIKE PHP FOR EXAMPLE) YOU CAN SET CREATE ANOTHER LEXER FOR THE INJECTION LANGUAGE(WHICH ALSO OF COURSE REQUIRES IMPORTING THE PROPER TREE-SITTER GRAMMAR ETC.)
	- To specify an injection lexer/parser you create language and query through `LEXER.construct_lang_and_query(self, lang_type)` (we will go over this function later)
	then you create a `tree_sitter.Parser(tree_sitter.Language)` and add it to `self.active_lexers: Dict[str, [tree_sitter.Parser, tree_sitter.Query, tree_sitter.Language]]`
	- e.g
	```
	elif (lang_type == "php"):
		l, q = self.construct_lang_and_query('html')
		p = tree_sitter.Parser(l)
		# p.set_language(l)
		self.active_lexers['html'] = [p, q, l]
	```
	- you might have to modify the query file in order to properly name the injection content capture to match the key in `self.active_lexers`, but we'll go over that later
		

#### - Modifying `LEXER.construct_lang_and_query(self, lang_type)`

- This function is responsible for loading the language(s) and quer(y/ies) (we will go over queries later)
- The lang_type should be a string, but you can pass it a list(it will take the first element of the list)
- Then you will add an `if/elif` somewhere in the decision tree and check for the lang_type you want to pass
```
elif (lang_type == "py"):
	language = PYTHON_LANGUAGE
		with open(f"{SOURCE_PATH}/ts_queries/python.scm", "r") as file:
			query = language.query(file.read())
```
- As you surely remember `PYTHON_LANGUAGE` is the object we constructed before
- Here you will want to modify the path you load your queries from
```
elif (lang_type == "{your language type}"):
	language = {The language you constructed at the start of the file}
		with open(f"{SOURCE_PATH}/ts_queries/{name of your query file}.scm", "r") as file:
			query = language.query(file.read())
```
- That's it

#### - Queries

- Queries are bundled with tree_sitter grammars in their respective repos on [github](https://github.com/tree-sitter/)
- in the `queries` folder
- There is a bunch of files usually so I just put them into one big filed named `[lang].scm` in the `ts_queries` folder

##### - Captures
- If you look at the query file you will see usually a string or a list of strings and names starting with the `@` sign after that, these are basically types of the the string or list of strings being matched
- Simply put tree-sitter looks for the strings in quotes and if it finds a match, it puts the type and location of the match in our parser's results and we work with it afterwards
- Our highlighter can manage these captures by default: (cannot manage every single one possible capture because the people writing these queries usually name things differently (for example, `function_declaration` vs `function_definition` etc.)
	- `@keyword`, `@function`, `@operator`, `@string`, `@function.method`, `@number`, `@comment`, `@parenthesis`, `@special_chars`, `@delimeter`, `@tag`, `@upcase`, `@type`, `@type_parameters`, `@special_keywords`, `@command_keywords`,  `@attribute`, `@proc_keywords`, `@logical_keywords`, `@numerical_keywords`, `@constant.builtin`
- So if you copy a query file somewhere and put it in the `ts_queries` dir and one of the captures is named `@function.declaration` and you want it to be highlighted as the other functions simply rename it to `function`
- You can also move around these captures to highlight them with different colors if you wish
- for example in these preprocessor directives would get highlighted as keywords:
	```
	"#define" @keyword
	"#elif" @keyword
	"#else" @keyword
	"#endif" @keyword
	"#if" @keyword
	"#ifdef" @keyword
	"#ifndef" @keyword
	"#include" @keyword
	(preproc_directive) @keyword
	```
- but you might want them to be highlighted the same way as constants written in UPPERCASE so you can rename them to:
	```
	"#define" @upcase
	"#elif" @upcase
	"#else" @upcase
	"#endif" @upcase
	"#if" @upcase
	"#ifdef" @upcase
	"#ifndef" @upcase
	"#include" @upcase
	(preproc_directive) @upcase
	```
- for more information on how to deal with these queries please consult the tree-sitter docs
