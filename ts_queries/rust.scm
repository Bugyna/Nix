(identifier) @variable

((identifier) @upcase
 (#match? @upcase "^[A-Z_][A-Z_]+$"))

(type_identifier) @type
(primitive_type) @type.builtin
(field_identifier) @property

; Identifier conventions

; Assume all-caps names are constants
((identifier) @constant
 (#match? @constant "^[A-Z][A-Z\\d_]+$'"))

; Assume uppercase names are enum constructors
((identifier) @constructor
 (#match? @constructor "^[A-Z]"))

; Assume that uppercase names in paths are types
((scoped_identifier
	path: (identifier) @type)
 (#match? @type "^[A-Z]"))
((scoped_identifier
	path: (scoped_identifier
	name: (identifier) @type))
 (#match? @type "^[A-Z]"))
((scoped_type_identifier
	path: (identifier) @type)
 (#match? @type "^[A-Z]"))
((scoped_type_identifier
	path: (scoped_identifier
	name: (identifier) @type))
 (#match? @type "^[A-Z]"))

; Assume all qualified names in struct patterns are enum constructors. (They're
; either that, or struct names; highlighting both as constructors seems to be
; the less glaring choice of error, visually.)
(struct_pattern
	type: (scoped_type_identifier
	name: (type_identifier) @constructor))

; Function calls

(call_expression
	function: (identifier) @function)

(call_expression
	function: (field_expression
	field: (field_identifier) @function.method))

(call_expression
	function: (scoped_identifier
	"::"
	name: (identifier) @function))

(generic_function
	function: (identifier) @function)
(generic_function
	function: (scoped_identifier
	name: (identifier) @function))
(generic_function
	function: (field_expression
	field: (field_identifier) @function.method))

(macro_invocation
	macro: (identifier) @function.macro
	"!" @function.macro)

; Function definitions

(function_item (identifier) @function)
(function_signature_item (identifier) @function)

(line_comment) @comment
(block_comment) @comment

(line_comment (doc_comment)) @comment.documentation
(block_comment (doc_comment)) @comment.documentation

(type_arguments
	"<" @punctuation.bracket
	">" @punctuation.bracket)
(type_parameters
	"<" @punctuation.bracket
	">" @punctuation.bracket)

"," @punctuation.delimiter
";" @punctuation.delimiter

;;":" @delimeter
"::" @delimeter
"." @delimeter


[
	"("
	")"
	"["
	"]"
	"{"
	"}"
] @parenthesis

(parameter (identifier) @variable.parameter)

(lifetime (identifier) @label)

[
	"impl"
	"struct"
	"fn"
	"mod"
	"move"
	"ref"
	"trait"
	"type"
	"yield"
	"union"
	"dyn"
	"let"
] @keyword
(crate) @keyword
(mutable_specifier) @keyword
(use_list (self) @keyword)
(scoped_use_list (self) @keyword)
(scoped_identifier (self) @keyword)
(super) @keyword

(self) @special_keywords

[
	"false"
	"true"
	"enum"
] @numerical_keywords

((identifier) @numerical_keywords
 (#match? @numerical_keywords "usize"))

[
	"if"
	"else"
	"loop"
	"for"
	"while"
	"continue"
	"break"
	"match"
	"return"
] @logical_keywords

[
	"use"
	"in"
	"as"
	"unsafe"
	"extern"
	"pub"
	"const"
	"where"
] @special_keywords


(self) @variable.builtin

(char_literal) @string
(string_literal) @string
(raw_string_literal) @string

(boolean_literal) @constant.builtin
(integer_literal) @constant.builtin
(float_literal) @constant.builtin

(escape_sequence) @escape

(attribute_item) @attribute
(inner_attribute_item) @attribute

[
	"-"
	"-="
	"!="
	"*"
	"*="
	"/"
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
	"="
	"=="
	">"
	">="
	">>"
	">>="
	"|"
	"|="
	"&&"
	"||"
	"!"
	"^"
	"'"
	":"
] @operator

; ADT definitions

(struct_item
	name: (type_identifier) @name) @definition.class

(enum_item
	name: (type_identifier) @name) @definition.class

(union_item
	name: (type_identifier) @name) @definition.class

; type aliases

(type_item
	name: (type_identifier) @name) @definition.class

; method definitions

(declaration_list
	(function_item
		name: (identifier) @name)) @definition.method

; function definitions

(function_item
	name: (identifier) @name) @definition.function

; trait definitions
(trait_item
	name: (type_identifier) @name) @definition.interface

; module definitions
(mod_item
	name: (identifier) @name) @definition.module

; macro definitions

(macro_definition
	name: (identifier) @name) @definition.macro

; references

(call_expression
	function: (identifier) @name) @reference.call

(macro_invocation
	macro: (identifier) @name) @reference.call @function.method

; implementations

(impl_item
	trait: (type_identifier) @name) @reference.implementation

(impl_item
	type: (type_identifier) @name
	!trait) @reference.implementation