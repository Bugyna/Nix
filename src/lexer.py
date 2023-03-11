import string
import re
import os
import threading

# how is this any more readable
az         = string.ascii_letters + "_"
num        = string.digits
alphanum   = az + num
whitespace = " \t"
operators = "+-*/"
logic_operators = "!=<>"
brackets = "()[]{}"
left_brackets = "([{"
right_brackets = ")]}"
colon = ":"
semicolon = ";"
dot = "."
comma = ","
single_quote = "'"
double_quote = "\""
hashtag = "#"


class EMPTY_LEXER():
	def __init__(self, parent, txt):
		self.parent = parent
		self.buffer = txt

	def lex(self, text=None):
		pass

class RLEXER:
	def __init__(self, parent, txt):
		self.parent = parent
		self.buffer = txt

		self.word: str = ""
		self.last_word: str = ""
		self.index: int = 0
		self.char: str = ""
		self.offset = 0
		self.max_length: int = 0
		self.tokens = []

	def lex(self, text=None):
		if (text): self.text = text+" "
		else: self.text = self.buffer.get("1.0", "end")
		self.max_length = len(text)
		left_bracket_count = 0

		# for char in self.text:
		while (self.index < self.max_length):
			self.char = self.text[self.index]
			self.next_char = self.text[self.index+1]

			if (self.char in az):
				if (self.check_word_for_type(az+num)):
					self.destroy_word()

				self.word += self.char

			elif (self.char in operators):
				self.destroy_word()
				self.word = self.char
				if (self.char == "/" and self.next_char == "/"):
					self.word = self.char + self.next_char
					self.destroy_word()
					self.index += 1

			elif (self.char in logic_operators):
				if (self.next_char in logic_operators):
					self.destroy_word()
					self.word = self.char + self.next_char
					self.destroy_word()
					self.index += 1
				else:
					self.destroy_word()
					self.word = self.char
					self.destroy_word()
					

			elif (self.char in num):
				if (self.last_char == dot):
					pass


				elif (self.check_word_for_type(az+num)):
					self.destroy_word()

				self.word += self.char

			elif (self.char in brackets):
				if (self.char in right_brackets):
					left_bracket_count -= 1

				else:
					left_bracket_count += 1

				self.destroy_word()
				self.word = self.char
				self.destroy_word()

			elif (self.char in whitespace):
				self.destroy_word()

			elif (self.char == semicolon):
				self.destroy_word()
				self.word = self.char
				self.destroy_word()

			elif (self.char == colon):
				self.destroy_word()
				self.word = self.char
				self.destroy_word()

			elif (self.char == single_quote):
				self.destroy_word()
				self.word = self.char
				self.destroy_word()

			elif (self.char == double_quote):
				self.destroy_word()
				self.word = self.char
				self.destroy_word()

			elif (self.char == hashtag):
				self.destroy_word()
				self.word = self.char
				self.destroy_word()

			elif (self.char == dot):
				if (self.last_char in num):
					self.word += self.char

				else:
					self.destroy_word()
					self.word += self.char
					self.destroy_word()

			elif (self.char == comma):
				self.destroy_word()
				self.word = self.char
				self.destroy_word()
				
			elif (self.char in "\r\n"):
					if (self.char == "\n" and self.next_char == "\r"):
						self.destroy_word()
						self.word = self.char + self.next_char
						self.destroy_word()

					else:
						self.destroy_word()
						self.word = self.char
						self.destroy_word()

			self.index += 1
			self.last_char = self.char


	def check_word_for_type(self, type):
		for char in self.word:
			if (char not in type):
				return True

		return False

	def destroy_word(self):
		if (self.word):
			if (self.word != "\n"): print(self.word)
			self.tokens.append(self.word)
			self.last_word = self.word
			self.word = ""


class PARSER:
	def __init__(self, tokens):
		self.tokens = []

	def parse(self):
		pass

