from datetime import datetime


def _find_next_deadline(assignment_data):
    current_date = datetime.today()
    for i, d in enumerate(assignment_data):
        if datetime.strptime(d[1], "%d.%m.%Y") >= current_date:
            return i
    return len(assignment_data) - 1


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
    print_table(table_headers, table_rows)


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
    print_table(table_headers, table_rows)
