from jira import JIRA

from pytools.display import ColumnDefinition, display_table

__headers = [
	ColumnDefinition("Key", width=10),
	ColumnDefinition("Summary", width=90),
	ColumnDefinition("Assignee", width=16, cell_style="conditional", cell_style_context={"Samuel Bourke" : "orange3"}),
	ColumnDefinition("Created", width=10, cell_style="age_warning", cell_style_context="7:28"),
	ColumnDefinition("Link", width=46)
]

def __issues_to_table_row(issues):
	"""
	Convert a list of Jira issue to rich table rows
	:param issues: A list of Jira issues
	:return: A list of table rows
	"""
	converted_issues = []
	for issue in issues:
		converted_issues.append(
			[issue.key, issue.fields.summary, issue.fields.assignee, issue.fields.created[:10], f"https://costcutter.jira.com/browse/{issue.key}"])
	return converted_issues


def search(query):
	"""
	Run a Jira query
	:param query: The JQL query
	:return: A list of Jira issues
	"""
	jira = JIRA("https://costcutter.jira.com/", basic_auth=('sam.bourke@costcutter.com', 'vhdQoeyUm3pg3OwnBxkp729C'))
	return jira.search_issues(query)

def display(issues, title=None):
	"""
	Display a list of Jira issues in a table
	:param issues: A list of Jira issues
	:param title: The title of the table
	"""
	display_table(__headers, __issues_to_table_row(issues), title=title)