def run_test():
	text = r"""

#pragma once
#include "engine.h"

// typedef enum move_state move_state;


typedef struct Entity Entity;
typedef struct Animator Animator;
typedef struct Vec2 Vec2;
typedef struct Vec3 Vec3;
typedef struct Body Body;

enum move_state
{
	not_moving = 0,
	moving,
	accelerating,
	deccelerating,
	jumping,
	falling,
	
};

struct Vec2
{
	float x, y;
};

struct Vec3
{
	float x, y, z;
};

struct Body
{
	float x, y, w, h, z, d;
};

struct Animator
{
	Entity* parent;
	void (*animate)(Animator*);
	Body render_rect;
	uint32_t frame, offset_x, offset_y, fraction, max;
};

struct Entity
{
	Body rect;
	SDL_Texture* sprite;
	uint32_t state;
	int32_t dx, dy, vel;
	uint8_t direction; // 1 = left, 0 = right
	Animator animator;
	uint32_t delta_time; 
	
};

// void entity_init(

void animator_init(
	Entity* entity, Animator* animator, void (*func)(Animator*),
	uint32_t offset_x, uint32_t offset_y, uint32_t fraction, uint32_t max
	)
{
	animator->parent = entity;
	animator->animate = *func;
	animator->render_rect = (Body){9, 20, 15, 15, 0, 0};
	animator->frame = 0;
	animator->offset_x = offset_x;
	animator->offset_y = offset_y;
	animator->fraction = fraction;
	animator->max = max;
}

void animate(Animator* animator)
{
	uint32_t ticks = SDL_GetTicks();

	if (animator->parent->state == not_moving) {
		animator->render_rect.y = 20;
		animator->max = 4;
	}
	else if (animator->parent->state == moving) {
		animator->render_rect.y = 20+5*(animator->offset_y);
		animator->max = 8;
	}

	animator->frame = ticks / animator->fraction % animator->max;
	// animator->render_rect.x = 9+animator->frame*(animator->offset_x+animator->render_rect.w);
	animator->render_rect.x = 9+animator->frame*animator->offset_x;
}


SDL_Rect convert_body_to_rect(Body body)
{
	return (SDL_Rect){body.x, body.y, body.w, body.h};
}

void screen_blit(SDL_Renderer* renderer, SDL_Texture* texture, Body* render_rect, Body* rect, int angle, int something, int direction)
{
	SDL_Rect src = convert_body_to_rect(*render_rect);
	SDL_Rect dst = convert_body_to_rect(*rect);
	SDL_RenderCopyEx(renderer, texture, &src, &dst, angle, NULL, direction);
}





"""
	
	lexer = RLEXER(None, None)
	lexer.lex(text)
	print(lexer.tokens)


if __name__ == "__main__":
	run_test()

