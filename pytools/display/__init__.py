# Functions
from rich import box
from rich.console import Console
from rich.table import Table

from pytools.display.ColumnDefinition import ColumnDefinition

__default_cell_style = "[cyan]"
__null_cell_style = "[bright_black]<null>"


def table(headers, rows, title=None):
	table = Table(title=title, box=box.ROUNDED, border_style="b blue")
	for column in headers:
		if not isinstance(column, ColumnDefinition):
			table.add_column(column, justify="left")
		else:
			table.add_column(column.header)
	for row in rows:
		table.add_row(*map(str, __format_row(list(row), headers)), )
	return table


def display_table(headers, rows, title=None):
	Console().print(table(headers, rows, title))


def __format_row(row, columns):
	for i in range(len(row)):
		row[i] = __format_value(row[i], columns[i])
	return row


def __format_value(value, column):
	if value is None:
		return __null_cell_style
	if not isinstance(column, ColumnDefinition) or column.cell_style is None:
		return value
	if column.cell_style == "standard":
		return f"[{column.cell_style_context}]{value}"
	if column.cell_style == "pos_nev_num":
		return __apply_pos_nev_num(value)
	if column.cell_style == "conditional":
		return __apply_conditional(value, column.cell_style_context)
	return value


def __apply_pos_nev_num(value):
	if value > 0:
		return f"[green]{value}"
	if value < 0:
		return f"[red]{value}"
	return __default_cell_style + str(value)


def __apply_conditional(value, context):
	if str(value) in context:
		return f"[{context[str(value)]}]{value}"
	return __default_cell_style + str(value)
