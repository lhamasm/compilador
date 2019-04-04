ln = 1
erro = False
ehString = False
lines = []

palavras_reservadas = ['ATEH', 'BIT', 'DE', 'ENQUANTO', 'ESCREVA', 'FIM', 'FUNCAO', 'INICIO', 'INTEIRO', 'LEIA', 'NULO', 'PARA', 'PARE', 'REAL', 'RECEBA', 'SE', 'SENAO', 'VAR', 'VET']
tokens = []

def estado_inicial(index, line):
	global erro
	global ehString
	global ln

	if index < len(line):
		if ehString:
			estado_tres(index, line)
		else:
			if line[index] == '*':
				estado_dois(index + 1, line)
			elif line[index] == '"':
				estado_tres(index + 1, line)
			elif line[index] >= '0' and line[index] <= '9':
				estado_quatro(index, line)
			elif (line[index] >= 'a' and line[index] <= 'z') or (line[index] >= 'A' and line[index] <= 'Z'):
				estado_cinco(index, line)
			elif line[index] == '>':
				estado_seis(index + 1, line)
			elif line[index] == '<':
				estado_sete(index + 1, line)
			elif line[index] == '.' or line[index] == ':' or line[index] == ';' or line[index] == '+' or line[index] == '-' or line[index] == '/' or line[index] == '%' or line[index] == '(' or line[index] == ')' or line[index] == '[' or line[index] == ']' or line[index] == '=' or line[index] == '&' or line[index] == '|' or line[index] == '!':
				estado_oito(index, line)
			elif line[index] == ' ' or line[index] == '\n' or line[index] == '\t':
				if line[index] == '\n':
					ln += 1

				estado_inicial(index+1, line)
			else:
				if index == 0:
					index += 1

				print ln, index
				erro = True
				estado_inicial(index + 1, line)

def estado_dois(index, line):
	if index < len(line):
		if line[index] == '*':
			tokens.append(('**', '**'))
			estado_inicial(index + 1, line)
		else:
			tokens.append(('*', '*'))
			estado_inicial(index, line)

def estado_tres(index, line):
	global erro
	global ehString
	global ln
	global lines

	if index < len(line):
		count = 0
		string = '"'

		while index + count < len(line) and count < 513 and line[index + count] != '"':
			string += line[index + count]
			count += 1

		if count == 513:
			if line[index + count] == '"':
				tokens.append(('STRING', string + '"'))
				estado_inicial(index + count + 1, line)
			else:
				print ln, index + count - 1
				erro = True
				estado_inicial(index + count, line)
		elif index + count >= len(line):
			#print ln, index + count - 1
			#erro = True
			ehString = True
			return
		else:
			tokens.append(('STRING', string + '"'))
			ehString = False
			estado_inicial(index + count + 1, line)
	else:
		if ln == len(lines):
			erro = True
			print ln, index - 1
		else:
			ehString = True
			return

def estado_quatro(index, line):
	global erro
	global ln

	if index < len(line):
		count = 0
		number = ''

		while index + count < len(line) and count < 513:
			if line[index + count] >= '0' and line[index + count] <= '9':
				number += line[index + count]
				count += 1
			else:
				break

		if count == 513:
			if line[index + count] >= '0' and line[index + count] <= '9':
				print ln, index + count - 1
				erro = True
			else:
				tokens.append(('NUMBER', number))

			estado_inicial(index + count, line)

		elif index + count >= len(line):
			tokens.append(('NUMBER', number))
		elif line[index + count] == ',':
			if index + count + 1 < len(line):
				if line[index + count + 1] >= '0' and line[index + count + 1] <= '9':
					estado_nove(index + count + 1, number + ',', line)
				else:
					if line[index + count + 1] == ',':
						print ln, index + count + 1
						print ln, index + count + 2
						erro = True
						tokens.append(('NUMBER', number + ','))
						estado_inicial(index + count + 2, line)
					else:
						tokens.append(('NUMBER', number + ','))
						estado_inicial(index + count + 1, line)
			else:
				tokens.append(('NUMBER', number + ','))
				return

		elif (line[index + count] >= 'a' and line[index + count] <= 'z') or (line[index + count] >= 'A' and line[index + count] <= 'Z'):
			print ln, index+count
			erro = True
			estado_inicial(index + count + 1, line)
		elif line[index + count] == '\t' or line[index + count] == '\n':
			tokens.append(('NUMBER', number))
			estado_inicial(index + count + 1, line)
		else:
			estado_inicial(index + count, line)		

