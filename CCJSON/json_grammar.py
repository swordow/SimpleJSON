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
SYM_FIVE = 49
SYM_SIX = 50
SYM_SEVEN = 51
SYM_EIGHT = 52
SYM_NINE = 53
SYM_ZERO = 54

SYM_DIGIT = 55
SYM_DIGITS = 56

SYM_ANY_CHAR = 57

SYM_DIGIT1_9 = 58

global SYM_DICT
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

class SymbolSet(object):
	def __init__(self):
		super(SymbolSet, self).__init__()
		self.sym = []
		self.sym_str = []

	def append(self, symbol):
		if symbol == '#':
			self.sym_str.append('#')
			return
		self.sym.append(symbol)
		self.sym_str.append(repr(symbol))
	
	def has(self, symbol):
		return (repr(symbol) in self.sym_str)

	def all_symbols(self):
		return self.sym

	def __repr__(self):
		return repr(self.sym_str)

class FirstSet(object):
	def __init__(self):
		self.dirty = True
		self.first_set = {}

	def add(self, sym_str):
		self.first_set[sym_str] = SymbolSet()
		self.dirty = True

	def check(self, sym_str):
		return sym_str in self.first_set

	def append(self, sym_str, symbol):
		self.first_set[sym_str].append(symbol)
		self.dirty = True
	
	def has(self, sym_str, symbol):
		return self.first_set[sym_str].has(symbol)

	def all_symbols(self, sym_str):
		return self.first_set[sym_str].all_symbols()

# 符号串
class SymbolSequence(object):
	def __init__(self, seq):
		self.seq = seq

	def equal(self, seq):
		return self.repr() == seq.repr()

		if len(self.seq) != len(seq.seq):
			return False
		for i in xrange(len(seq.seq)):
			if self.seq[i].repr() != seq.seq[i]:
				return False
		return True

	def symbols(self):
		return self.seq

	def first_symbol(self):
		return self.seq[0]

	def is_empty_sequence(self):
		return len(self.seq) == 0

	def symbol(self, i):
		return self.seq[i]

	def get_first_non_terminal_symbol(self):
		for sym in self.seq:
			if sym.is_vn():
				return sym

	def remove_first_symbol(self):
		self.seq = self.seq[1:]

	def get_symbols(self, start, end):
		return self.seq[start:end]

	def clone(self):
		clone = []
		for i in xrange(len(self.seq)):
			clone.append(self.seq[i])
		return SymbolSequence(clone)

	def add_symbol(self, sym):
		self.seq.append(sym)

	def add_symbols(self, syms):
		for sym in syms:
			self.add_symbol(sym)

	def contains_symbol(self, sym):
		if sym.equal(self.seq[-1]):
			return True, True

		for _sym in self.seq:
			if sym.equal(_sym):
				return True,False
		return False, False

	def get_sub_sequence_after_symbol(self, sym):
		if sym.equal(self.seq[-1]):
			return SymbolSequence([])

		seq = SymbolSequence([])
		found = False
		for _sym in self.seq:
			if not found:
				if sym.equal(_sym):
					found = True
			else:
				seq.add_symbol(_sym)
		return seq


	def __repr__(self):
		s = ""
		if len(self.seq) == 0:
			return "es"
		for i in xrange(len(self.seq)):
			s += " "+repr(self.seq[i])
		return s

	def repr(self):
		return repr(self)

