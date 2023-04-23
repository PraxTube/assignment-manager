from rich import print
from rich.table import Table as RichTable
import inquirer


def print_table(table_headers, table_rows):
    if len(table_headers) != len(table_rows):
        raise ValueError(
            "The length of the given lists must match", table_headers, table_rows
        )

    table = RichTable(*table_headers)
    for row in table_rows:
        table.add_row(*row)
    print(table)


def confirmation_prompt():
    question = [
        inquirer.List(
            "confirmation",
            message="Are you sure you want to continue?",
            choices=["Yes", "No"]
        )
    ]
    return inquirer.prompt(question)["confirmation"] == "Yes"