class LEXER:
	def __init__(self, parent, txt):
		self.parent = parent
		self.buffer = txt
		self.defines = {}
		self.function_regex = re.compile(r"(([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]+)*([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*[\[\]\*]*[\ \t]+))([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*)(\((.*\n*)*\))")

		# unsigned int eq(int a, int b) 
		# {
		#	return (unsigned int)(a == b);
		# }	

		# = type: unsigned int
		# name: eq
		# parameters: int a int b
		# local: None

		self.index = 0

		self.types = []
		self.modifiers = []
		self.keywords = ["if", "else", "while", "switch", "case"]
		self.vars = []
		self.functions = []
		self.objects  = []
		self.scopes  = {}

		self.identifier = r"\b[a-zA-Z_]+[a-zA-Z_0-9_]*\b"
		self.statement = {
			"keywords" : r"\b(for|while|if|else|case|switch|do|elif)",
			"rule" : "newline",
		}

	def lex(self, text=None):
		# should iterate through characters make a token and then parse the token
		# I should probably just use tree sitter or something though
		if (text): self.text = text
		else: self.text = self.buffer.get("1.0", "end")
		self.row_index = 1
		self.column_index = 0


		self.in_whitespace = False
		self.in_comment = False
		self.line = ""
		self.prev_word = ""
		self.word = ""
		self.last_char = ""

		for self.index, char in enumerate(self.text, 0):
			if (self.in_comment):
				if (char == "\n"): self.in_comment = False
				else: continue

			if (self.in_whitespace):
				if (char not in whitespace):
					self.in_whitespace = False
					self.handle_separator()
					
			elif (char in whitespace):
				self.in_whitespace = True
				continue

			if (char == "\n"):
				self.handle_separator()

			elif ((not self.word and char in az) or (self.word and char in alphanum)):
				if (self.in_whitespace): self.in_whitespace = False; self.handle_separator()
				self.word += char

			elif (char == "="):
				self.make_var()

			elif (char == "("):
				self.make_function()

			elif (char in ["[", "]", "{", "}", ")", ";"]):
				self.prev_word = self.word = ""

			self.last_char = char
			# print("prev: ", self.prev_word, "word: ", self.word)

	def handle_separator(self):
		if (self.word == ""):
			return
		else:
			# print(f"word: {self.word} ({self.prev_word})")
			self.prev_word = self.word
			self.word = ""

	def make_var(self):
		# if (re.match(r"[a-zA-Z_][0-9_]+", self.prev_word) and re.match(r"[a-zA-Z_][0-9_]+", self.prev_word)):
		# w = f"{self.word} ({self.prev_word})"
		w = self.word
		# print("making var: ", w)
		if ((w not in self.vars) and (self.word not in self.keywords)):
			self.vars.append(w)

	def make_function(self):
		# w = f"{self.word} ({self.prev_word})"
		w = self.word
		# print("making func: ", w)
		if ((w not in self.functions) and (self.word not in self.keywords)):
			self.functions.append(w)

	# def check_keyword(self):
		# return self.word in self.keywords

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objects)
		print("VARS: ", self.vars)

		s = "FNCS: \n"
		for word in self.functions:
			s += "\t"+word+"\n"

		s += "OBJS: \n"
		for word in self.objects:
			s += "\t"+word+"\n"

		self.parent.command_out_set(s)




class PY_LEXER(LEXER):
	""" basic lexing """
	def __init__(self, parent, txt):
		super().__init__(parent, txt)

	def lex(self, text=None):
		if (text): self.text = text
		else: self.text = self.buffer.get("1.0", "end-1c")
		row_index = 1
		char_index = 0

		in_comment = False
		
		brackets = {
			"(": 0,
			"[": 0,
			"{": 0,
		}

		line = []
		prev_word = ""
		word = ""
		expr = ""
		in_quote = in_quote_ = False

		for self.index, char in enumerate(self.text, 0):
			if (in_comment):
				if (char == "\n"): in_comment = False
				else: continue 

			elif (in_quote or in_quote_):
				expr += char
				self.index += 1
				if (in_quote and char == "\""):
					in_quote = False
					word_count = 0
					continue

				elif (in_quote_ and char == "'"):
					in_quote_ = False
					word_count = 0
					continue

				else:
					continue

			if (char == " " or char == "\t"):
				# self.make_func(prev_word, word, expr)
				line.append(word)
				prev_word = word
				word = ""
				expr += " "
				
			elif (char == "\n"):
				# self.make_func(prev_word, word, expr)
				line = []
				prev_word = ""
				word = ""
				expr = ""
				
				row_index += 1
				char_index = 0
				continue

			elif (char == "\""):
				in_quote = not in_quote
				self.index += 1
				expr += char
				continue

			elif (char == "'"):
				in_quote_ = not in_quote_
				self.index += 1
				expr += char
				continue

			elif (char == "#"):
				in_comment = True

			elif (char in az):
				word += char
				expr += char

			elif (word and char in num):
				word += char
				expr += char


			elif (char in ")]}"):
				expr += char
				if (char == ")"):
					self.make_func(prev_word, word, expr)

				expr = ""
				prev_word = word
				word = ""


			elif (char in ("(", "[", "{")):
				# brackets[char] = brackets[char]+1
				expr += char
				# if (char == "("):
					# self.make_func(prev_word, word)

				prev_word = word
				word = ""

			elif (char == "."):
				line.append(word)
				word = ""
				expr += char

			elif (char == ","):
				expr += char
				
			elif (char == "="):
				expr += char
				self.make_var(prev_word, word, expr)

				word = ""
				prev_word = word

			elif (char == ":"):
				expr += char
				if (self.text[self.index+1] == "\n"): self.make_func(prev_word, word, expr)
				expr = ""

			# elif (char in (")", "]", "}")):
				# brackets[char] = brackets[char]-1

			char_index += 1

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objects)
		print("VARS: ", self.vars)

	def make_func(self, prev_word, word, expr):
		if (re.search("def", expr)):
			# expr = re.sub("\s+", " ", expr)
			# group 1 is the full type
			# group 3 is the last part of the type
			# group 4 is the function name
			# group 5 are parameters
			expr = expr.strip()
			# print(expr)
			m = self.function_regex.match(expr)
			# m = re.match(r"(([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]+)*([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*[\[\]\*]*[\ \t]+))([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*)(\((.*\n*)*\))", expr)
			# print(m)
	
			if (m):
				x = ('', m.group(4), m.group(5))
				# print(m.groups())
				if (m.group(4) not in self.defines):
					self.defines[m.group(4)] = x
					self.functions.append(m.group(4))

		elif (prev_word == "class" or prev_word == "import"):
			self.objects.append(word)

	def make_var(self, prev_word, word, expr):
		pass
		# if (self.text[self.index+1] != "="): self.vars.append(word)


