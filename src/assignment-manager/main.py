from datetime import datetime, timedelta

import typer


app = typer.Typer()


def generate_dates(start_date, deadline, torus, number_of_assignments):
    start = datetime.strptime(start_date, "%d.%m.%Y")
    end = datetime.strptime(deadline, "%d.%m.%Y")

    delta = timedelta(days=torus)
    dates = []

    for i in range(number_of_assignments):
        dates.append([start.strftime("%d.%m.%Y"), end.strftime("%d.%m.%Y"), 0])
        start += delta
        end += delta
    return dates


def add_assignment(name, start_date, deadline, torus, number_of_assignments):
    data = load_data()
    if name in data.keys():
        raise ValueError("Name already exists!", name)

    progress = generate_dates(start_date, deadline, torus, number_of_assignments)
    data[name] = progress
    write_data(data)


def update_assignment(name, cycle, progress):
    data = load_data()
    if name not in data.keys():
        raise ValueError("Name doesn't exist!", name)

    data[name][cycle][2] = progress
    write_data(data)


def remove_assignment(name):
    data = load_data()
    if name not in data.keys():
        raise ValueError("Name doesn't exist!", name)

    if not confirmation_prompt():
        print("[bold]Aborting...[/bold]")
        return

    data.pop(name)
    write_data(data)


@app.command()
def add():
    questions = [
      inquirer.Text("name", message="Name of course"),
      inquirer.Text("start_date", message="First published date"),
      inquirer.Text("end_date", message="When is the deadline"),
      inquirer.Text("torus", message="How many days until the next assignment (torus)"),
      inquirer.Text("amount", message="Number of total assignments"),
    ]
    answers = inquirer.prompt(questions)
    add_assignment(
        answers["name"],
        answers["start_date"],
        answers["end_date"],
        int(answers["torus"]),
        int(answers["amount"])
    )


@app.command()
def show(name=""):
    if name == "":
        show_all_assignments()
        return
    show_specific_assignment(name)


@app.command()
def update():
    data = load_data()
    question_course = [
        inquirer.List(
            "name",
            message="Which course do you want to update?",
            choices=data.keys()
        ),
    ]
    course = inquirer.prompt(question_course)["name"]

    questions = [
        inquirer.List(
            "cycle",
            message="Which cycle do you want to update?",
            choices=[d for d in data[course]]
        ),
        inquirer.List(
            "progress",
            message="New progress status",
            choices=[p.name for p in Progress]
        ),
    ]
    answers = inquirer.prompt(questions)
    cycle = [d for d in data[course]].index(answers["cycle"])
    progress = [p.name for p in Progress].index(answers["progress"])
    
    update_assignment(course, cycle, progress)


@app.command()
def remove(name):
    remove_assignment(name)


if __name__ == "__main__":
    app()
