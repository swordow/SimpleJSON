# coding=utf-8

ST_VN = 0
ST_VT = 1

SYM_OBJ = 1
SYM_EP = 2
SYM_MEMBERS = 3
SYM_PAIR = 4
SYM_STRING = 5
SYM_VALUE = 6
SYM_ARRAY = 7
SYM_ELEMENTS = 8
SYM_NUMBER = 9
SYM_INT = 10
SYM_FRAC = 11
SYM_EXP = 12
SYM_DOT = 13
SYM_MINUS = 14
SYM_LEFT_BRACE = 15
SYM_RIGHT_BRACE = 16
SYM_LEFT_BRACKET = 17
SYM_RIGHT_BRACKET = 18
SYM_COMMA = 19
SYM_EXP_E = 20
SYM_COLON = 21
SYM_DOUBLE_QUOTE = 22
SYM_BACK_SLASH = 23
SYM_SLASH = 24
SYM_CHARS = 25
SYM_CHAR = 26

SYM_b = 27
SYM_f = 28
SYM_n = 29
SYM_r = 30
SYM_e = 31
SYM_E = 32
SYM_u = 33
SYM_PLUS = 34
SYM_t = 35

SYM_A = 36
SYM_B = 37
SYM_C = 38
SYM_D = 39
SYM_F = 40

SYM_a = 41
SYM_c = 42
SYM_d = 43

SYM_HEX_DIGIT = 44

SYM_ONE = 45
SYM_TWO = 46
SYM_THREE = 47
SYM_FOUR =  48
SYM_FIVE = 47
SYM_SIX = 48
SYM_SEVEN = 49
SYM_EIGHT = 50
SYM_NINE = 51
SYM_ZERO = 52

SYM_DIGIT = 53
SYM_DIGITS = 54

SYM_ANY_CHAR = 55

SYM_DIGIT1_9 = 56

SYM_DICT = {
	SYM_OBJ:"SYM_OBJ",
	SYM_EP:"SYM_EP",
	SYM_MEMBERS : "SYM_MEMBERS",
	SYM_PAIR : "SYM_PAIR",
	SYM_STRING : "SYM_STRING",
	SYM_VALUE : "SYM_VALUE",
	SYM_ARRAY : "SYM_ARRAY",
	SYM_ELEMENTS :"SYM_ELEMENTS",
	SYM_NUMBER : "SYM_NUMBER",
	SYM_INT : "SYM_INT",
	SYM_FRAC : "SYM_FRAC",
	SYM_EXP : "SYM_EXP",
	SYM_DOT : "SYM_DOT",
	SYM_MINUS : "SYM_MINUS",
	SYM_LEFT_BRACE : "SYM_LEFT_BRACE",
	SYM_RIGHT_BRACE : "SYM_RIGHT_BRACE",
	SYM_LEFT_BRACKET : "SYM_LEFT_BRACKET",
	SYM_RIGHT_BRACKET : "SYM_RIGHT_BRACKET",
	SYM_COMMA : "SYM_COMMA",
	SYM_EXP_E : "SYM_EXP_E",
	SYM_COLON : "SYM_COLON",
	SYM_DOUBLE_QUOTE : "SYM_DOUBLE_QUOTE",
	SYM_BACK_SLASH : "SYM_BACK_SLASH",
	SYM_SLASH : "SYM_SLASH",
	SYM_CHARS : "SYM_CHARS",
	SYM_CHAR : "SYM_CHAR",

	SYM_b : "SYM_b",
	SYM_f : "SYM_f",
	SYM_n : "SYM_n",
	SYM_r : "SYM_r",
	SYM_e : "SYM_e",
	SYM_E : "SYM_E",
	SYM_u : "SYM_u",
	SYM_PLUS : "SYM_PLUS",
	SYM_t : "SYM_t",

	SYM_A : "SYM_A",
	SYM_B : "SYM_B",
	SYM_C : "SYM_C",
	SYM_D : "SYM_D",
	SYM_F : "SYM_F",

	SYM_a : "SYM_a",
	SYM_c : "SYM_c",
	SYM_d : "SYM_d",

	SYM_HEX_DIGIT : "SYM_HEX_DIGIT",

	SYM_ONE : "SYM_ONE",
	SYM_TWO : "SYM_TWO",
	SYM_THREE : "SYM_THREE",
	SYM_FOUR : "SYM_FOUR",
	SYM_FIVE : "SYM_FIVE",
	SYM_SIX : "SYM_SIX",
	SYM_SEVEN : "SYM_SEVEN",
	SYM_EIGHT : "SYM_EIGHT",
	SYM_NINE : "SYM_NINE",
	SYM_ZERO : "SYM_ZERO",

	SYM_DIGIT : "SYM_DIGIT",
	SYM_DIGITS : "SYM_DIGITS",

	SYM_ANY_CHAR : "SYM_ANY_CHAR",

	SYM_DIGIT1_9 : "SYM_DIGIT1_9"
}

