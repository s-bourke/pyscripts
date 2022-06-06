from jira import JIRA
from collections import defaultdict

from pytools.cli import run_pipe
from pytools.display import ColumnDefinition, display_table
from pyfiletools import parse
from pyfiletools import load

__headers = [
	ColumnDefinition("Key", width=10),
	ColumnDefinition("Summary", width=85),
	ColumnDefinition("Status", width=15),
	ColumnDefinition("Assignee", width=15, cell_style="conditional", cell_style_context={"Samuel Bourke": "orange3"}),
	ColumnDefinition("Created", width=10, cell_style="age_warning", cell_style_context="7:28"),
	ColumnDefinition("Link", width=55)
]

__jira_client = None

def __issues_to_table_row(issues):
	"""
	Convert a list of Jira issue to rich table rows
	:param issues: A list of Jira issues
	:return: A list of table rows
	"""
	converted_issues = []
	for issue in issues:
		converted_issues.append(
			[issue.key, issue.fields.summary, issue.fields.status, issue.fields.assignee, issue.fields.created[:10], f"https://nidigitalsolutions.jira.com//browse/{issue.key}"])
	return converted_issues

def __get_jira():

    global __jira_client

    if __jira_client is None:
        token = run_pipe("cat secret", cwd="/Users/sbourke/.jira.d").split("=", 1)[1]

        config_file = parse(load.file("/Users/sbourke/.jira.d/config.yml"))
        config = defaultdict(list)

        for k, v in config_file:
            config[k].append(v)

       	__jira_client = JIRA(config.get("endpoint:")[0], basic_auth=(config.get("user:")[0], token))

    return __jira_client

def search(query):
	"""
	Run a Jira query
	:param query: The JQL query
	:return: A list of Jira issues
	"""

	return __get_jira().search_issues(query)


def display(issues, title=None):
	"""
	Display a list of Jira issues in a table
	:param issues: A list of Jira issues
	:param title: The title of the table
	"""
	display_table(__headers, __issues_to_table_row(issues), title=title)