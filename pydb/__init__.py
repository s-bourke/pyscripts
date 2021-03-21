import json

import mysql.connector
from rich.progress import Progress

import pyfiletools as ft
import pytools as pt
from pydb.QueryResult import QueryResult

__connectors = {}
__default_connector = None


def get_connector(name):
	"""
	Get a mysql connector by name. If connector does not exist, load
	from config file.
	:param name: Name of the connection in config file
	:return: The connector
	"""
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
	"""
	Set the default connector. This will be used if no connector is specified
	:param name: The name of the connector in the config file
	"""
	global __default_connector
	__default_connector = name


def __get_default_connection():
	"""
	Fetch the default connection set by set_default_connection
	:return: The default connection
	"""
	return get_connector(__default_connector)


def query(query_string, connection=None):
	"""
	Run a query
	:param query_string: The query as a string
	:param connection: The name of the connection. If not set will try to use default connection
	:return: The query result as a QueryResult object
	"""
	if connection is None:
		connection = __get_default_connection()
	else:
		connection = get_connector(connection)

	mycursor = connection.cursor()
	mycursor.execute(query_string)

	result = QueryResult(mycursor.fetchall(), mycursor.column_names)

	mycursor.close()

	return result


def query_table(query_string, connection=None, title=None, headers=None):
	"""
	Run a query and return the result as a rich table
	:param query_string: The query as a string
	:param connection: The name of the connection. If not set will try to use default connection
	:param title: The title of the table
	:param headers: The headers of the table, will use headers form query if not specified
	:return: A rich table object
	"""
	result = query(query_string, connection)
	return pt.display.table(headers or result.headers, list(result.data), title=title)


def query_formatted(query_string, connection=None, title=None, headers=None):
	"""
	Run a query and dislay the result as a rich table
	:param query_string: The query as a string
	:param connection: The name of the connection. If not set will try to use default connection
	:param title: The title of the table
	:param headers: The headers of the table, will use headers form query if not specified
	"""
	result = query(query_string, connection)
	pt.display.display_table(headers or result.headers, list(result.data), title=title)


def copy_data(table, source, dest, suffix=None, full_query=None, task=None, progress=None):
	"""
	Copy data from one instance to another. This will populate the destination tables
	with data extracted from the source.
	:param table: The name of the table to be copied
	:param source: The name of the source database from the config file
	:param dest: The name of the destination database from the config file
	:param suffix: Added to end of query if full query not specified. Allows Where clause, limits, orders etc
	:param full_query: Whole select query. Result headers must march destination table headers
	:param task: Rich task for updating visual component
	:param progress: Rich progress object for updating visual component
	"""
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
				progress.update(task, advance=100 / len(chunkyList))
	if progress is not None:
		progress.update(task, completed=100)
	thing.close()


def copy_group_data(tables, source, dest):
	"""
	Copy multiple tables from destination to source. This will delete the data in
	te destination and populate from the source. Entire tables will be copied.
	:param tables:  A list of the table names as strings. Must be in insert order.
	:param source: The name of the source database from the config file
	:param dest: The name of the destination database from the config file
	"""
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
	"""
	Yield successive n-sized chunks from list.
	:param lst: The list to be chunked
	:param n: The number of elements in each chunk
	:return: List of chunks as 2D Array
	"""
	for i in range(0, len(lst), n):
		yield lst[i:i + n]
