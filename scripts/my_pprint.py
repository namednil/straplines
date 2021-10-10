import json

from pprint import pprint

def insert_indent(t, width=80):
	r = ["\t"]
	line_length = 0
	for c in t:
		r.append(c)
		if c == "\n":
			r.append("\t")
			line_length = 0
		elif c.isspace() and line_length > width:
			r.append("\n\t")
			line_length = 0
		else:
			line_length += 1
	return "".join(r)

while True:
	try:
		l = input()
		s = json.loads(l)
		#pprint(s, width=150)
		for key in sorted(s.keys()):
			print(key)
			print(insert_indent(str(s[key])))
			print()
		print(80*"=")
			
	except EOFError:
		break
	