class C_LEXER(LEXER):
	def __init__(self, parent, txt):
		super().__init__(parent, txt)
		self.indexed_files = []

	def lex(self, text=None, file=""):
		if (text): self.text = text
		else: self.text = self.buffer.get("1.0", "end-1c")
		self.file_queue = []
		
		row_index = 1
		char_index = 0
		in_comment = False
		in_multiline_comment = False
		in_quote = False # "
		in_quote_ = False # '
		
		brackets = {
			"(": 0,
			"[": 0,
			"{": 0,
		}

		line = []	
		prev_word = ""
		word = ""

		self.index = 0
		last_index = ""
		index = ""
		word_count = 0
		expr = ""
		flag = 0
		prev_char = ""
		# print("length: ", len(self.text), file)
		
		# for self.index in range(len(self.text)-1):
		while (self.index < len(self.text)-1):
			# if (flag): print("FLAG: ", char, self.index); flag = 0
			prev_char = self.text[self.index-1]
			char = self.text[self.index]
			if (in_comment):
				if (char == "\n"):
					in_comment = False
					word_count = 0

				else: self.index += 1; continue

			elif (in_multiline_comment):
				if (char == "*" and self.text[self.index+1] == "/"):
					in_multiline_comment = False
					word_count = 0
					self.index += 2
					continue

				else: self.index += 1; continue


			elif (in_quote or in_quote_):
				expr += char
				self.index += 1
				if (in_quote and char == "\""):
					in_quote = False
					word_count = 0
					continue

				elif (in_quote_ and char == "'"):
					in_quote_ = False
					word_count = 0
					continue

				else:
					continue
				

			if (char == " " or char == "\t"):
				# if (self.text[self.index+1] == "="): self.make_var(prev_word, word, index=self.index+1)
				if (self.search_whitespace(self.index+1)):
					line.append(word)
					prev_word = word
					word_count += 1
					word = ""
					if (expr): expr += " "

			elif (char == ","):
				line.append(word)
				prev_word = word
				word = ""
				expr += char

			elif (char == "\""):
				in_quote = not in_quote
				self.index += 1
				continue

			elif (char == "'"):
				in_quote_ = not in_quote_
				self.index += 1
				continue
				
			elif (char == "\n"):
				# if (prev_word and prev_word[0] == "#"):
					# prev_word = word
					# word = ""

				row_index += 1
				char_index = 0
				if (expr): expr += "\n"
				self.index += 1
				continue

			elif (char == "/"):
				if (self.text[self.index+1] == "/"):
					in_comment = True

				elif (self.text[self.index+1] == "*"): in_multiline_comment = not in_multiline_comment

			elif (prev_char == "\n" and char == "#"):
				word = ""
				self.handle_preprocessor()
				flag = 1
				# print("preproc: ", self.index)

			elif (char in az):
				word += char
				expr += char

			elif (word and char in num):
				word += char
				expr += char

			elif (char in "+-=|<>./?:*%^&!~"):
				expr += char

			elif (char in "([{"):
				brackets[char] = brackets[char]+1
				expr += char

			elif (char in ")]}"):
				# brackets[char] = brackets[char]-1
				# if (char == "(" or char == "{"):
				expr += char
				if (char == ")"):
					# self.make_func(prev_word, word)
					self.make_func_new(expr)
					expr = ""
				elif (char == "}"):
					expr = ""

				prev_word = word
				word = ""

			elif (char == "."):
				line.append(word)
				word = ""
				expr += char

			elif (char == "="):
				self.make_var(prev_word, word)
				expr += char

				word = ""
				prev_word = word

			elif (char in ";:"):
				word_count = 0
				expr = ""

				
			char_index += 1
			self.index += 1
			# print("i: ", self.index, char, word, file)


		# print("lexing ended")

		for object in self.objects:
			if (object not in self.buffer.highlighter.keywords): self.buffer.highlighter.keywords.append(object)
	
			# self.parent.command_out_set("lex finished")
	
		# file_queue += self.file_queue.copy()
		# print("file Q: ", file_queue)

		for file in self.file_queue:
			if (file not in self.indexed_files):
				self.indexed_files.append(file)
				# self.parent.command_out_set(f"file {file} is a file")
				path = f"{os.path.dirname(self.buffer.full_name)}/{file}"
				if (os.path.isfile(path)):
					# print(path)
					f = open(path, "r")
					self.lex(f.read(), path)
					f.close()
				else:
					path = f"/usr/include/{file}"
					# print("dwaw: ", path)
					if (os.path.isfile(path)):
						f = open(path, "r")
						self.lex(f.read(), path)
						f.close()

		# self.print_res()

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objects)
		print("VARS: ", self.vars)

		s = "FNCS: \n"
		for word in self.functions:
			s += "\t"+word+"\n"

		s += "OBJS: \n"
		for word in self.objects:
			s += "\t"+word+"\n"

		self.parent.command_out_set(s)


	def handle_preprocessor(self):
		word = ""
		command = ""
		ignore_next = False
		i = 1
		for char in self.text[self.index+i:]:
			if ((not command or command == "include") and char in az or char == "/" or char == "\\" or char == "."):
				word += char

			elif (command == "define" and char != "\\"):
				word += char

			elif (command == "ignore"):
				pass
			
			# print(f"[{word}]")
			
			if (char == " " and not command and word):
				# print("dwawd", f"[{word}]", char)
				if (word == "include" or word == "define"):
					command = word
					word = ""
				else: command = "ignore"

			elif (not ignore_next and char == "\\"):
				ignore_next = True

			elif (ignore_next):
				ignore_next = False

			elif (char == "\n" and not ignore_next):
				break

			i += 1

		# self.parent.command_out_set(f"file {word} was added to queue")

		# print("end: ", command, word, i)
		self.index += i
		if (command == "include" and word not in self.indexed_files): self.file_queue.append(word)
		elif (command == "define"):
			x = self.parse_macro_define(word)
			# print(x)
			if (x[0] not in self.defines):
				self.objects.append(x[0])
				self.defines[x[0]] = x
				# self.objects.append(x[0])
				# self.defines.append(x)


	def parse_macro_define(self, macro):
		
		ignore_whitespace = 0
		ignore_next = 0
		word = ""
		i = 0
		# print("macro: ", macro)
		for c in macro:
			i += 1
			# print("parse macro define: ", macro, word)
			if (ignore_next and c not in "\n \t"): ignore_next = False
			# if (c not in "\n \t" and ignore_whitespace): ignore_whitespace = False
			if (c == "("): ignore_whitespace = True
			elif (c == ")"): ignore_whitespace = False
			elif (c == "\\"): ignore_next = True
			elif (c == "\n" and not ignore_whitespace): break
			elif (c == " " and not ignore_whitespace): break
			word += c

		return word, macro[i:].replace("\\", "")


	def add_file_to_queue(self):
		word = ""
		for char in self.text[self.index:]:
			if (char in az or char == "/" or char == "\\" or char == "."):
				word += char
			elif (char == " "):
				if (word != "include"): return
				else: word = ""
			elif (char == "\n"):
				break

		# self.parent.command_out_set(f"file {word} was added to queue")
		if (word not in self.indexed_files): self.file_queue.append(word)


	def search_whitespace(self, index) -> bool:
		for char in self.text[index:]:
			if (char == " " or char == "\t"):
				pass
			elif (char == "\n"):
				return False
			else:
				return True

	def add_object(self, name):
		if (name and name not in self.objects):
			self.objects.append(name)

	def add_function(self, name):
		if (name and name not in self.functions):
			self.functions.append(name)

	def add_var(self, name):
		if (name and name not in self.vars):
			self.vars.append(name)


	def make_func_new(self, expr):
		# print("EXPR: ", expr)
		if (re.search(r"=|return", expr)): return
		# if (re.match(r"([a-zA-Z_]+[a-zA-Z_0-9]+\ )+ \(([a-zA-Z_]+[a-zA-Z_0-9]+\ )+\)", expr)): print("ok")
		# if (re.match(r"((([a-zA-Z_]+[a-zA-Z_0-9]*\ +)*([a-zA-Z_]+[a-zA-Z_0-9]*))\((.)*\))", expr)): print("ok")
		# if (re.match(r"([[a-zA-Z_]+[a-zA-Z_0-9]*\ +]*[a-zA-Z_]+[a-zA-Z_0-9]*)\(.*\)", expr)): pass

		# expr = expr.replace("\n", "")
		# expr = expr.replace("\t", " ")

		expr = re.sub("\s+", " ", expr)
		# group 1 is the full type
		# group 3 is the last part of the type
		# group 4 is the function name
		# group 5 are parameters
		# print("\n\nfunc: ", expr)
		m = self.function_regex.match(expr)

		if (m):
			# print("dwadw\n\n")
			x = (m.group(1), m.group(4), m.group(5))
			# print(m.groups())
			if (m.group(4) not in self.defines):
				self.defines[m.group(4)] = x
				self.functions.append(m.group(4))

	
	def make_func(self, prev_word, word):
		if (prev_word == "#define"):
			self.add_object(word)
			
		elif (prev_word == "struct"):
			self.add_object(word)

		elif (word == "struct"):
			self.add_object(self.get_struct_name())

		elif (self.text[self.index] == "("):
			self.add_function(word)

	def make_var(self, prev_word, word, override=False, index=None):
		if (not index): index = self.index
		if (self.text[index+1] != "="): self.add_var(word)
		if (override): self.add_var(word)

	def get_scope(self, type, name, index):
		pass		

	def get_struct_name(self):
		#haahah I have no idea what the fuck I am doing
		brackets = 0
		word = ""
		for index, char in enumerate(self.text[self.index:], self.index):
			if (char == "{"):
				brackets += 1

			elif (char == "}"):
				brackets -= 1
				if (brackets == 0):
					for char in self.text[index:]:
						if (char in az):
							word += char
						elif (word and char in num):
							word += char
						elif (char == ";" and word != ""):
							return word
						elif (char == "\n"):
							self.buffer.tag_add("error_bg", f"1.0+{index}c")
							return None

			self.buffer.tag_remove("error_bg", f"1.0+{index}c")
