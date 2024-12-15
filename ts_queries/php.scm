[
	(php_tag)
	"?>"
] @tag

; Keywords

[
	"as"
	"catch"
	"clone"
	"const"
	"declare"
	"default"
	"do"
	"echo"
	"finally"
	"fn"
	"function"
	"instanceof"
	"insteadof"
	"interface"
	"match"
	"new"
	"print"
	"use"
	"yield"
	(abstract_modifier)
	(final_modifier)
	(readonly_modifier)
	(static_modifier)
	(visibility_modifier)
] @keyword

[
	"while"
	"if"
	"foreach"
	"for"
	"else"
	"elseif"
	"enddeclare"
	"endfor"
	"endforeach"
	"endif"
	"endswitch"
	"endwhile"
] @logical_keywords

[
	"global"
	"require"
	"require_once"
	"include"
	"include_once"
	"trait"
	"namespace"
	"interface"
	"implements"
	"extends"
	"class"
	(null)
] @command_keywords

[
	"enum"
	"and"
	"xor"
] @numbers

[
	"exit"
	"break"
	"case"
	"return"
	"try"
	"throw"
] @special_chars

[
	"continue"
	"goto"
	"switch"
] @proc_keywords

[
	"("
	")"
	"["
	"]"
	"{"
	"}"
] @parenthesis

"." @delimeter
"->" @delimeter
";" @delimiter

(yield_expression "from" @keyword)
(function_static_declaration "static" @keyword)

; Namespace

(namespace_definition
	name: (namespace_name
	(name) @module))

(namespace_name
	(name) @module)

(namespace_use_clause
	[
	(name) @type
	(qualified_name
		(name) @type)
	alias: (name) @type
	])

(namespace_use_clause
	type: "function"
	[
	(name) @function
	(qualified_name
		(name) @function)
	alias: (name) @function
	])

(namespace_use_clause
	type: "const"
	[
	(name) @constant
	(qualified_name
		(name) @constant)
	alias: (name) @constant
	])

; Variables

(relative_scope) @variable.builtin

(variable_name) @variable

(method_declaration name: (name) @constructor
	(#eq? @constructor "__construct"))

(object_creation_expression [
	(name) @constructor
	(qualified_name (name) @constructor)
])


((name) @constant
 (#match? @constant "^_?[A-Z][A-Z\\d_]+$"))

((name) @upcase
 			(#match? @upcase "^[A-Z_][A-Z_1-9]+$"))

((name) @constant.builtin
 (#match? @constant.builtin "^__[A-Z][A-Z\d_]+__$"))
(const_declaration (const_element (name) @constant))

; Types

(primitive_type) @type.builtin
(cast_type) @type.builtin
(named_type [
	(name) @type
	(qualified_name (name) @type)
]) @type
(named_type (name) @type.builtin
	(#any-of? @type.builtin "static" "self"))

; Functions

(array_creation_expression "array" @function.builtin)
(list_literal "list" @function.builtin)
(exit_statement "exit" @function.builtin "(")

(method_declaration
	name: (name) @function.method)

(function_call_expression
	function: [(qualified_name (name)) (name)] @function)

(scoped_call_expression
	name: (name) @function)

(member_call_expression
	name: (name) @function.method)

(function_definition
	name: (name) @function)

; Member

(property_element
	(variable_name) @property)

(member_access_expression
	name: (variable_name (name)) @property)
(member_access_expression
	name: (name) @property)

; Basic tokens
[
	(string)
	(string_content)
	(encapsed_string)
	(heredoc)
	(heredoc_body)
	(nowdoc_body)
] @string
(boolean) @number
(integer) @number
(float) @number
(comment) @comment

((name) @variable.builtin
 (#eq? @variable.builtin "this"))

"$" @operator

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

((text) @injection.content @html
 (#set! injection.language "html")
 (#set! injection.combined))

((comment) @injection.content
	(#set! injection.language "phpdoc"))

(heredoc
	(heredoc_body) @injection.content
	(heredoc_end) @injection.language)

(nowdoc
	(nowdoc_body) @injection.content
	(heredoc_end) @injection.language)

(namespace_definition
	name: (namespace_name) @name) @module

(interface_declaration
	name: (name) @name) @definition.interface

(trait_declaration
	name: (name) @name) @definition.interface

(class_declaration
	name: (name) @name) @definition.class

(class_interface_clause [(name) (qualified_name)] @name) @impl

(property_declaration
	(property_element (variable_name (name) @name))) @definition.field

(function_definition
	name: (name) @name) @definition.function

(method_declaration
	name: (name) @name) @definition.function

(object_creation_expression
	[
	(qualified_name (name) @name)
	(variable_name (name) @name)
	]) @reference.class

(function_call_expression
	function: [
	(qualified_name (name) @name)
	(variable_name (name)) @name
	]) @reference.call

(scoped_call_expression
	name: (name) @name) @reference.call

(member_call_expression
	name: (name) @name) @reference.call
