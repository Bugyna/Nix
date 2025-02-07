(tag_name) @tag @keyword
(erroneous_end_tag_name) @tag.error
(doctype) @constant @logical_keywords
(attribute_name) @attribute
(attribute_value) @string
(comment) @comment

[
	"'"
	"\""
] @string

[
	"="
] @operator

[
	"<"
	">"
	"</"
	"/>"
] @punctuation.bracket @parenthesis

((script_element
	(raw_text) @injection.content)
 (#set! injection.language "javascript"))

((style_element
	(raw_text) @injection.content)
 (#set! injection.language "css"))
