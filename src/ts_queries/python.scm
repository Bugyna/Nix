; Identifier naming conventions

(identifier) @variable

((identifier) @constructor
 (#match? @constructor "^[A-Z]"))

((identifier) @upcase
 (#match? @upcase "^[A-Z_][A-Z_]+$"))

((identifier) @constant
 (#match? @constant "^[A-Z][A-Z_]*$"))

((identifier) ("." (identifier))) @special_keywords

; Function calls

(decorator) @special_keywords

(call
	function: (attribute attribute: (identifier) @function.method))
(call
	function: (identifier) @function)

; Builtin functions

((call
	function: (identifier) @function.builtin)
 (#match?
	 @function.builtin
	 "^(abs|all|any|ascii|bin|bool|breakpoint|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip|__import__)$"))

; Function definitions

(function_definition
	name: (identifier) @function)

(attribute attribute: (identifier) @property)
(type (identifier) @type)

; Literals

[
	(none)
	(true)
	(false)
] @constant.builtin

[
	(integer)
	(float)
] @number

(comment) @comment
(string) @string
(escape_sequence) @escape

(interpolation
	"{" @punctuation.special
	"}" @punctuation.special) @embedded

(interpolation
	"{" @punctuation.special
	"}" @punctuation.special) @special_keywords

[
	"-"
	"-="
	"!="
	"*"
	"**"
	"**="
	"*="
	"/"
	"//"
	"//="
	"/="
	"&"
	"&="
	"%"
	"%="
	"^"
	"^="
	"+"
	"->"
	"+="
	"<"
	"<<"
	"<<="
	"<="
	"<>"
	"="
	":="
	"=="
	">"
	">="
	">>"
	">>="
	"|"
	"|="
	"~"
	"@="
] @operator

[
	"and"
	"in"
	"is"
	"not"
	"or"
	"while"
	"with"
	"import"
	"elif"
	"else"
	"for"
	"from"
	"if"
] @logical_keywords

[
	"("
	")"
	"["
	"]"
	"{"
	"}"
	"~"
	"@"
] @parenthesis


[
	"as"
	"assert"
	"async"
	"await"
	"break"
	"def"
	"del"
	"except"
	"finally"
	"nonlocal"
	"pass"
	"print"
	"raise"
	"try"
	"match"
	"case"
] @keyword

[
	"continue"
	"class"
	"exec"
	"global"
	"lambda"
	"yield"
	"return"
] @special_keywords
