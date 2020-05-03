import tkinter
import database_handling as db
import reports_handling
import server

window = tkinter.Tk()

list_of_terminals = tkinter.Listbox(window, height=7, width=40, exportselection=0)
list_of_cards = tkinter.Listbox(window, height=7, width=40, exportselection=0)
list_of_workers = tkinter.Listbox(window, height=7, width=40, exportselection=0)


def add_new_terminal(new_terminal_id):
    if new_terminal_id != '':
        is_new_terminal_id_correct = True if new_terminal_id[0] == 'T' else False
        if is_new_terminal_id_correct:
            terminal_exists = db.check_if_terminal_exists(db.database_filename, new_terminal_id)
            if not terminal_exists:
                db.add_terminal(db.database_filename, new_terminal_id)
                fill_list_of_terminals()
                print("Added terminal %s" % new_terminal_id)
            else:
                print("Terminal already exists!")
        else:
            print("Incorrect terminal id!")


def remove_terminal(terminal_id):
    if terminal_id != '':
        db.remove_terminal(db.database_filename, terminal_id)
        fill_list_of_terminals()
        print("Removed terminal %s" % terminal_id)


def add_new_card():
    new_card_id = db.generate_random_card_id()
    does_card_exist = db.check_if_card_exists(db.database_filename, new_card_id)
    if not does_card_exist:
        db.add_card(db.database_filename, new_card_id)
        fill_list_of_cards()
        print("Added card %s" % new_card_id)
    else:
        print("Card already exists!")


def remove_card(card_id):
    if card_id != '':
        db.remove_card(db.database_filename, card_id)
        fill_list_of_cards()
        print("Removed card %s" % card_id)


def add_new_worker(new_worker_first_name, new_worker_last_name):
    if new_worker_first_name != '' and new_worker_last_name != '':
        db.add_worker(db.database_filename, new_worker_first_name, new_worker_last_name)
        fill_list_of_workers()
        print("Added worker %s %s" % (new_worker_first_name, new_worker_last_name))


def remove_worker(worker_id):
    if worker_id != '':
        db.remove_worker_cards_ownership(db.database_filename, worker_id)
        db.remove_worker(db.database_filename, worker_id)
        fill_list_of_workers()
        fill_list_of_cards()
        print("Removed worker %s. His cards are now unassigned." % worker_id)


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
    window.geometry("750x550")
    window.title("System Handling")

    tkinter.Label(window, text="Choose object and action", font=("Courier", 13)).grid(
        column=1)

    tkinter.Label(window, text="Terminals: ", font=("Courier", 10)).grid(row=1, column=0)
    tkinter.Label(window, text="Cards: ", font=("Courier", 10)).grid(row=1, column=1)
    tkinter.Label(window, text="Workers: ", font=("Courier", 10)).grid(row=1, column=2)

    fill_list_of_terminals()
    fill_list_of_cards()
    fill_list_of_workers()

    # --------------------------------------------------------------------------------------------------------

    tkinter.Label(window, text="Connect or disconnect\nchosen terminal", font=("Courier", 10), fg="blue").grid(
        row=3, column=0)
    tkinter.Button(window, text="Connect", fg="blue",
                   command=lambda: connect_terminal(list_of_terminals.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=4, column=0)
    tkinter.Button(window, text="Disconnect", fg="blue",
                   command=lambda: disconnect_terminal(list_of_terminals.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=5, column=0)

    tkinter.Label(window, text="Add new terminal", font=("Courier", 10), fg="green").grid(row=7, column=0)
    tkinter.Label(window, text="Insert terminal ID\nformat: T<number>", font=("Courier", 8), fg="green").grid(row=8,
                                                                                                              column=0)
    terminal_entry = tkinter.Entry(window)
    terminal_entry.grid(row=9, column=0)
    tkinter.Button(window, text="Add terminal", fg="green",
                   command=lambda: add_new_terminal(terminal_entry.get())).grid(column=0, row=10)

    tkinter.Label(window, text="Remove marked terminal\nfrom system", font=("Courier", 10), fg="red").grid(row=12,
                                                                                                           column=0)
    tkinter.Button(window, text="Remove marked terminal", fg="red",
                   command=lambda: remove_terminal(list_of_terminals.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        column=0, row=13)

    # --------------------------------------------------------------------------------------------------------

    tkinter.Label(window, text="Manage card assignment:", font=("Courier", 10), fg="blue").grid(row=3, column=1)
    tkinter.Button(window, text="Delete chosen card assignment", fg="blue",
                   command=lambda: remove_card_assignment(list_of_cards.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=4, column=1)
    tkinter.Button(window, text="Assign chosen card to chosen worker", fg="blue",
                   command=lambda: assign_card(list_of_workers.get(tkinter.ANCHOR).split(" - ")[0],
                                               list_of_cards.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=5, column=1)
    tkinter.Button(window, text="Mark chosen card as stolen", fg="blue",
                   command=lambda: mark_card_as_stolen(list_of_cards.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        row=6, column=1)

    tkinter.Label(window, text="Add new card", font=("Courier", 10), fg="green").grid(row=8, column=1)
    tkinter.Label(window, text="Card ID will be\ngenerated randomly", font=("Courier", 8), fg="green").grid(row=9,
                                                                                                            column=1)
    tkinter.Button(window, text="Add card", fg="green", command=lambda: add_new_card()).grid(row=10, column=1)

    tkinter.Label(window, text="Remove marked card\nfrom system", font=("Courier", 10), fg="red").grid(row=12, column=1)
    tkinter.Button(window, text="Remove marked card", fg="red",
                   command=lambda: remove_card(list_of_cards.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        column=1, row=13)

    # --------------------------------------------------------------------------------------------------------

    tkinter.Label(window, text="Create work time csv file", font=("Courier", 10), fg="blue").grid(row=3, column=2)
    tkinter.Button(window, text="Create csv for chosen worker", fg="blue",
                   command=lambda: reports_handling.create_csv(
                       list_of_workers.get(tkinter.ANCHOR).split(" - ")[0])).grid(row=4, column=2)

    tkinter.Label(window, text="Add new worker", font=("Courier", 10), fg="green").grid(row=6, column=2)
    tkinter.Label(window, text="Insert new worker first name: ", font=("Courier", 8), fg="green").grid(row=7, column=2)

    first_name_entry = tkinter.Entry(window)
    first_name_entry.grid(row=8, column=2)
    tkinter.Label(window, text="Insert new worker last name: ", font=("Courier", 10), fg="green").grid(row=9, column=2)
    last_name_entry = tkinter.Entry(window)
    last_name_entry.grid(row=10, column=2)
    tkinter.Button(window, text="Add worker", fg="green",
                   command=lambda: add_new_worker(first_name_entry.get(), last_name_entry.get())).grid(column=2, row=11)

    tkinter.Label(window, text="Remove marked worker\nfrom system", font=("Courier", 10), fg="red").grid(row=13,
                                                                                                         column=2)
    tkinter.Button(window, text="Remove marked worker", fg="red",
                   command=lambda: remove_worker(list_of_workers.get(tkinter.ANCHOR).split(" - ")[0])).grid(
        column=2, row=14)


if __name__ == "__main__":
    create_main_window()
    window.mainloop()
