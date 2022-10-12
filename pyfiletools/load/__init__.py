import pyfiletools as ft


def file(filename):
	"""
	Load data from file into array line by line.
	:param filename: string pointing to file relative to current directory
	:return: The content of the file as a list of strings
	"""
	with open(filename) as f:
		content = f.readlines()
	return content


def float(filename):
	"""
	Load data from file.
	Split each line into individual float values.
	Ignore values that cannot be cast to float.
	Return 2d Array
	filename: string pointing to file relative to current directory
	"""
	return ft.parser.pfloat(ft.load.file(filename))


def int(filename):
	"""
	Load data from file.
	Split each line into individual integer values.
	Ignore values that cannot be cast to integer.
	Return 2d Array
	filename: string pointing to file relative to current directory
	"""
	return ft.parser.pint(ft.load.file(filename))


def str(filename):
	"""
	Load data from file.
	Split each line into individual string values.
	Return 2d Array
	filename: string pointing to file relative to current directory
	"""
	return ft.parser.pstr(ft.load.file(filename))