'''
	1. 空串是VN还是VT
'''
class SymbolSet(object):
	def __init__(self):
		super(SymbolSet, self).__init__()
		self.ss = []

	def append(self, symbol):
		pass

class Production(object):
	def __init__(self, sym_left, sym_rights):
		super(Production, self).__init__()
		self.sym_left = sym_left
		self.sym_rights = sym_rights

	def dump(self):
		out = SYM_DICT[self.sym_left.value] + " -> "
		for p in self.sym_rights:
			for s in p:
				if s.type == ST_VT:
					out += str(s.value)
				else:
					out += SYM_DICT[s.value]
				out += ' '
			out += ' | '
		return out[:-2]

	def remove_indirect_left_recursion(self, sym, production):
		n_rights = []
		for p in self.sym_rights:
			# A->By
			if sym.equal(p[0]):
				for pp in production.sym_rights:
					nn = []
					for ss in pp:
						nn.append(ss)
					for ss in xrange(1,len(p)):
						nn.append(p[ss])
					n_rights.append(nn)

			else:
				n_rights.append(p)
		self.sym_rights = n_rights


class Symbol(object):
	'''
	type = ST_VT
	value = None 
	表示匹配任意字符
	'''
	def __init__(self, type_, value_):
		super(Symbol, self).__init__()
		self.type = type_
		self.value = value_

	def equal(self, sym):
		if self.value != SYM_ANY_CHAR:
			return self.type == sym.type and self.value == sym.value

		elif self.type == ST_VT and sym.value != SYM_DOUBLE_QUOTE and sym.value != SYM_BACK_SLASH:
			return True
		
		else:
			return False

	def is_vt(self):
		return self.type == ST_VT

	def is_vn(self):
		return self.type == ST_VN
		

