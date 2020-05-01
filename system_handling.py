import tkinter
import database_handling as db
import reports_handling
import server

window = tkinter.Tk()

list_of_terminals = tkinter.Listbox(window, exportselection=0)
list_of_cards = tkinter.Listbox(window, width=40, exportselection=0)
list_of_workers = tkinter.Listbox(window, exportselection=0)


def add_new_terminal(new_terminal_id):
    db.add_terminal(db.database_filename, new_terminal_id)
    fill_list_of_terminals()
    print("Added terminal %s" % new_terminal_id)


def add_new_worker(new_worker_name, new_worker_surname):
    db.add_worker(db.database_filename, new_worker_name, new_worker_surname)
    fill_list_of_workers()
    print("Added worker %s %s" % (new_worker_name, new_worker_surname))


def add_new_card():
    new_card_id = db.generate_random_card_id()
    db.add_card(db.database_filename, new_card_id)
    fill_list_of_cards()
    print("Added card %s" % new_card_id)


def assign_card(worker_id, card_id):
    if worker_id != '' and card_id != '':
        db.assign_card(db.database_filename, worker_id, card_id)
        worker_full_name = db.get_worker_full_name(db.database_filename, worker_id)
        fill_list_of_cards()
        print("%s is assigned to %s" % (card_id, worker_full_name))


def remove_card_assignment(card_id):
    if card_id != '':
        db.remove_card_assignment(db.database_filename, card_id)
        fill_list_of_cards()
        print("removed card %s assignment" % card_id)


def mark_card_as_stolen(card_id):
    if card_id != '':
        db.mark_card_as_stolen(db.database_filename, card_id)
        fill_list_of_cards()
        print("card %s is marked as stolen" % card_id)


def connect_terminal(terminal_id):
    if terminal_id != '':
        db.connect_terminal_to_system(db.database_filename, terminal_id)
        fill_list_of_terminals()
        server.subscribe_terminal(terminal_id)
        print("%s is connected" % terminal_id)


def disconnect_terminal(terminal_id):
    if terminal_id != '':
        db.disconnect_terminal_from_system(db.database_filename, terminal_id)
        fill_list_of_terminals()
        server.unsubscribe_terminal(terminal_id)
        print("%s is disconnected" % terminal_id)


def fill_list_of_terminals():
    scrollbar = tkinter.Scrollbar(window)
    scrollbar.grid(row=2, column=0, sticky='nes')

    list_of_terminals.delete(0, tkinter.END)
    terminals_data = db.get_terminals(db.database_filename)
    for terminal in terminals_data:
        terminal_id = terminal[0]
        is_terminal_connected = terminal[1]
        terminal_status = "connected" if is_terminal_connected else "disconnected"
        terminal_data = "%s - (%s)" % (terminal_id, terminal_status)
        list_of_terminals.insert(tkinter.END, terminal_data)
    list_of_terminals.grid(column=0, row=2)

    list_of_terminals.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=list_of_terminals.yview)


def fill_list_of_cards():
    scrollbar = tkinter.Scrollbar(window)
    scrollbar.grid(row=2, column=1, sticky='nes')

    list_of_cards.delete(0, tkinter.END)
    cards_data = db.get_cards(db.database_filename)
    for card in cards_data:
        card_id = card[0]
        card_assignment = db.get_card_assignment_info(db.database_filename, card_id)
        card_data = "%s - %s" % (card_id, card_assignment)
        list_of_cards.insert(tkinter.END, card_data)
    list_of_cards.grid(column=1, row=2)

    list_of_cards.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=list_of_cards.yview)


def fill_list_of_workers():
    scrollbar = tkinter.Scrollbar(window)
    scrollbar.grid(row=2, column=2, sticky='nes')

    list_of_workers.delete(0, tkinter.END)
    workers_data = db.get_workers(db.database_filename)
    for worker in workers_data:
        worker_id = worker[0]
        worker_last_name = worker[2]
        worker_first_name = worker[1]
        worker_full_name = "%s - %s %s" % (worker_id, worker_last_name, worker_first_name)
        list_of_workers.insert(tkinter.END, worker_full_name)
    list_of_workers.grid(column=2, row=2)

    list_of_workers.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=list_of_workers.yview)


