import math



def factorial(n: int) -> int:
	if (n < 0):
		raise ArithmeticError("argument value must be bigger then zero!")
	if (n < 2):
		return 1
	total = 1
	for i in range(1, n + 1):
		total *= i
	return total


def sum(*args):	return sum(args)
def max(*args):	return max(args)
def min(*args):	return min(args)
