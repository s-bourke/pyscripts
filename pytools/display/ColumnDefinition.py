class ColumnDefinition:
	def __init__(self, header, header_style=None, cell_style=None, cell_style_context=None, justify="left", width=None):
		self.header = header
		self.header_style = header_style
		self.cell_style = cell_style
		self.cell_style_context = cell_style_context
		self.justify = justify
		self.width = width
