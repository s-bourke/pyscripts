from jira import JIRA

from pytools.display import ColumnDefinition, display_table

__headers = [
	ColumnDefinition("Key", width=10),
	ColumnDefinition("Summary", width=90),
	ColumnDefinition("Assignee", width=16, cell_style="conditional", cell_style_context={"Samuel Bourke": "orange3"}),
	ColumnDefinition("Created", width=10, cell_style="age_warning", cell_style_context="7:28"),
	ColumnDefinition("Link", width=46)
]


def __issue_to_table_row(issues):
	converted_issues = []
	for issue in issues:
		converted_issues.append(
			[issue.key, issue.fields.summary, issue.fields.assignee, issue.fields.created[:10], f"https://costcutter.jira.com/browse/{issue.key}"])
	return converted_issues


def search(query):
	jira = JIRA("https://costcutter.jira.com/", basic_auth=('sam.bourke@costcutter.com', 'vhdQoeyUm3pg3OwnBxkp729C'))
	return jira.search_issues(query)


def display(issues, title=None):
	display_table(__headers, __issue_to_table_row(issues), title=title)
