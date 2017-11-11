data1 = data
key = ["A","A","B","B","C"]
value = [3,4,5,6,7]

x = {}
for a,b in zip(key,value):
	x.setdefault(a, x.get(a, 0) + b)