def create_main_window():
    window.geometry("670x520")
    window.title("System Handling")

    tkinter.Label(window, text="Choose object and action", font=("Courier", 13), fg="green").grid(
        column=1)

    tkinter.Label(window, text="Terminals: ", font=("Courier", 10), fg="blue").grid(row=1, column=0)
    tkinter.Label(window, text="Cards: ", font=("Courier", 10), fg="blue").grid(row=1, column=1)
    tkinter.Label(window, text="Workers: ", font=("Courier", 10), fg="blue").grid(row=1, column=2)

    fill_list_of_terminals()
    fill_list_of_cards()
    fill_list_of_workers()

    tkinter.Label(window, text="Add new terminal", font=("Courier", 8), fg="blue").grid(row=3, column=0)
    tkinter.Label(window, text="Insert terminal ID\nformat: T<number>", font=("Courier", 8)).grid(row=4,
                                                                                                  column=0)
    terminal_entry = tkinter.Entry(window)
    terminal_entry.grid(row=5, column=0)
    tkinter.Button(window, text="Add terminal",
                   command=lambda: add_new_terminal(terminal_entry.get())).grid(column=0, row=6)

    tkinter.Label(window, text="Add new card", font=("Courier", 8), fg="blue").grid(row=3, column=1)
    tkinter.Label(window, text="Card ID will be\ngenerated randomly", font=("Courier", 8)).grid(row=4,
                                                                                                column=1)
    tkinter.Button(window, text="Add card",
                   command=lambda: add_new_card()).grid(row=5, column=1)

    tkinter.Label(window, text="Add new worker", font=("Courier", 8), fg="blue").grid(row=3, column=2)
    tkinter.Label(window, text="Insert new worker first name: ", font=("Courier", 8)).grid(row=4,
                                                                                           column=2)

    first_name_entry = tkinter.Entry(window)
    first_name_entry.grid(row=5, column=2)
    tkinter.Label(window, text="Insert new worker last name: ", font=("Courier", 8)).grid(row=6, column=2)
    last_name_entry = tkinter.Entry(window)
    last_name_entry.grid(row=7, column=2)
    tkinter.Button(window, text="Add worker",
                   command=lambda: add_new_worker(first_name_entry.get(), last_name_entry.get())).grid(column=2, row=8)

    tkinter.Label(window, text="Connect or disconnect\nchosen terminal", font=("Courier", 10), fg="blue").grid(
        row=10, column=0)
    tkinter.Button(window, text="Connect",
                   command=lambda: connect_terminal(list_of_terminals.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=11, column=0)
    tkinter.Button(window, text="Disconnect",
                   command=lambda: disconnect_terminal(list_of_terminals.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=12, column=0)

    tkinter.Label(window, text="Manage card assignment:", font=("Courier", 10), fg="blue").grid(
        row=10, column=1)
    tkinter.Button(window, text="Delete chosen card assignment",
                   command=lambda: remove_card_assignment(list_of_cards.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=11,
        column=1)
    tkinter.Button(window, text="Assign chosen card to chosen worker",
                   command=lambda: assign_card(list_of_workers.get(tkinter.ANCHOR).split(" - ")[0],
                                               list_of_cards.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=12, column=1)
    tkinter.Button(window, text="Mark chosen card as stolen",
                   command=lambda: mark_card_as_stolen(list_of_cards.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=13, column=1)

    tkinter.Label(window, text="Create work time csv file", font=("Courier", 10), fg="blue").grid(row=10,
                                                                                                  column=2)
    tkinter.Button(window, text="Create csv for chosen worker",
                   command=lambda: reports_handling.create_csv(
                       list_of_workers.get(tkinter.ANCHOR).split(" - ")[0])).grid(row=11,
                                                                                  column=2)


if __name__ == "__main__":
    create_main_window()
    window.mainloop()