class Production(object):
	def __init__(self, sym_left, sym_rights):
		super(Production, self).__init__()
		self.sym_left = sym_left
		self.sym_seqs = []
		for ss in sym_rights:
			self.sym_seqs.append(SymbolSequence(ss))

	def dump(self):
		out = SYM_DICT[self.sym_left.value] + " -> "
		for ss in self.sym_seqs:
			out += repr(ss) + ' | '
		return out[:-2]

	# wrong...
	def remove_indirect_left_recursion(self, production):
		n_rights = []
		# 遍历自己的所有候选符号串
		for candidate_seq in self.sym_seqs:
			# A->By
			# 如果传入的产生式的起始符号和当前候选符号串的首字符相同
			if production.sym_left.equal(candidate_seq.first_symbol()):
				# 就遍历传入的产生式的所有候选符号串,重新生成A的产生式符号串
				# B->a|T|c
				# A->ay|Ty|cy
				for in_candidate_seq in production.sym_seqs:
					new_seq = in_candidate_seq.clone()
					new_seq.add_symbols(candidate_seq.get_symbols(1, None))
					n_rights.append(new_seq)

			else:
				n_rights.append(candidate_seq)
		self.sym_seqs = n_rights

	def equal(self, production):
		if not len (production.sym_seqs) == len(self.sym_seqs):
			return False
		
		for seq in self.sym_seqs:
			found = False
			for oseq in production.sym_seqs:
				#print 'compare', seq.repr(), oseq.repr(), seq.__class__, oseq.__class__
				if seq.equal(oseq):
					found = True
					break
			if not found:
				return False
		return True

	def adjust_common_left_symbol(self, gramma):
		sts = {}
		new_productions = {}
		bak_sym_seqs = self.sym_seqs
		self.sym_seqs = []
		
		for seq in bak_sym_seqs:
			# 空串
			if seq.is_empty_sequence():
				self.sym_seqs.append(seq)
				continue

			# 如果是终结符
			if seq.first_symbol().is_vt():
				if seq.first_symbol().repr() not in sts:
					sts[seq.first_symbol().repr()] = []
				sts[seq.first_symbol().repr()].append(seq)
				continue

			# 如果是非终结符
			if seq.first_symbol().repr() not in sts:
				sts[seq.first_symbol().repr()] = []
			sts[seq.first_symbol().repr()].append(seq)
			continue

			self.sym_seqs.append(seq)
				
		
		for sym_str, seq_list in sts.iteritems():
			if len(seq_list) < 2:
				self.sym_seqs.append(seq_list[0])
				continue
			sym = seq_list[0].first_symbol()
			extend_code = gramma.get_extend_symbol_code()
			extend_symbol = self.sym_left.produce_extend_symbol(extend_code)
			extend_production = Production(extend_symbol, [])
			for seq in seq_list:
				cloned = seq.clone()
				cloned.remove_first_symbol()
				extend_production.sym_seqs.append(cloned)

			# 提取公共左因子之后，会产生，不一样的扩展非终结符，但是却有一样的产生式
			# 比如现在碰到的
			# SYM_EXP_E_EXTEND_1007 -> es |  + |  -
			# SYM_EXP_E_EXTEND_1008 -> es |  + |  -
			dup_extend_symbol = None
			for ec, ep in new_productions.iteritems():
				if extend_production.equal(ep):
					dup_extend_symbol = ep.sym_left
					print 'Notification!! Merge same production with different VN', SYM_DICT[ec], extend_symbol
					break
			if dup_extend_symbol is None:	
				new_productions[extend_code] = extend_production
				extend_seq = SymbolSequence([sym, extend_symbol])
			else:
				extend_seq = SymbolSequence([sym, dup_extend_symbol])
			self.sym_seqs.append(extend_seq)

		return new_productions



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
	
	def __repr__(self):
		if self.is_vt() and self.value != SYM_ANY_CHAR:
			return self.value
		else:
			return SYM_DICT[self.value]

	def repr(self):
		return repr(self)

	def produce_extend_symbol(self, extend_code):
		assert(self.type == ST_VN)
		ret = Symbol(self.type, extend_code)
		global SYM_DICT
		SYM_DICT[extend_code] = self.repr() + '_EXTEND_'+repr(extend_code)
		return ret
		

