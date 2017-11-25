import random
matrix = [[0] * 4 for i in range(4)]

def gen_rnd(p):
	fix = random.randint(0, p-1)
	return lambda i: random.randint(1, 2) * 2 if fix == i else 0
	
def shink(line):
	return [num for num in line if num] + [0] * line.count(0)
	
def eval4(line):
	line = shink(line)
	for i in range(3):
		if line[i] == line[i+1]:
			line[i] *= 2
			line[i+1] = 0
		line = shink(line)
	return line
	
def tranpose(mat):
	return [list(line) for line in zip(*mat)]
	
def gravity(vec, reverse):
	global matrix
	if vec:
		matrix = tranpose(matrix)
	if reverse:
		matrix = [list(reversed(line)) for line in matrix]
	
	
	matrix = [eval4(line) for line in matrix]
	
	zeros = sum(line.count(0) for line in matrix)
	rnd = gen_rnd(zeros)
	c = 0
	for i in range(4):
		for j in range(4):
			if matrix[i][j] == 0:
				matrix[i][j] = rnd(c)
				c += 1
	
	
	if reverse:
		matrix = [list(reversed(line)) for line in matrix]
	if vec:
		matrix = tranpose(matrix)
	return matrix
	
def print_matrix(mat):
	for line in mat:
		print(line)
		
while True:
	dir = input()
	if dir == 'a':
		gravity(False, False)
	elif dir == 'd':
		gravity(False, True)
	elif dir == 'w':
		gravity(True, False)
	elif dir == 's':
		gravity(True, True)
	print_matrix(matrix)
	
	