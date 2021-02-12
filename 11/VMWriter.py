kind_to_segment = {'static': 'static',
                   'field': 'this',
                   'arg': 'argument',
                   'var': 'local'}

class VMWriter:


	def __init__(self, ostream):
		
		self.ostream = ostream
		self.label_count = 0

	def write_if(self, label):
	
		self.ostream.write('not\n') # Negate to jump if the conditions doesn't hold
		self.ostream.write('if-goto {}\n'.format(label))

	def write_goto(self, label):
		
		self.ostream.write('goto {}\n'.format(label))

	def write_label(self, label):
	
		self.ostream.write('label {}\n'.format(label))

	def write_function(self, jack_subroutine):
		
		class_name = jack_subroutine.jack_class.name
		name = jack_subroutine.name
		local_vars = jack_subroutine.var_symbols
		subroutine_type = jack_subroutine.subroutine_type

		self.ostream.write('function {}.{} {}\n'.format(class_name, name, local_vars))

	def write_return(self):
		
		self.ostream.write('return\n')

	def write_call(self, class_name, func_name, arg_count):
		
		self.ostream.write('call {0}.{1} {2}\n'.format(
				class_name, func_name, arg_count
			))

	def write_pop_symbol(self, jack_symbol):
		
		kind = jack_symbol.kind
		offset = jack_symbol.id # the offset in the segment

		segment = kind_to_segment[kind]
		self.write_pop(segment, offset)

	def write_push_symbol(self, jack_symbol):
		
		kind = jack_symbol.kind
		offset = jack_symbol.id # the offset in the segment

		segment = kind_to_segment[kind]
		self.write_push(segment, offset)

	def write_pop(self, segment, offset):
		
		self.ostream.write('pop {0} {1}\n'.format(segment, offset))

	def write_push(self, segment, offset):
		
		self.ostream.write('push {0} {1}\n'.format(segment, offset))

	def write(self, action):
		
		self.ostream.write('{}\n'.format(action))

	def write_int(self, n):
		
		self.write_push('constant', n)

	def write_string(self, s):
	
		s = s[1:-1]
		self.write_int(len(s))
		self.write_call('String', 'new', 1)
		for c in s:
			self.write_int(ord(c))
			self.write_call('String','appendChar', 2)