class JsonGramma(object):
	

	def __init__(self):
		self.extend_sym_code = 1000
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
				]), #SYM_OBJ -> {} | { SYM_MEMBERS }  // 意味着需要提取公共左因子 
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
				[self.symbols[SYM_DIGITS]],
				[self.symbols[SYM_MINUS], self.symbols[SYM_DIGITS]]
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

	def get_extend_symbol_code(self):
		ret = self.extend_sym_code
		self.extend_sym_code += 1
		return ret

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
				PA.remove_indirect_left_recursion(PB)

	def adjust_common_left_symbol(self):
		bak_productions = self.productions
		self.productions = {}
		for sym_code, production in bak_productions.iteritems():
			new_productions = production.adjust_common_left_symbol(self)
			self.productions[sym_code] = production
			for extend_code, extend_p in new_productions.iteritems():
				self.productions[extend_code] = extend_p
				self.symbols[extend_code] = extend_p.sym_left

	def get_first_set_of_symbol(self, first_set, sym):
		sym_str = sym.repr()
		if not first_set.check(sym_str):
			first_set.add(sym_str)
		else:
			return

		if sym.is_vt():
			if not first_set.has(sym_str, sym):
				first_set.append(sym_str, sym)
			return

		return self.get_first_set_of_production(first_set, self.productions[sym.value])

	def get_first_set_of_production(self, first_set, p):
		vn_str = repr(p.sym_left)
		if not first_set.check(vn_str):
			first_set.add(vn_str)

		for seq in p.sym_seqs:
			# X -> es  then FIRST(X) add es
			if seq.repr() == SymbolSequence([]).repr():
				if not first_set.has(vn_str, seq):
					first_set.append(vn_str, seq)
				continue

			# X->Y1Y2 | Y3Y4 | Y5Y6
			# FIRST(X) = FRIST(Y1Y2) U FIRST(Y3Y4) U FIRST(Y5Y6)
			self.get_first_set_of_symbol_sequence(first_set, seq)
			for item in first_set.all_symbols(repr(seq)):
				if not first_set.has(vn_str, item):
					first_set.append(vn_str, item)

	# SEQ-> Y1Y2Y3Y4Y5
	def get_first_set_of_symbol_sequence(self, first_set, seq):
		assert (seq.repr() != SymbolSequence([]).repr())
		
		str_seq = repr(seq)
		
		if not first_set.check(str_seq):
			 first_set.add(str_seq)

		empty_seq_mark = [False]*len(seq.symbols())
		empty_seq = SymbolSequence([])
		empty_seq_count = 0
		first_sym_has_empty_seq_idx = -1
		for i in xrange(len(seq.symbols())):
			sym = seq.symbols()[i]
			self.get_first_set_of_symbol(first_set, sym)
			if first_set.has(sym.repr(), empty_seq):
				empty_seq_mark[i] = True
				if first_sym_has_empty_seq_idx < 0:
					first_sym_has_empty_seq_idx = i
				empty_seq_count += 1

		if empty_seq_count == len(seq.symbols()): # all symbols has empty seq in first set
			if not first_set.has(str_seq, empty_seq):
				first_set.append(str_seq, empty_seq)

		# add FIRST(Y1) to FIRST(seq)
		for sym in first_set.all_symbols(seq.first_symbol().repr()):
			if not first_set.has(str_seq, sym):
				first_set.append(str_seq, sym)

		#print 'EMPTY SEQ NARK',empty_seq_mark

		# if FIRST(Y1) has empty seq
		# add FIRST(Y2) to seq
		# if FIRST(Y2) has empty seq
		# add FIRST(Y3) to seq
		# and so on
		for idx in xrange(len(empty_seq_mark)-1):
			if empty_seq_mark[idx]:
				# add FIRST(Yidx+1) to FIRST(seq)
				sym_idx_1 = seq.symbols()[idx+1]
				for sym in first_set.all_symbols(sym_idx_1.repr()):
					if not first_set.has(str_seq, sym):
						first_set.append(str_seq, sym)
			else:
				break
		
	# FIRST(X)
	# if X is terminal then FIRST(X) = {x}
	# if X is nonterminal and X->Y1Y2Y3Yk
	# if es in all Yj ( 1 <= j <= k), then es add to FIRST(X)
	# if es in all Yj ( 1 <= j < i), then FIRST(Yi) add to FIRST(X)
	def get_first_set(self):
		fs = FirstSet()
		while fs.dirty:
			print 'XXXXXXXXXXXXXXXXXX'
			fs.dirty = False
			for _, p in self.productions.iteritems():
				self.get_first_set_of_production(fs , p)
		
		return fs

	def check_LL1(self):
		# vts = []
		# for k,s in self.symbols.iteritems():
		# 	if s.is_vn():
		# 		vts.append(s)

		# first_set = {}
		# for sym in vts:
		# 	self.get_first_set_of_symbol(first_set, sym)

		# Get the first set through all the productions
		first_set = self.get_first_set()
		empty_seq = SymbolSequence([])

		print '------------------------ first set ------------------------'
		# print first_set
		for k, v in first_set.first_set.iteritems():
			line = "<"+k+">" + '\t\t\t';
			for vv in v.all_symbols():
				line = line + repr(vv) + ','
			line = line[:-1]
			print line 

		print '------------------------ follow set -----------------------'
		
		follow_set = {
			repr(self.symbols[SYM_OBJ]):SymbolSet(),
		}

		follow_set[repr(self.symbols[SYM_OBJ])].append('#')
		# https://www.cs.virginia.edu/~cs415/reading/FirstFollowLL.pdf
		# Follow set are ONLY defined for nonterminals....
		# 分析每个产生式的每个候选项
		# 按照self.symbols的顺序计算每个vtn的followset
		nvts = []
		for _ , sym in self.symbols.iteritems():
			if sym.is_vn():
				nvts.append(sym)

		follow_set_changed = True
		while follow_set_changed:
			follow_set_changed = False
			for nvt in nvts:
				if repr(nvt) not in follow_set:
					follow_set[repr(nvt)] = SymbolSet()

				nvt_str = repr(nvt)
				for ssym, p in self.productions.iteritems():
				
					if repr(p.sym_left) not in follow_set:
						follow_set[repr(p.sym_left)] = SymbolSet()

					for seq in p.sym_seqs:
						if seq.is_empty_sequence():
							continue

						contained, last = seq.contains_symbol(nvt)
						if not contained:
							continue
						
						#print 'Current Production %s -> <%s> '%(repr(p.sym_left),repr(seq)), 'Current Symbol %s' % repr(nvt)

						# X -> aPb
						if not last:

							
							beta_seq = seq.get_sub_sequence_after_symbol(nvt)
							
							#print 'Get one of the Seq <%s>'%repr(beta_seq)

							if not first_set.check(repr(beta_seq)):
								#print 'Seq:<%s> not in first set and cal the first set'%(repr(beta_seq))
								self.get_first_set_of_symbol_sequence(first_set, beta_seq)
							
							#print 'Seq:<%s> first set=%s'%(repr(beta_seq),repr(first_set.all_symbols(repr(beta_seq))))

							
							# follow(p) = first(b) - {e}
							first_seq = first_set.all_symbols(repr(beta_seq))
							for sym in first_seq:
								if not follow_set[nvt_str].has(sym) and repr(sym) != repr(empty_seq):
									follow_set[nvt_str].append(sym)
									#print 'FollowSet(%s)=%s'%(nvt_str, repr(follow_set[nvt_str]))
									follow_set_changed = True
							
							# 如果 {e} in first(b)
							# follow(p) U= follow(X)
							if repr(empty_seq) in first_seq:
								for fsym in follow_set[repr(p.sym_left)].all_symbols():
									if not follow_set[nvt_str].has(fsym):
										follow_set[nvt_str].append(fsym)
										#print 'FollowSet(%s)=%s'%(nvt_str, repr(follow_set[nvt_str]))
										follow_set_changed = True

							continue

						# 如果 X->aP
						# follow(p) U= follow(X)
						for fsym in follow_set[repr(p.sym_left)].all_symbols():
							if not follow_set[nvt_str].has(fsym):
								follow_set[nvt_str].append(fsym)
								#print 'FollowSet(%s)=%s'%(nvt_str, repr(follow_set[nvt_str]))
								follow_set_changed = True
						

		# print first_set
		for k, v in follow_set.iteritems():
			line = "NVT<"+k+">" + '\t\t\t';
			for vv in v.all_symbols():
				line = line + repr(vv) + ','
			line = line[:-1]
			print line 
		print '------------------------ make_predict_table -----------------------'

		m = self.make_predict_table(first_set, follow_set)

		for _sym, _token in m.iteritems():
			for _i, p in m[_sym].iteritems():
				print '[%s, %s] -> %s'%(_sym, _i, p)

	# 1. 空串既不是终结符，也不是非终结符
	def make_predict_table(self, first_set, follow_set):
		M = {}
		for sym_code, p in self.productions.iteritems():
			if repr(p.sym_left) not in M:
				M[repr(p.sym_left)] = {}
			for seq in p.sym_seqs:
				if repr(seq) == repr(SymbolSequence([])):
					continue
				_first_set = first_set.first_set[repr(seq)]
				for sym in _first_set.all_symbols():
					if sym.is_vt():
						if repr(sym) in M[repr(p.sym_left)]:
							l, s = M[repr(p.sym_left)][repr(sym)]
							if repr(l) != repr(p.sym_left) or repr(s) != repr(seq):
								print 'Current First Seq is %s -> %s Set is %s'%(repr(p.sym_left), repr(seq),repr(_first_set))
								print 'M[%s, %s] = %s already exists!'%(repr(p.sym_left), repr(sym), repr((l, s)))
								print 'ERRRRRRRRRRRRRRRRRRRRRRRRRRRR'
								return
						M[repr(p.sym_left)][repr(sym)] = (p.sym_left, seq)
						continue
					
					if repr(sym) == repr(SymbolSequence([])):
						for fsym in follow_set[repr(p.sym_left)].all_symbols():
							if repr(fsym) in M[repr(p.sym_left)]:
								print 'M[%s, %s] already exists!'%(repr(p.sym_left), repr(fsym))
								print 'ERRRRRRRRRRRRRRRRRRRRRRRRRRRRR'
								return
							M[repr(p.sym_left)][repr(fsym)] = (p.sym_left, seq)
		self.M = M
		return M			

	def check_json(self, json_str):
		stack = ['#', self.symbols[SYM_OBJ]] + [None]*1000
		stack_top = 1
		a_json_str = json_str + '#'
		buffer_ptr = 0
		ret = False
		while True:
			token = a_json_str[buffer_ptr]
			top_token = stack[stack_top]
			if token == repr(top_token) and token == '#':
				ret = True
				print 'ok'
				break

			if top_token.is_vt() and top_token.repr() == token:
				print '#top_token %s = token %s '%(top_token.repr(), token)
				print ' pop stack: ', top_token.repr()
				stack_top -= 1
				buffer_ptr += 1
				continue

			if top_token.is_vt() and top_token.repr() != token:
				ret = False
				print ' token %s != top_token %s and top_token is vt! '%(token, top_token.repr())
				break

			if token not in self.M[top_token.repr()]:
				ret = False
				print ' token %s not in M[%s] !'%(token, top_token.repr())
				break

			print '#top_token %s , token %s '%(top_token.repr(), token)
			seq = self.M[top_token.repr()][token][1]
			print ' hit production [%s,%s]: '%(top_token.repr(), token), self.M[top_token.repr()][token]
			print ' pop stack: ', top_token.repr()
			stack_top -= 1
			tseq = list(seq.symbols())
			tseq.reverse()
			for sym in tseq:
				print ' push stack: ', sym
				stack_top += 1
				stack[stack_top] = sym

			

a = JsonGramma()
print '----------------------- RAW --------------------------'
a.dump()
#a.remove_indirect_left_recursion()
print '----------------------- After adjust common left symbol --------------------------'
a.adjust_common_left_symbol()
a.dump()
print '----------------------- After adjust common left symbol --------------------------'
a.adjust_common_left_symbol()
a.dump()
#print '----------------------- after remove left recursion --------------------------'
#a.dump()
print '----------------------- Check LL1 --------------------------'
a.check_LL1()
print '------------------------------- test ------------------------------'
json = '{"a":"dsadsadas", "b":0012312,  "c":1231.2e213}'
a.check_json(json)

