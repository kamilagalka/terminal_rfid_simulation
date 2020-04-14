import sqlite3
import os

database_filename = "test2.db"
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
    worker_name = worker[1]
    return worker_name


def get_worker_last_name(db_name, worker_id):
    workers = get_data(db_name, "workers")
    worker = workers[int(worker_id) - 1]
    worker_surname = worker[2]
    return worker_surname


def get_worker_logs(db_name, worker_id):
    logs = get_data(db_name, "logs")
    worker_logs = []
    for log in logs:
        log_worker_id = log[3]
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


def add_log(db_name, date, time, terminal_id, card_id, worker_id):
    instruction = "INSERT INTO logs VALUES ('%s', '%s', '%s', '%s', '%s')" % (
        date, time, card_id, worker_id, terminal_id)
    modify_database(db_name, instruction)


def find_card_owner_id(db_name, card_id):
    cards = get_data(db_name, "cards")
    for card in cards:
        this_card_id = card[0]
        owner_id = card[1]
        if this_card_id == card_id:
            return owner_id


def get_card_possession_info(db_name, card_id):
    worker_id = find_card_owner_id(db_name, card_id)
    if worker_id is None:
        return "unknown"
    elif worker_id == -1:
        return "THIS CARD HAS BEEN STOLEN"
    else:
        return get_worker_last_name(db_name, worker_id) + get_worker_first_name(db_name, worker_id)


def get_data(db_name, table_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM %s" % table_name)
    items = cursor.fetchall()
    connection.close()
    return items


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

    assign_card(db_name, 1, "[176, 111, 225, 37, 27]")
    assign_card(db_name, 2, "[217, 125, 80, 211, 39]")
    assign_card(db_name, 3, "[123, 41, 351, 52, 22]")

    mark_card_as_stolen(db_name, "[42, 241, 54, 122, 532]")

    add_log(db_name, "14.04.2020", "12:01:11", "T1", "[176, 111, 225, 37, 27]", 1)
    add_log(db_name, "14.04.2020", "20:10:15", "T1", "[176, 111, 225, 37, 27]", 1)
    add_log(db_name, "15.04.2020", "20:05:02", "T1", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "16.04.2020", "04:01:11", "T1", "[217, 125, 80, 211, 39]", 1)
    add_log(db_name, "14.04.2020", "12:01:20", "T1", "[217, 125, 80, 211, 39]", 2)
    add_log(db_name, "14.04.2020", "20:02:53", "T1", "[217, 125, 80, 211, 39]", 2)


if __name__ == "__main__":
    # creates database with empty system essential tables (workers, cards, terminals, logs)
    # create_empty_system_database(database_filename)

    # creates test database with 3 workers, 5 cards (with some assignments), 2 terminals and 10 logs
    create_test_database(database_filename)
