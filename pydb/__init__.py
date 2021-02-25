import json

import mysql.connector
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

import pyfiletools as ft
from pydb.QueryResult import QueryResult

__connectors = {}
__default_connector = None


def get_connector(name):
	if name in __connectors:
		return __connectors[name]
	else:
		config = json.loads(' '.join(ft.load.file("/home/sam/.sql/mysqlConfig.json")))
		for connection in config:
			if connection["name"] == name:
				__connectors[name] = mysql.connector.connect(
					host=connection["host"],
					port=connection["port"],
					user=connection["user"],
					password=connection["password"],
					autocommit=True
				)
				break
		return __connectors[name]


def set_default_connection(name):
	global __default_connector
	__default_connector = name


def __get_default_connection():
	return get_connector(__default_connector)


def query(query_string, connection=None, limit=None):
	if connection is None:
		connection = __get_default_connection()
	else:
		connection = get_connector(connection)

	mycursor = connection.cursor()
	mycursor.execute(query_string)

	result = QueryResult(mycursor.fetchall(), mycursor.column_names)

	mycursor.close()

	return result


def query_table(query_string, connection=None, limit=None):
	result = query(query_string, connection, limit)
	table = Table()

	for column in result.headers:
		table.add_column(column)

	for row in result.data:
		table.add_row(*map(str, row))

	return table


def query_formatted(query_string, connection=None, limit=None):
	Console().print(query_table(query_string, connection, limit))


def copy_data(table, source, dest, suffix=None, full_query=None, task=None, progress=None):
	if full_query is None:
		result = query(f"SELECT * FROM {table} {suffix};", source)
	else:
		result = query(full_query, source)
	thing = get_connector(dest).cursor()

	insertHeaders = f"{result.headers}".replace("\'", "")

	placeholder = "(%s"
	if len(result.data) != 0:
		for _ in range(len(result.data[0]) - 1):
			placeholder += ",%s"
		placeholder += ")"

		chunkyList = list(chunks(list(result.data), 100))
		for x in range(len(chunkyList)):
			thing.executemany(f"INSERT INTO {table} {insertHeaders} values {placeholder}", chunkyList[x])
			if progress is not None:
				progress.update(task, advance=100/len(chunkyList))
	if progress is not None:
		progress.update(task, completed=100)
	thing.close()


def copy_group_data(tables, source, dest):

	stringlen = len(max(tables, key=len))

	for table in reversed(tables):
		query(f"DELETE FROM {table}", dest)

	for tableGroup in list(chunks(list(tables), 8)):
		with Progress() as progress:
			tasks = []
			for table in tableGroup:
				tasks.append([progress.add_task(f"[green]{table.ljust(stringlen)}"), table])
			for task in tasks:
				copy_data(task[1], source, dest, progress=progress, task=task[0])


def chunks(lst, n):
	"""Yield successive n-sized chunks from lst."""
	for i in range(0, len(lst), n):
		yield lst[i:i + n]
