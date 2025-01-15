# Themes

## theme_conf.json

- this file holds information about all available themes
- you can create new ones by simply updating the file

### structure

- individual themes are split into two separate contexts

### window

- the window context holds information about basic default background, foreground colors of the window
- `bg` is for the background of the whole window
- `fg` is for the foreground(default text color) of the whole window
- `insertbg` is the cursor color
- `selectbg` is for the color of background color of selection(when selecting text)
- `selectfg` is for the text color of selected text
- `line_numbers` is for the color of line numbers
	- for `widget_fg`, `select_widget`, `select_widget_fg` refer to the widgets documentation and buffer_tab theme configurations


### highlighter

- holds information about how text should be highlighted
- the options here can be a bit more extensible compared to the `window` context
- what you specify are `tags` that can be of the form:
	- `"name": "#COLOR_CODE"` eg. `"pair": "#0000FF"
		- this is the simplest tag configuration there is and specifies just the foreground color of text highlighted with this tag

	- `"name": "{"option": "Value", "option2": True}` eg. `"pair": "{"background": #990000", "bold": true}"`
		- this is the extend version
		- all options you can use are:
			- `"background": "#color_code"`
			- `"foreground": "#color_code"`
			- `"bold": True|False`
			- `"underline": True|False`

	- tags you can specify are
		- *For information about which tags are used for which keywords you can look into `ts_queries/[lang].scm`, the keywords are usually captured by the @[tag_name] which should mostly match the tags listed below*
		- `keywords` which are mostly used general keywords(like types)
		- `logical_keywords` which are mostly used for keywords that have something to do with control flow(if, switch, goto, for, etc.)
		- `command_keywords` (in theme_conf) or `special_keywords`(in the tree_sitter queries) which are mostly used for various modifiers(const, volatile, static, register)
		- `functions` which are used for functions(defintions and callls)
		- `upcase` which are mostly used for words written in UPPER_CASE
		- `numbers` which are used for numbers and numerical keywords(things like NULL, enum, signed, unsigned)
		- `operators` which are used for operators (again refer to the tree_sitter queries as stated above for more info) as what an operator is can wildy differ from language to language and my personal whims
		- `special_chars` which are used for parenthesis and special characters(similar situation as operators)
		- `quotes` which are used for literal string values and things of that sort
			- string formattting in various languages can be captured and highlighted differently to the rest of the string and is usually highlighted with the `special_keywords` tag
		- `comments` which are for comments
		- `pair` which is for highlighting matched bracket pair
		- `found` which is for highlighting matched words when searching in text
		- `command_out_select` which is for highlighting selected text in the COMMAND_OUT widget
		- `error` which is supposed to be for errors but is generally unused I think

		
		