class JsonGramma(object):
	


	def __init__(self):

		self.vn = SymbolSet()
		self.productions = []
		self.symbols = {
			SYM_OBJ:Symbol(ST_VN, SYM_OBJ),
			SYM_MEMBERS: Symbol(ST_VN, SYM_MEMBERS),
			SYM_PAIR: Symbol(ST_VN, SYM_PAIR),
			SYM_STRING: Symbol(ST_VN, SYM_STRING),
			SYM_VALUE: Symbol(ST_VN, SYM_VALUE),
			SYM_ARRAY: Symbol(ST_VN, SYM_ARRAY),
			SYM_ELEMENTS: Symbol(ST_VN, SYM_ELEMENTS),
			SYM_NUMBER:Symbol(ST_VN, SYM_NUMBER),
			SYM_CHARS:Symbol(ST_VN, SYM_CHARS),
			SYM_CHAR: Symbol(ST_VN, SYM_CHAR),
			SYM_HEX_DIGIT: Symbol(ST_VN, SYM_HEX_DIGIT),
			SYM_DIGITS: Symbol(ST_VN, SYM_DIGITS),
			SYM_DIGIT: Symbol(ST_VN, SYM_DIGIT),
			SYM_DIGIT1_9: Symbol(ST_VN, SYM_DIGIT1_9),
			SYM_ANY_CHAR: Symbol(ST_VT, SYM_ANY_CHAR),
			SYM_EXP_E: Symbol(ST_VN, SYM_EXP_E),
			SYM_HEX_DIGIT: Symbol(ST_VN, SYM_HEX_DIGIT),
			SYM_INT: Symbol(ST_VN, SYM_INT),
			SYM_FRAC: Symbol(ST_VN, SYM_FRAC),
			SYM_INT: Symbol(ST_VN, SYM_INT),
			SYM_EXP: Symbol(ST_VN, SYM_EXP),

			SYM_DOT: Symbol(ST_VT, '.'),
			SYM_MINUS: Symbol(ST_VT, '-'),
			SYM_LEFT_BRACE: Symbol(ST_VT, '{'),
			SYM_RIGHT_BRACE: Symbol(ST_VT, '}'),
			SYM_LEFT_BRACKET: Symbol(ST_VT, '['),
			SYM_RIGHT_BRACKET: Symbol(ST_VT, ']'),
			SYM_COMMA: Symbol(ST_VT, ','),
			SYM_COLON: Symbol(ST_VT, ':'),
			SYM_DOUBLE_QUOTE: Symbol(ST_VT, '"'),
			SYM_BACK_SLASH: Symbol(ST_VT, '\\'),
			SYM_SLASH: Symbol(ST_VT, '/'),
			SYM_PLUS: Symbol(ST_VT, '+'),

			SYM_A: Symbol(ST_VT, 'A'),
			SYM_a: Symbol(ST_VT, 'a'),
			SYM_B: Symbol(ST_VT, 'B'),
			SYM_b: Symbol(ST_VT, 'b'),
			SYM_C: Symbol(ST_VT, 'C'),
			SYM_c: Symbol(ST_VT, 'c'),
			SYM_D: Symbol(ST_VT, 'D'),
			SYM_d: Symbol(ST_VT, 'd'),
			SYM_E: Symbol(ST_VT, 'E'),
			SYM_e: Symbol(ST_VT, 'e'),

			SYM_F: Symbol(ST_VT, 'F'),
			SYM_f: Symbol(ST_VT, 'f'),

			SYM_n: Symbol(ST_VT, 'n'),
			SYM_r: Symbol(ST_VT, 'r'),
			SYM_t: Symbol(ST_VT, 't'),
			SYM_u: Symbol(ST_VT, 'u'),

			SYM_ONE: Symbol(ST_VT, '1'),
			SYM_TWO: Symbol(ST_VT, '2'),
			SYM_THREE: Symbol(ST_VT, '3'),
			SYM_FOUR: Symbol(ST_VT, '4'),
			SYM_FIVE: Symbol(ST_VT, '5'),
			SYM_SIX: Symbol(ST_VT, '6'),
			SYM_SEVEN: Symbol(ST_VT, '7'),
			SYM_EIGHT: Symbol(ST_VT, '8'),
			SYM_NINE: Symbol(ST_VT, '9'),
			SYM_ZERO: Symbol(ST_VT, '0'),

		}
		self.productions={
			SYM_OBJ:Production(
				self.symbols[SYM_OBJ], [
				[self.symbols[SYM_LEFT_BRACE], self.symbols[SYM_RIGHT_BRACE]],
				[self.symbols[SYM_LEFT_BRACE], self.symbols[SYM_MEMBERS], self.symbols[SYM_RIGHT_BRACE]]
				]),
			SYM_MEMBERS:Production(
				self.symbols[SYM_MEMBERS],[
				[self.symbols[SYM_PAIR]],
				[self.symbols[SYM_PAIR],self.symbols[SYM_COMMA], self.symbols[SYM_MEMBERS]]
				]),
			SYM_PAIR:Production(
				self.symbols[SYM_PAIR],[
				[self.symbols[SYM_STRING], self.symbols[SYM_COLON], self.symbols[SYM_VALUE]]
				]),
			SYM_ARRAY:Production(
				self.symbols[SYM_ARRAY],[
				[self.symbols[SYM_LEFT_BRACKET], self.symbols[SYM_RIGHT_BRACKET]],
				[self.symbols[SYM_LEFT_BRACKET], self.symbols[SYM_ELEMENTS], self.symbols[SYM_RIGHT_BRACKET]]
				]),
			SYM_ELEMENTS:Production(
				self.symbols[SYM_ELEMENTS],[
				[self.symbols[SYM_VALUE]],
				[self.symbols[SYM_VALUE],self.symbols[SYM_COMMA], self.symbols[SYM_ELEMENTS]],
				]),
			SYM_VALUE:Production(
				self.symbols[SYM_VALUE],[
				[self.symbols[SYM_STRING]],
				[self.symbols[SYM_NUMBER]],
				[self.symbols[SYM_OBJ]],
				[self.symbols[SYM_ARRAY]]
				]),
			SYM_STRING:Production(
				self.symbols[SYM_STRING],[
				[self.symbols[SYM_DOUBLE_QUOTE],self.symbols[SYM_DOUBLE_QUOTE]],
				[self.symbols[SYM_DOUBLE_QUOTE],self.symbols[SYM_CHARS], self.symbols[SYM_DOUBLE_QUOTE]]
				]),
			SYM_CHARS:Production(
				self.symbols[SYM_CHARS],[
				[self.symbols[SYM_CHAR]],
				[self.symbols[SYM_CHAR], self.symbols[SYM_CHARS]],
				]),
			SYM_CHAR:Production(
				self.symbols[SYM_CHAR],[
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_DOUBLE_QUOTE]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_BACK_SLASH]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_SLASH]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_b]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_f]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_n]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_r]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_t]],
				[self.symbols[SYM_BACK_SLASH], self.symbols[SYM_u], self.symbols[SYM_HEX_DIGIT],self.symbols[SYM_HEX_DIGIT],self.symbols[SYM_HEX_DIGIT],self.symbols[SYM_HEX_DIGIT]],
				[self.symbols[SYM_ANY_CHAR]]

				]),
			SYM_NUMBER:Production(
				self.symbols[SYM_NUMBER],[
				[self.symbols[SYM_INT]],
				[self.symbols[SYM_INT], self.symbols[SYM_FRAC]],
				[self.symbols[SYM_INT], self.symbols[SYM_EXP]],
				[self.symbols[SYM_INT], self.symbols[SYM_FRAC], self.symbols[SYM_EXP]]
				]),
			SYM_INT:Production(
				self.symbols[SYM_INT],[
				[self.symbols[SYM_DIGIT]],
				[self.symbols[SYM_DIGIT1_9], self.symbols[SYM_DIGITS]],
				[self.symbols[SYM_MINUS], self.symbols[SYM_DIGIT]],
				[self.symbols[SYM_MINUS], self.symbols[SYM_DIGIT1_9], self.symbols[SYM_DIGITS]]
				]),
			SYM_FRAC:Production(
				self.symbols[SYM_FRAC],[
				[self.symbols[SYM_DOT], self.symbols[SYM_DIGITS]]
				]),
			SYM_EXP:Production(
				self.symbols[SYM_EXP],[
				[self.symbols[SYM_EXP_E], self.symbols[SYM_DIGITS]]
				]),
			SYM_DIGITS:Production(
				self.symbols[SYM_DIGITS],[
				[self.symbols[SYM_DIGIT]],
				[self.symbols[SYM_DIGIT], self.symbols[SYM_DIGITS]],
				]),
			SYM_EXP_E:Production(
				self.symbols[SYM_EXP_E],[
				[self.symbols[SYM_e]],
				[self.symbols[SYM_e], self.symbols[SYM_PLUS]],
				[self.symbols[SYM_e], self.symbols[SYM_MINUS]],
				[self.symbols[SYM_E]],
				[self.symbols[SYM_E],self.symbols[SYM_PLUS]],
				[self.symbols[SYM_E],self.symbols[SYM_MINUS]],
				]),
			SYM_DIGIT:Production(
				self.symbols[SYM_DIGIT],[
				[self.symbols[SYM_ONE]],
				[self.symbols[SYM_TWO]],
				[self.symbols[SYM_THREE]],
				[self.symbols[SYM_FOUR]],
				[self.symbols[SYM_FIVE]],
				[self.symbols[SYM_SIX]],
				[self.symbols[SYM_SEVEN]],
				[self.symbols[SYM_EIGHT]],
				[self.symbols[SYM_NINE]],
				[self.symbols[SYM_ZERO]],
			]),
			SYM_DIGIT1_9:Production(
				self.symbols[SYM_DIGIT1_9],[
				[self.symbols[SYM_ONE]],
				[self.symbols[SYM_TWO]],
				[self.symbols[SYM_THREE]],
				[self.symbols[SYM_FOUR]],
				[self.symbols[SYM_FIVE]],
				[self.symbols[SYM_SIX]],
				[self.symbols[SYM_SEVEN]],
				[self.symbols[SYM_EIGHT]],
				[self.symbols[SYM_NINE]],
			]),
			SYM_HEX_DIGIT:Production(
				self.symbols[SYM_HEX_DIGIT],[
				[self.symbols[SYM_DIGIT]],
				[self.symbols[SYM_A]],
				[self.symbols[SYM_B]],
				[self.symbols[SYM_C]],
				[self.symbols[SYM_D]],
				[self.symbols[SYM_E]],
				[self.symbols[SYM_a]],
				[self.symbols[SYM_b]],
				[self.symbols[SYM_c]],
				[self.symbols[SYM_d]],
				[self.symbols[SYM_e]]
				]),
		}

	def dump(self):
		for s,p in self.productions.iteritems():
			print p.dump();

	def remove_left_recursion(self):
		pass

	def remove_indirect_left_recursion(self):
		vts = []
		for k,s in self.symbols.iteritems():
			if s.is_vn():
				vts.append(s)

		for i in xrange(0,len(vts)):
			for j in xrange(0,i):
				A = vts[i]
				B = vts[j]
				# find A->By
				# and B->a|b
				# replace with A->ay|by
				PA = self.productions[A.value]
				PB = self.productions[B.value]
				PA.remove_indirect_left_recursion(B, PB);

	def get_first_set_of_symbol(self, first_set, sym):
		if sym.is_vt() and sym.value not in first_set:
			first_set.append(sym.value)
			return first_set

		if sym.is_vn():
			return self.get_first_set_of_production(first_set, self.productions[sym.value])

	def get_first_set_of_production(self, first_set, p):
		for item in p.sym_rights:
			self.get_first_set_of_symbol(first_set, item[0])

		return first_set

	def get_follow_set_of_symbol(self, follow_set, sym):
		if sym.is_vt() and sym.value not in follow_set:
			follow_set.append(sym.value)
			return follow_set

		if sym.is_vn():
			return self.get_follow_set_of_production(follow_set, self.productions[sym.value])

	def get_follow_set_of_production(self, follow_set, p):
		for item in p.sym_rights:
			self.get_follow_set_of_symbol(follow_set, item[-1])

		return follow_set

	def check_LL1(self):
		vts = []
		for k,s in self.symbols.iteritems():
			if s.is_vn():
				vts.append(s)

		first_set = {}
		for sym in vts:
			first_list = []
			self.get_first_set_of_symbol(first_list, sym)
			first_set[SYM_DICT[sym.value]] = first_list
		print '------------------------ first set ------------------------'
		for k, v in first_set.iteritems():
			line = k + '\t\t\t';
			for vv in v:
				line = line + repr(vv) + ','
			line = line[:-1]
			print line 

		print '------------------------ follow set -----------------------'
		follow_set = {
			'SYM_OBJ':['#',],
		}
		for s,p in self.productions.iteritems():
			pass
		print follow_set





			

a = JsonGramma()
a.dump()
a.remove_indirect_left_recursion()
print '-------------------------------------------'
a.dump()
a.check_LL1()