def estado_cinco(index, line):
	global erro
	global ln

	if index < len(line):
		count = 0
		identifier = ''

		while index + count < len(line) and count < 513:
			if (line[index + count] >= 'a' and line[index + count] <= 'z') or (line[index + count] >= 'A' and line[index + count] <= 'Z') or (line[index + count] >= '0' and line[index + count] <= '9'):
				identifier += line[index + count]
				count += 1
			else:
				if identifier not in palavras_reservadas:
					tokens.append(('ID', identifier))
				else:
					tokens.append((identifier, identifier))
				
				break

		if count == 513:
			if (line[index + count] >= 'a' and line[index + count] <= 'z') or (line[index + count] >= 'A' and line[index + count] <= 'Z') or (line[index + count] >= '0' and line[index + count] <= '9'):
				print ln, index + count - 1
				erro = True
			
			estado_inicial(index + count, line)
		elif index + count >= len(line):
			if identifier not in palavras_reservadas:
				tokens.append(('ID', identifier))
			else:
				tokens.append((identifier, identifier))
		else:
			estado_inicial(index + count, line)

def estado_seis(index, line):
	if index < len(line):
		if line[index] == '=':
			tokens.append(('>=', '>='))
			estado_inicial(index + 1, line)
		else:
			tokens.append(('>', '>'))
			estado_inicial(index, line)

def estado_sete(index, line):
	if index < len(line):
		if line[index] == '-':
			tokens.append(('<-', '<-'))
			estado_inicial(index + 1, line)
		elif line[index] == '=':
			tokens.append(('<=', '<='))
			estado_inicial(index + 1, line)
		elif line[index] == '>':
			tokens.append(('<>', '<>'))
			estado_inicial(index + 1, line)
		else:
			estado_inicial(index, line)

def estado_oito(index, line):
	if index < len(line):
		tokens.append((line[index], line[index]))
		estado_inicial(index + 1, line)

def estado_nove(index, number, line):
	if index < len(line):
		global erro
		global ln

		count = 0

		while index + count < len(line) and count + index < 513:
			if line[index + count] >= '0' and line[index + count] <= '9':
				number += line[index + count]
				count += 1
			else:
				break

		if index + count == 513:
			if line[index + count] >= '0' and line[index + count] <= '9':
				print ln, index + count - 1
				erro = True
			else:
				tokens.append(('NUMBER', number))
		
			estado_inicial(index + count, line)
		elif index + count >= len(line):
				tokens.append(('NUMBER', number))
		else:
			if line[index + count] == ',':
				print ln, index + count
				print ln, index + count + 1
				erro = True
				estado_inicial(index + count + 1, line)
			else:
				tokens.append(('NUMBER', number))
				estado_inicial(index + count, line)
		

if __name__ == '__main__':
	# file = open('codigo.txt', 'r')
	#lines = file.readlines()

	ok = True

	while True:
		try:
			lines.append(raw_input())
		except EOFError:
			break
	
	for line in lines:
		for index in range(0, len(line)):
			if (ord(line[index]) < 9 or ord(line[index]) > 10) and (ord(line[index]) < 32 or ord(line[index]) > 126):
				print 'ARQUIVO INVALIDO'
				ok = False
				break
		if not ok:
			break

	if ok:
		for line in lines:
			estado_inicial(0, line)
			ln += 1

		if not erro:
			print 'OK\n'
			tokens.append(('eof', 'eof'))

				