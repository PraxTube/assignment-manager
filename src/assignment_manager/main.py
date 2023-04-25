from datetime import datetime, timedelta

import typer

from assignment_manager import assignments


app = typer.Typer()
backup_app = typer.Typer()
app.add_typer(backup_app, name="backup")


@app.command()
def add():
    assignments.add_assignment()


@app.command()
def show(one: bool = False):
    if one:
        assignments.show_specific_assignment()
    else:
        assignments.show_all_assignments()


@app.command()
def update():
    assignments.update_assignment()


@app.command()
def remove():
    assignments.remove_assignment()


@backup_app.command("copy")
def copy_backup():
    """
    Copy the data file. This will OVERWRITE the BACKUP file.
    """
    assignments.copy_backup()


@backup_app.command("paste")
def paste_backup():
    """
    Paste the backup file. This will OVERWRITE the DATA file.
    """
    assignments.paste_backup()


def main():
    app()


if __name__ == "__main__":
    main()
