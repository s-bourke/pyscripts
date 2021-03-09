def file(filename, values=None, separator=","):
	"""
	Write 2d array to file.
	filename: string pointing to file relative to current directory
	values: array of data values ([[item1,item2, ...],[item3, item4, ...], ...])
	"""
	if values is None:
		values = []
	f = open(filename, "w")
	for i in range(0, len(values)):
		for j in range(0, len(values[i])):
			f.write(str(values[i][j]))
			if j != len(values[i]) - 1:
				f.write(separator)
		if i != len(values):
			f.write("\n")
	f.close()
	return
