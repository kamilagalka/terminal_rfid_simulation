import random
import sqlite3
import os

database_filename = "system_database.db"
STOLEN_CARD_OWNER_ID = -1


def create_database(db_name):
    if os.path.exists(db_name):
        os.remove(db_name)

    connection = sqlite3.connect(db_name)
    connection.close()


def modify_database(db_name, instruction):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute(instruction)
    connection.commit()

    connection.close()


def check_if_table_exists(db_name, table_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='%s' ''' % table_name)
    does_table_exist = cursor.fetchone()[0]
    connection.close()

    return does_table_exist


def create_workers_table(db_name):
    instruction = """CREATE TABLE workers (
    worker_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
    )"""

    modify_database(db_name, instruction)


def create_cards_table(db_name):
    instruction = """CREATE TABLE cards (
        card_id TEXT,
        owner_id INTEGER
        )"""

    modify_database(db_name, instruction)


def create_terminals_table(db_name):
    instruction = """CREATE TABLE terminals (
           terminal_id TEXT,
           is_connected_to_system BIT
           )"""

    modify_database(db_name, instruction)


def create_logs_table(db_name):
    instruction = """CREATE TABLE logs (
            date TEXT,
            time TEXT,
            card_id TEXT,
            worker_id INTEGER,
            terminal_id INTEGER 
            )"""

    modify_database(db_name, instruction)


def add_worker(db_name, first_name, last_name):
    instruction = "INSERT INTO workers(first_name, last_name) VALUES ('%s', '%s')" % (first_name, last_name)
    modify_database(db_name, instruction)


def get_worker_first_name(db_name, worker_id):
    workers = get_data(db_name, "workers")
    worker = workers[int(worker_id) - 1]
    worker_first_name = worker[1]
    return worker_first_name


def get_worker_last_name(db_name, worker_id):
    workers = get_data(db_name, "workers")
    worker = workers[int(worker_id) - 1]
    worker_last_name = worker[2]
    return worker_last_name


def get_worker_full_name(db_name, worker_id):
    worker_last_name = get_worker_last_name(db_name, worker_id)
    worker_first_name = get_worker_first_name(db_name, worker_id)
    worker_full_name = worker_id.__str__() + " " + worker_last_name + " " + worker_first_name
    return worker_full_name


def get_worker_logs(db_name, worker_id):
    logs = get_data(db_name, "logs")
    worker_logs = []
    for log in logs:
        log_worker_id = log[3]
        if log_worker_id != 'None':
            if int(log_worker_id) == int(worker_id):
                worker_logs.append(log)
    return worker_logs


def remove_worker(db_name, worker_id):
    instruction = "DELETE from workers where worker_id = %s" % worker_id
    modify_database(db_name, instruction)


def add_card(db_name, card_id):
    instruction = "INSERT INTO cards(card_id) VALUES ('%s')" % card_id
    modify_database(db_name, instruction)


def assign_card(db_name, worker_id, card_id):
    instruction = """UPDATE cards
        SET owner_id = '%s'
        WHERE card_id = '%s'
        """ % (worker_id, card_id)
    modify_database(db_name, instruction)


def remove_card_assignment(db_name, card_id):
    instruction = """UPDATE cards
        SET owner_id = NULL
        WHERE card_id = '%s'
        """ % card_id
    modify_database(db_name, instruction)


def mark_card_as_stolen(db_name, card_id):
    remove_card_assignment(db_name, card_id)
    assign_card(db_name, STOLEN_CARD_OWNER_ID, card_id)


def generate_random_card_id():
    card_id = "["
    for i in range(5):
        card_id += (random.randint(0, 999)).__str__()
        if i != 4:
            card_id += ", "

    card_id += "]"
    return card_id


def find_card_owner_id(db_name, card_id):
    cards = get_data(db_name, "cards")
    for card in cards:
        this_card_id = card[0]
        owner_id = card[1]

        if this_card_id == card_id:
            return owner_id


def get_card_assignment_info(db_name, card_id):
    owner_id = find_card_owner_id(db_name, card_id)
    if owner_id == STOLEN_CARD_OWNER_ID:
        assignment_info = "--STOLEN--"
    elif owner_id is None:
        assignment_info = "--not-assgined--"
    else:
        assignment_info = get_worker_full_name(db_name, owner_id)
    return assignment_info


def add_terminal(db_name, terminal_id):
    instruction = "INSERT INTO terminals(terminal_id, is_connected_to_system) VALUES ('%s', '%s')" % (terminal_id, 0)
    modify_database(db_name, instruction)


def connect_terminal_to_system(db_name, terminal_id):
    instruction = """UPDATE terminals
        SET is_connected_to_system = 1
        WHERE terminal_id = '%s'
        """ % terminal_id
    modify_database(db_name, instruction)


def disconnect_terminal_from_system(db_name, terminal_id):
    instruction = """UPDATE terminals
        SET is_connected_to_system = 0
        WHERE terminal_id = '%s'
        """ % terminal_id
    modify_database(db_name, instruction)


def remove_terminal(db_name, terminal_id):
    instruction = "DELETE from terminals where terminal_id = %s" % terminal_id
    modify_database(db_name, instruction)


def get_terminal_status(db_name, terminal_id):
    terminals = get_data(db_name, "terminals")

    is_terminal_connected = "disconnected"

    for terminal in terminals:
        if terminal_id == terminal[0]:
            is_terminal_connected = terminal[1]

    terminal_status = "connected" if is_terminal_connected else "disconnected"
    return terminal_status


def add_log(db_name, date, time, terminal_id, card_id, worker_id):
    instruction = "INSERT INTO logs VALUES ('%s', '%s', '%s', '%s', '%s')" % (
        date, time, card_id, worker_id, terminal_id)
    modify_database(db_name, instruction)


def get_data(db_name, table_name):
    does_table_exist = check_if_table_exists(db_name, table_name)
    if not does_table_exist:
        create_empty_system_database(db_name)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM %s" % table_name)
    items = cursor.fetchall()
    connection.close()
    return items


def get_terminals(db_name):
    return get_data(db_name, "terminals")


def get_cards(db_name):
    return get_data(db_name, "cards")


def get_workers(db_name):
    return get_data(db_name, "workers")


def print_data(db_name, table_name):
    for item in get_data(db_name, table_name):
        print(item)


def create_empty_system_database(db_name):
    create_database(db_name)
    create_workers_table(db_name)
    create_cards_table(db_name)
    create_terminals_table(db_name)
    create_logs_table(db_name)


def create_test_database(db_name):
    create_empty_system_database(db_name)

    add_worker(db_name, "Jan", "Kowalski")
    add_worker(db_name, "Anna", "Nowak")
    add_worker(db_name, "Filip", "Filipowski")

    add_card(db_name, "[176, 111, 225, 37, 27]")
    add_card(db_name, "[217, 125, 80, 211, 39]")
    add_card(db_name, "[123, 41, 351, 52, 22]")
    add_card(db_name, "[92, 421, 51, 552, 312]")
    add_card(db_name, "[42, 241, 54, 122, 532]")

    add_terminal(db_name, "T1")
    add_terminal(db_name, "T2")

    connect_terminal_to_system(db_name, "T1")
    connect_terminal_to_system(db_name, "T2")

    assign_card(db_name, 1, "[176, 111, 225, 37, 27]")
    assign_card(db_name, 2, "[217, 125, 80, 211, 39]")
    assign_card(db_name, 3, "[123, 41, 351, 52, 22]")

    mark_card_as_stolen(db_name, "[42, 241, 54, 122, 532]")

    add_log(db_name, "14.04.2020", "12:01:11", "T1", "[176, 111, 225, 37, 27]", 1)
    add_log(db_name, "14.04.2020", "20:10:15", "T2", "[176, 111, 225, 37, 27]", 1)
    add_log(db_name, "15.04.2020", "20:05:02", "T2", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "16.04.2020", "04:01:11", "T1", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "17.04.2020", "08:01:21", "T1", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "17.04.2020", "16:11:09", "T2", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "18.04.2020", "08:00:42", "T1", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "18.04.2020", "16:02:01", "T1", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "14.04.2020", "12:01:20", "T1", "[217, 125, 80, 211, 39]", 2)
    add_log(db_name, "14.04.2020", "20:02:53", "T2", "[217, 125, 80, 211, 39]", 2)
    add_log(db_name, "15.04.2020", "12:07:13", "T1", "[217, 125, 80, 211, 39]", 2)
    add_log(db_name, "15.04.2020", "18:02:42", "T2", "[217, 125, 80, 211, 39]", 2)
    add_log(db_name, "15.04.2020", "10:02:42", "T2", "[217, 125, 80, 211, 39]", 3)
    add_log(db_name, "15.04.2020", "18:02:42", "T1", "[217, 125, 80, 211, 39]", 3)

    print("Test database created")


if __name__ == "__main__":
    create_test_database(database_filename)
