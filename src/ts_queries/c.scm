(identifier) @variable

((identifier) @constant
 (#match? @constant "^[A-Z][A-Z\\d_]*$"))

((identifier) @upcase
 (#match? @upcase "^[A-Z_][A-Z_1-9]+$"))

[
	"switch"
	"case"
	"if"
	"else"
	"goto"
	"for"
	"while"
	"continue"
	"break"
	"do"
] @logical_keywords

[
	"enum"
	"NULL"
	"signed"
	"unsigned"
] @numerical_keywords

[
	"asm"
	"__attribute__"
	"const"
	"extern"
	"volatile"
	"typedef"
	"static"
	"register"
] @special_keywords

"#define" @keyword
"#elif" @keyword
"#else" @keyword
"#endif" @keyword
"#if" @keyword
"#ifdef" @keyword
"#ifndef" @keyword
"#include" @keyword
(preproc_directive) @keyword

"--" @operator
"-" @operator
"-=" @operator
"->" @operator
"=" @operator
"!=" @operator
"*" @operator
"&" @operator
"&&" @operator
"+" @operator
"++" @operator
"+=" @operator
"<" @operator
"==" @operator
">" @operator
"||" @operator

"." @delimeter
"->" @delimeter
";" @delimiter

[
	"("
	")"
	"["
	"]"
	"{"
	"}"
	"~"
] @parenthesis

(string_literal) @string
(system_lib_string) @string

(null) @constant
(number_literal) @number
(char_literal) @number

(field_identifier) @property
(statement_identifier) @label
(type_identifier) @type
(primitive_type) @type
(sized_type_specifier) @type

(call_expression
	function: (identifier) @function)
(call_expression
	function: (field_expression
	field: (field_identifier) @function))



(function_declarator
	declarator: (identifier) @function)
(preproc_function_def
	name: (identifier) @function.special)

(comment) @comment

(struct_specifier name: (type_identifier) @name body:(_)) @definition.class

(declaration type: (union_specifier name: (type_identifier) @name)) @definition.class

(function_declarator declarator: (identifier) @name) @definition.function

(type_definition declarator: (type_identifier) @name) @definition.type

(enum_specifier name: (type_identifier) @name) @definition.type

((identifier) ("." (identifier))) @special_keywords