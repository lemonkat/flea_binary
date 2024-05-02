def to_binary(d:int, length:int = -1) -> list[bool]:
	result = [int(x) == 1 for x in bin(d)[2:]]
	if length == -1:
		return result
	return ([False] * (length - len(result))) + result

def to_int(b:list[bool]) -> int:
	total = 0
	for i in range(len(b)):
		total += (2 ** i) * b[len(b) - i - 1]
	return total

if __name__ == "__main__":
	print(to_int([True, False, False, True, True]))