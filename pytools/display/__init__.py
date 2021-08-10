# Functions
from datetime import datetime, timedelta

import dateutil.parser
from rich import box
from rich.console import Console
from rich.table import Table

from pytools.display.ColumnDefinition import ColumnDefinition

__default_cell_style = "[cyan]"
__null_cell_style = "[bright_black]<null>"


def table(headers, rows, title=None):
	"""
	Create rich table object
	:param headers: A list of table headers
	:param rows: A list of row data
	:param title: Title of the table
	:return: The rich table object
	"""
	table = Table(title=title, box=box.ROUNDED, border_style="b blue")
	for column in headers:
		if not isinstance(column, ColumnDefinition):
			table.add_column(column, justify="left")
		else:
			table.add_column(column.header, width=column.width, justify=column.justify)
	for row in rows:
		table.add_row(*map(str, __format_row(list(row), headers)), )
	return table


def display_table(headers, rows, title=None):
	"""
	Display a pretty table
	:param headers: A list of table headers
	:param rows: A list of row data
	:param title: Title of the table
	"""
	Console().print(table(headers, rows, title))


def __format_row(row, headers):
	"""
	Format a table row. This will apply any formatting rules determined
	by the header definitions
	:param row: Row data as a list
	:param headers: Column headers as a list
	:return: The formatted row
	"""
	for i in range(len(row)):
		row[i] = __format_value(row[i], headers[i])
	return row


def __format_value(value, header):
	"""
	Formats a value for a table cell. If column header is not a ColumnDefinition or
	has no cell_style defined will use default format
	:param value: The value to be formatted
	:param header: The column header.
	:return: The formatted value
	"""
	if value is None:
		return __null_cell_style
	if not isinstance(header, ColumnDefinition) or header.cell_style is None:
		return __default_cell_style + str(value)
	if header.cell_style == "standard":
		return f"[{header.cell_style_context}]{value}"
	if header.cell_style == "pos_nev_num":
		return __apply_pos_nev_num(value)
	if header.cell_style == "conditional":
		return __apply_conditional(value, header.cell_style_context)
	if header.cell_style == "age_warning":
		return __apply_age_warning(value, header.cell_style_context)
	if header.cell_style == "reverse_age_warning":
		return __apply_reverse_age_warning(value, header.cell_style_context)
	return __default_cell_style + str(value)


def __apply_pos_nev_num(value):
	"""
	Format positive numbers as green
	Format negative numbers as red
	Format zero as default
	:param value: The value to be formatted
	:return: The formatted value
	"""
	if value > 0:
		return f"[green]{value}"
	if value < 0:
		return f"[red]{value}"
	return __default_cell_style + str(value)


def __apply_conditional(value, context):
	"""
	Apply conditional formatting. If the value is in the column context
	then set specified formatting
	:param value: The value to be formatted
	:param context: Dictionary of conditional values and formatting.
			E.g {"FirstMatch" : "orange3", "SecondMatch" : "blue"}
	:return: The formatted value
	"""
	if str(value) in context:
		return f"[{context[str(value)]}]{value}"
	return __default_cell_style + str(value)


def __apply_age_warning(value, context):
	"""
	Apply colour formatting if date is over given amount in the past
	:param value: The value to be formatted
	:param context: Age boundaries for highlighting First value if first age boundary,
			second value is second boundary. E.g "7:28"
	:return: The formatted value
	"""
	if dateutil.parser.isoparse(str(value)) < datetime.now() - timedelta(days=int(context.split(":")[1])):
		return f"[red]{str(value)}"
	if dateutil.parser.isoparse(str(value)) < datetime.now() - timedelta(days=int(context.split(":")[0])):
		return f"[yellow]{str(value)}"
	return f"[green]{str(value)}"

def __apply_reverse_age_warning(value, context):
	"""
	Apply colour formatting if date is over given amount in the past
	:param value: The value to be formatted
	:param context: Age boundaries for highlighting First value if first age boundary,
			second value is second boundary. E.g "7:28"
	:return: The formatted value
	"""
	if dateutil.parser.isoparse(str(value)) < datetime.now() - timedelta(days=int(context.split(":")[1])):
		return f"[green]{str(value)}"
	if dateutil.parser.isoparse(str(value)) < datetime.now() - timedelta(days=int(context.split(":")[0])):
		return f"[yellow]{str(value)}"
	return f"[red]{str(value)}"
