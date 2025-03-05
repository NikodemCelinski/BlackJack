
def choose_move(move):
	return {
	'stay' : stay,
	'hit' : hit,
	'double down' : double_down,
	'split': split
	}

def convert_to_int(inpt):
	print(f"You entered: {repr(inpt)}")
	while True:
		try:
			int_value = int(inpt)
			break
		except ValueError:
			print(f"ValueError: {inpt} is not an int! Try again. Assigning -1")
			inpt = -1
	
	return int_value