import pyfiletools.parse
import pyfiletools.load
import pyfiletools.write


def parse(data_list, type="str"):
	if type == "float":
		return parse.pfloat(data_list)
	elif type == "int":
		return parse.pint(data_list)
	else:
		return parse.pstr(data_list)
