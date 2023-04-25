from datetime import datetime, timedelta

from assignment_manager.data import (
    Progress,
    load_data,
    write_data,
    data_file_empty,
    backup_file_empty,
    copy_backup as data_copy_backup,
    paste_backup as data_paste_backup,
)
from assignment_manager import io


def _find_next_deadline(assignment_data):
    current_date = datetime.today()
    for i, d in enumerate(assignment_data):
        if datetime.strptime(d[1], "%d.%m.%Y") >= current_date:
            return i
    return len(assignment_data) - 1


def show_all_assignments():
    data = load_data()
    table_headers = ["Name", "Start", "Deadline", "Progress"]
    table_rows = []
    for key in data:
        cycle = _find_next_deadline(data[key])
        table_rows.append(
            [
                key,
                data[key][cycle][0],
                data[key][cycle][1],
                Progress(data[key][cycle][2]).name,
            ]
        )
    io.print_table(table_headers, table_rows)


def show_specific_assignment():
    data = load_data()
    name = io.course_response(data.keys())

    table_headers = ["Start", "Deadline", "Progress"]
    table_rows = []
    for data_entry in data[name]:
        table_rows.append([data_entry[0], data_entry[1], Progress(data_entry[2]).name])
    io.print_table(table_headers, table_rows)


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


def add_assignment():
    params = io.add_assignment_response()

    if data_file_empty():
        data = {}
    else:
        data = load_data()

    if params[0] in data:
        raise ValueError("Name already exists!", name, data.keys())

    progress = generate_dates(params[1], params[2], params[3], params[4])
    data[params[0]] = progress
    write_data(data)


def update_assignment():
    data = load_data()
    name = io.course_response(data.keys())

    cycle_choices = [d for d in data[name]]
    progress_choices = [p.name for p in Progress]
    cycle, progress = io.update_assignment_response(cycle_choices, progress_choices)

    data[name][cycle][2] = progress
    write_data(data)


def rename_assignment():
    data = load_data()
    old_name = io.course_response(data.keys())
    new_name = io.rename_assignment_response()

    if new_name in data:
        raise ValueError("The name already exists!", new_name, data.keys())

    data[new_name] = data.pop(old_name)
    write_data(data)


def remove_assignment():
    data = load_data()
    name = io.course_response(data.keys())

    confirmation_msg = "This will delete [bold]ALL[/bold] data for the course: [bold]{}[/bold]\n".format(
        name
    )

    if not io.confirmation_prompt(confirmation_msg):
        return

    data.pop(name)
    write_data(data)


def copy_backup():
    if data_file_empty():
        raise ValueError("The data file is empty. No backup will be made.")

    confirmation_msg = "This will OVERWRITE the old BACKUP file if there is one."

    if not io.confirmation_prompt(confirmation_msg):
        return

    data_copy_backup()


def paste_backup():
    if backup_file_empty():
        raise ValueError("The backup file is empty. Will not overwrite data.")

    confirmation_msg = "This will OVERWRITE the old DATA file if there is one."

    if not io.confirmation_prompt(confirmation_msg):
        return

    data_paste_backup()
