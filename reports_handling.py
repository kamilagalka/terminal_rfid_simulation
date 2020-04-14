import datetime
import database_handling as db
import csv


def calc_work_time(entry_date, entry_time, exit_date, exit_time):
    entry_date_table = entry_date.split(".")
    entry_time_table = entry_time.split(":")

    entry_datetime = datetime.datetime(int(entry_date_table[2]), int(entry_date_table[1]), int(entry_date_table[0]),
                                       int(entry_time_table[0]), int(entry_time_table[1]),
                                       int(entry_time_table[2]))

    exit_date_table = exit_date.split(".")
    exit_time_table = exit_time.split(":")

    exit_datetime = datetime.datetime(int(exit_date_table[2]), int(exit_date_table[1]), int(exit_date_table[0]),
                                      int(exit_time_table[0]), int(exit_time_table[1]),
                                      int(exit_time_table[2]))
    work_time = exit_datetime - entry_datetime

    return work_time


def create_csv(worker_id):
    worker_last_name = db.get_worker_last_name(db.database_filename, worker_id)
    worker_first_name = db.get_worker_first_name(db.database_filename, worker_id)
    filename = ("reports/%s_%s_%s_report.csv" % (worker_id, worker_last_name, worker_first_name))

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Entry date", "Entry time", "Entry card", "Entry terminal", "Exit date", "Exit time", "Exit card",
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
