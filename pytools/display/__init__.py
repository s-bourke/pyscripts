# Functions
from rich import box
from rich.console import Console
from rich.table import Table

from pytools.display.ColumnDefinition import ColumnDefinition


def table(headers, rows, title=None):
	table = Table(header_style="b orange3", title=title, box=box.ROUNDED, border_style="b blue")
	for column in headers:
		if not isinstance(column, ColumnDefinition):
			table.add_column(column, style="cyan")
		else:
			print(column.cell_style)
			table.add_column(column.header)
	for row in rows:
		table.add_row(*map(str, __format_row(list(row), headers)))
	return table


def display_table(headers, rows, title=None):
	Console().print(table(headers, rows, title))


def __format_row(row, columns):
	for i in range(len(row)):
		row[i] = __format_value(row[i], columns[i])
	return row


def __format_value(value, column):
	if not isinstance(column, ColumnDefinition) or column.cell_style is None:
		return value
	if column.cell_style == "pos_nev_num":
		return __apply_pos_nev_num(value)
	if column.cell_style == "conditional":
		return __apply_conditional(value, column.cell_style_context)
	return value


def __apply_pos_nev_num(value):
	if value > 0:
		return "[green]" + str(value)
	if value < 0:
		return "[red]" + str(value)
	return "[cyan]" + str(value)


def __apply_conditional(value, context):
	if str(value) in context:
		return "[" + context[str(value)] + "]" + str(value)
	return "[cyan]" + str(value)
