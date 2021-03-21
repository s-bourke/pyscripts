class ColumnDefinition:
	"""
	A class for defining a column in a rich table
	:param header: The header name
	:param header_style: The header formatting style
	:param cell_style: Column data formatting style
	:param cell_style_context: Context for the cell_style
	:param justify: Text justification
	:param width: Width of the column
	"""
	def __init__(self, header, header_style=None, cell_style=None, cell_style_context=None, justify="left", width=None):
		self.header = header
		self.header_style = header_style
		self.cell_style = cell_style
		self.cell_style_context = cell_style_context
		self.justify = justify
		self.width = width

