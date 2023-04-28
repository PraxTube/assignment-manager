from rich import print
from rich.table import Table as RichTable
import inquirer


def print_table(table_headers, table_rows):
    if len(table_headers) != len(table_rows[0]):
        raise ValueError(
            "The length of the given lists must match",
            table_headers,
            table_rows,
        )

    table = RichTable(*table_headers)
    for row in table_rows:
        table.add_row(*row)
    print(table)


def confirmation_prompt(msg=""):
    if msg != "":
        print(msg)

    if binary_prompt("Are you sure you want to continue?"):
        return True
    print("[bold]Aborting...[/bold]")
    return False


def add_assignment_response():
    questions = [
        inquirer.Text("name", message="Name of course"),
        inquirer.Text("start_date", message="First published date"),
        inquirer.Text("end_date", message="When is the deadline"),
        inquirer.Text(
            "torus", message="How many days until the next assignment (torus)"
        ),
        inquirer.Text("amount", message="Number of total assignments"),
    ]
    answers = inquirer.prompt(questions)
    return (
        answers["name"],
        answers["start_date"],
        answers["end_date"],
        int(answers["torus"]),
        int(answers["amount"]),
    )


def binary_prompt(msg):
    question = [
        inquirer.List(
            "answer",
            message=msg,
            choices=["Yes", "No"],
        )
    ]
    if inquirer.prompt(question)["answer"] == "Yes":
        return True
    return False


def list_prompt(choices, msg):
    question = [
        inquirer.List(
            "answer",
            message=msg,
            choices=choices,
        ),
    ]
    return inquirer.prompt(question)["answer"]


def update_assignment_response(cycle_choices, progress_choices):
    questions = [
        inquirer.List(
            "cycle",
            message="Which cycle do you want to update?",
            choices=cycle_choices,
        ),
        inquirer.List(
            "progress", message="New progress status", choices=progress_choices
        ),
    ]
    answers = inquirer.prompt(questions)
    cycle = cycle_choices.index(answers["cycle"])
    progress = progress_choices.index(answers["progress"])

    return (cycle, progress)


def rename_assignment_response():
    question = [
        inquirer.Text("name", message="What's the new name of the course?")
    ]
    return inquirer.prompt(question)["name"]
