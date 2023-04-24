from datetime import datetime, timedelta

from assignment_manager.data import (
    Progress, load_data, write_data
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
    table_headers = [
        "Name",
        "Start",
        "Deadline",
        "Progress"
    ]
    table_rows = []
    for key in data:
        cycle = _find_next_deadline(data[key])
        table_rows.append([
            key,
            data[key][cycle][0],
            data[key][cycle][1],
            Progress(data[key][cycle][2]).name
        ])
    io.print_table(table_headers, table_rows)


def show_specific_assignment(name):
    data = load_data()
    if not name in data:
        raise ValueError("The given course doesn't exist", name)

    table_headers = [
        "Start",
        "Deadline",
        "Progress"
    ]
    table_rows = []
    for data_entry in data[name]:
        table_rows.append([
            data_entry[0],
            data_entry[1],
            Progress(data_entry[2]).name
        ])
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
    data = load_data()
    if params[0] in data.keys():
        raise ValueError("Name already exists!", name)

    progress = generate_dates(params[1], params[2], params[3], params[4])
    data[params[0]] = progress
    write_data(data)


def update_assignment():
    data = load_data()
    name = io.update_assignment_response_course(data.keys())
    if name not in data.keys():
        raise ValueError("Name doesn't exist!", name)

    cycle_choices = [d for d in data[name]]
    progress_choices = [p.name for p in Progress]
    cycle, progress = io.update_assignment_response(cycle_choices, progress_choices)

    data[name][cycle][2] = progress
    write_data(data)


def remove_assignment(name):
    data = load_data()
    if name not in data.keys():
        raise ValueError("Name doesn't exist!", name)

    if not io.confirmation_prompt():
        print("[bold]Aborting...[/bold]")
        return

    data.pop(name)
    write_data(data)
