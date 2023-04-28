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


def sort_data(row_data, sort_index, ascending=True):
    if sort_index < 0 or sort_index >= len(row_data):
        raise ValueError(
            "The given index must be in range of the row_data",
            sort_index,
            row_data,
        )

    row_data.sort(key=lambda x: x[sort_index], reverse=not ascending)


def get_table_rows():
    data = load_data()
    table_rows = []
    for key in data:
        cycle = _find_next_deadline(data[key])
        remaing_days = (
            datetime.strptime(data[key][cycle][1], "%d.%m.%Y")
            - datetime.today()
        ).days
        table_rows.append(
            [
                key,
                datetime.strptime(data[key][cycle][0], "%d.%m.%Y"),
                datetime.strptime(data[key][cycle][1], "%d.%m.%Y"),
                Progress(data[key][cycle][2]),
                remaing_days,
            ]
        )
    return table_rows


def show_all_assignments(sort):
    table_headers = ["Name", "Start", "Deadline", "Progress", "Days"]
    table_rows = get_table_rows()

    if sort:
        sort_index = table_headers.index(
            io.list_prompt(table_headers, "Which to sort by?")
        )
        ascending = io.binary_prompt("Sort ascending?")
    else:
        sort_index = 4
        ascending = True

    table_headers[sort_index] += " ▼" if ascending else " ▲"
    sort_data(table_rows, sort_index, ascending)

    for i in range(len(table_rows)):
        table_rows[i] = [
            table_rows[i][0],
            table_rows[i][1].strftime("%d.%m.%Y"),
            table_rows[i][2].strftime("%d.%m.%Y"),
            table_rows[i][3].name,
            str(table_rows[i][4]),
        ]

    io.print_table(table_headers, table_rows)


def show_specific_assignment():
    data = load_data()
    name = io.list_prompt(data.keys(), "Which course do you want to update?")

    table_headers = ["Start", "Deadline", "Progress"]
    table_rows = []
    for data_entry in data[name]:
        table_rows.append(
            [data_entry[0], data_entry[1], Progress(data_entry[2]).name]
        )
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
    name = io.list_prompt(data.keys(), "Which course do you want to update?")

    cycle_choices = [d for d in data[name]]
    progress_choices = [p.name for p in Progress]
    cycle, progress = io.update_assignment_response(
        cycle_choices, progress_choices
    )

    data[name][cycle][2] = progress
    write_data(data)


def rename_assignment():
    data = load_data()
    old_name = io.list_prompt(
        data.keys(), "Which course do you want to update?"
    )
    new_name = io.rename_assignment_response()

    if new_name in data:
        raise ValueError("The name already exists!", new_name, data.keys())

    data[new_name] = data.pop(old_name)
    write_data(data)


def remove_assignment():
    data = load_data()
    name = io.list_prompt(data.keys(), "Which course do you want to update?")

    confirmation_msg = (
        "This will delete [bold]ALL[/bold] data for "
        "the course: [bold]{}[/bold]\n".format(name)
    )

    if not io.confirmation_prompt(confirmation_msg):
        return

    data.pop(name)
    write_data(data)


def copy_backup():
    if data_file_empty():
        raise ValueError("The data file is empty. No backup will be made.")

    confirmation_msg = (
        "This will OVERWRITE the old BACKUP file if there is one."
    )

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
