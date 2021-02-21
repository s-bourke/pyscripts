def pfloat(data_list):
	"""
	Seperate list of data strings into individual float values.
	Remove items that cannot be cast to float.
	data_list: array of strings containing data ["num1_1 num1_2 ...","num2_1 num2 ...", ...]
	"""
	pop_num = []
	for i in range(0, len(data_list)):
		data_list[i] = data_list[i].split()
		for j in range(0, len(data_list[i])):
			try:
				float(data_list[i][j])
				data_list[i][j] = float(data_list[i][j])
			except ValueError:
				pop_num.append(i)
				break

	if pop_num != 0:
		for i in range(len(pop_num) - 1, -1, -1):
			data_list.pop(pop_num[i])

	if not data_list[len(data_list) - 1]:
		data_list.pop(len(data_list) - 1)

	return data_list


def pint(data_list):
	"""
	Seperate list of data strings into individual integer values.
	Remove items that cannot be cast to integer.
	data_list: array of strings containing data ["num1_1 num1_2 ...","num2_1 num2 ...", ...]
	"""
	pop_num = []
	for i in range(0, len(data_list)):
		data_list[i] = data_list[i].split()
		for j in range(0, len(data_list[i])):
			try:
				int(data_list[i][j])
				data_list[i][j] = pint(data_list[i][j])
			except ValueError:
				pop_num.append(i)
				break

	if (pop_num != 0):
		for i in range(len(pop_num) - 1, -1, -1):
			data_list.pop(pop_num[i])

	if not data_list[len(data_list) - 1]:
		data_list.pop(len(data_list) - 1)

	return data_list


def pstr(data_list):
	"""
	Seperate list of data strings into individual items.
	data_list: array of strings containing data ["num1_1 num1_2 ...","num2_1 num2 ...", ...]
	"""
	for i in range(0, len(data_list)):
		data_list[i] = data_list[i].split()

	return data_list
