import pyfiletools.load
import pyfiletools.parser
import pyfiletools.write


def parse(data_list, type="str"):
	if type == "float":
		return parser.pfloat(data_list)
	elif type == "int":
		return parser.pint(data_list)
	else:
		return parser.pstr(data_list)
