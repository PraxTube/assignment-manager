from rich import print
from rich.table import Table as RichTable
import inquirer


def print_table(table_headers, table_rows):
    if len(table_headers) != len(table_rows[0]):
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


def add_assignment_response():
    questions = [
      inquirer.Text("name", message="Name of course"),
      inquirer.Text("start_date", message="First published date"),
      inquirer.Text("end_date", message="When is the deadline"),
      inquirer.Text("torus", message="How many days until the next assignment (torus)"),
      inquirer.Text("amount", message="Number of total assignments"),
    ]
    answers = inquirer.prompt(questions)
    return (
        answers["name"],
        answers["start_date"],
        answers["end_date"],
        int(answers["torus"]),
        int(answers["amount"])
    )


def update_assignment_response_course(course_choices):
    question_course = [
        inquirer.List(
            "name",
            message="Which course do you want to update?",
            choices=course_choices
        ),
    ]
    return inquirer.prompt(question_course)["name"]


def update_assignment_response(cycle_choices, progress_choices):
    questions = [
        inquirer.List(
            "cycle",
            message="Which cycle do you want to update?",
            choices=cycle_choices
        ),
        inquirer.List(
            "progress",
            message="New progress status",
            choices=progress_choices
        ),
    ]
    answers = inquirer.prompt(questions)
    cycle = cycle_choices.index(answers["cycle"])
    progress = progress_choices.index(answers["progress"])

    return (cycle, progress)
