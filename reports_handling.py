import datetime
import database_handling as db
import csv


def get_datetime_object_from_strings(date_string, time_string):
    date_table = date_string.split(".")
    time_table = time_string.split(":")
    return datetime.datetime(year=int(date_table[2]), month=int(date_table[1]), day=int(date_table[0]),
                             hour=int(time_table[0]), minute=int(time_table[1]), second=int(time_table[2]))


def calc_work_time(entry_date, entry_time, exit_date, exit_time):
    entry_datetime = get_datetime_object_from_strings(entry_date, entry_time)
    exit_datetime = get_datetime_object_from_strings(exit_date, exit_time)

    work_time = exit_datetime - entry_datetime
    return work_time


def create_csv(worker_id):
    worker_last_name = db.get_worker_last_name(db.database_filename, worker_id)
    worker_first_name = db.get_worker_first_name(db.database_filename, worker_id)
    filename = ("reports/%s_%s_%s_report.csv" % (worker_id, worker_last_name, worker_first_name))

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(
            ["Entry date", "Entry time", "Entry card", "Entry terminal", "Exit date", "Exit time", "Exit card",
             "Exit terminal", "Work time"])

        worker_logs = db.get_worker_logs(db.database_filename, worker_id)

        is_entry = True
        entry_date = ""
        entry_time = ""
        entry_card = ""
        entry_terminal = ""

        for log in worker_logs:
            if is_entry:
                entry_date = log[0]
                entry_time = log[1]
                entry_card = log[2]
                entry_terminal = log[4]

                is_entry = not is_entry
            else:
                exit_date = log[0]
                exit_time = log[1]
                exit_card = log[2]
                exit_terminal = log[4]
                work_time = (calc_work_time(entry_date, entry_time, exit_date, exit_time)).__str__()

                writer.writerow(
                    [entry_date, entry_time, entry_card, entry_terminal, exit_date, exit_time, exit_card, exit_terminal,
                     work_time])

                is_entry = not is_entry
    print("Report %s is ready" % filename)
