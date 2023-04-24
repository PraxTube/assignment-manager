from datetime import datetime, timedelta

import typer

from assignment_manager import assignments


app = typer.Typer()


@app.command()
def add():
    assignments.add_assignment()


@app.command()
def show(name=""):
    if name == "":
        assignments.show_all_assignments()
        return
    assignments.show_specific_assignment(name)


@app.command()
def update():
    assignments.update_assignment()


@app.command()
def remove():
    assignments.remove_assignment()


def main():
    app()


if __name__ == "__main__":
    main()
