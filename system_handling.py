import tkinter
import database_handling as db
import reports_handling
import server

window = tkinter.Tk()

chosen_terminal_id = tkinter.StringVar()
chosen_card_id = tkinter.StringVar()
chosen_worker_id = tkinter.StringVar()


def add_new_terminal(new_terminal_id):
    db.add_terminal(db.database_filename, new_terminal_id)
    print("Added terminal %s" % new_terminal_id)


def add_new_worker(name, surname):
    db.add_worker(db.database_filename, name, surname)
    print("Added worker %s %s" % (name, surname))


def add_new_card():
    card_id = db.generate_random_card_id()

    db.add_card(db.database_filename, card_id)
    print("Added card %s" % card_id)


def assign_card(worker_id, card_id):
    db.assign_card(db.database_filename, worker_id, card_id)
    worker_full_name = db.get_worker_full_name(db.database_filename, worker_id)
    print("%s is assigned to %s" % (card_id, worker_full_name))


def remove_card_assignment(card_id):
    db.remove_card_assignment(db.database_filename, card_id)
    print("removed card %s assignment" % card_id)


def mark_card_as_stolen(card_id):
    db.mark_card_as_stolen(db.database_filename, card_id)
    print("card %s is marked as stolen" % card_id)


def connect_terminal(terminal_id):
    db.connect_terminal_to_system(db.database_filename, terminal_id)
    server.subscribe_terminal(terminal_id)
    print("%s is connected" % terminal_id)


def disconnect_terminal(terminal_id):
    db.disconnect_terminal_from_system(db.database_filename, terminal_id)
    server.unsubscribe_terminal(terminal_id)
    print("%s is disconnected" % terminal_id)


def add_terminals_info_to_window(terminals_data, info_window):
    tkinter.Label(info_window, text="Terminals: ", font=("Courier", 8), fg="blue").grid()

    for terminal_data in terminals_data:
        terminal_id = terminal_data[0]
        terminal_status = db.get_terminal_status(db.database_filename, terminal_id)

        tkinter.Label(info_window, text=terminal_id + "(" + terminal_status + ")", font=("Courier", 8)).grid()


def add_cards_info_to_window(cards_data, info_window):
    tkinter.Label(info_window, text="Cards: ", font=("Courier", 8), fg="blue").grid()

    for card_data in cards_data:
        card_id = card_data[0]
        card_assignment_info = db.get_card_assignment_info(db.database_filename, card_id)
        tkinter.Label(info_window, text=card_id + " - " + card_assignment_info, font=("Courier", 8)).grid(sticky="W")


def add_workers_info_to_window(workers_data, info_window):
    tkinter.Label(info_window, text="Workers: ", font=("Courier", 8), fg="blue").grid()

    for worker in workers_data:
        worker_id = worker[0]
        worker_full_name = db.get_worker_full_name(db.database_filename, worker_id)
        tkinter.Label(info_window, text=worker_full_name, font=("Courier", 8)).grid()


def open_current_info_window():
    info_window = tkinter.Tk()
    info_window.title("current_info_window")
    info_window.geometry("400x400")

    terminals_data = db.get_data(db.database_filename, "terminals")
    cards_data = db.get_data(db.database_filename, "cards")
    workers_data = db.get_data(db.database_filename, "workers")

    add_terminals_info_to_window(terminals_data, info_window)
    add_cards_info_to_window(cards_data, info_window)
    add_workers_info_to_window(workers_data, info_window)

    info_window.mainloop()


def create_main_window():
    window.geometry("670x520")
    window.title("System Handling")

    terminals_data = db.get_data(db.database_filename, "terminals")
    cards_data = db.get_data(db.database_filename, "cards")
    workers_data = db.get_data(db.database_filename, "workers")

    first_terminal_id = terminals_data[0][0]
    chosen_terminal_id.set(first_terminal_id)

    first_card_id = cards_data[0][0]
    chosen_card_id.set(first_card_id)

    first_worker_id = workers_data[0][0]
    chosen_worker_id.set(first_worker_id)

    tkinter.Label(window, text="Choose object and action", font=("Courier", 13), fg="green").grid(
        column=1)

    tkinter.Label(window, text="Terminals: ", font=("Courier", 10), fg="blue").grid(row=1, column=0)
    tkinter.Label(window, text="Cards: ", font=("Courier", 10), fg="blue").grid(row=1, column=1)
    tkinter.Label(window, text="Workers: ", font=("Courier", 10), fg="blue").grid(row=1, column=2)

    column_zero_row = 1
    for terminal in terminals_data:
        terminal_id = terminal[0]
        column_zero_row += 1
        tkinter.Radiobutton(window, text=terminal_id, variable=chosen_terminal_id,
                            value=terminal_id,
                            font=("Courier", 8)).grid(row=column_zero_row)

    column_one_row = 1
    for card in cards_data:
        card_id = card[0]
        column_one_row += 1
        tkinter.Radiobutton(window, text=card_id, variable=chosen_card_id,
                            value=card_id,
                            font=("Courier", 8)).grid(row=column_one_row, column=1)

    column_two_row = 1
    for worker in workers_data:
        column_two_row += 1
        worker_id = worker[0]
        worker_name = worker[2] + " " + worker[1]
        tkinter.Radiobutton(window, text=worker_name, variable=chosen_worker_id, value=worker_id,
                            font=("Courier", 8)).grid(row=column_two_row, column=2, sticky="W")

    menu_start = max(column_zero_row, column_one_row, column_two_row)

    menu_row = menu_start + 1
    tkinter.Label(window, text="Add new terminal", font=("Courier", 8), fg="blue").grid(row=menu_row, column=0)
    menu_row += 1
    tkinter.Label(window, text="Insert terminal ID\nformat: T<number>", font=("Courier", 8)).grid(row=menu_row,
                                                                                                  column=0)
    menu_row += 1
    terminal_entry = tkinter.Entry(window)
    terminal_entry.grid(row=menu_row, column=0)
    menu_row += 1
    tkinter.Button(window, text="Add terminal",
                   command=lambda: add_new_terminal(terminal_entry.get())).grid(column=0)
    column_zero_row = menu_row

    menu_row = menu_start + 1
    tkinter.Label(window, text="Add new card", font=("Courier", 8), fg="blue").grid(row=menu_row, column=1)
    menu_row += 1
    tkinter.Label(window, text="Card ID will be\ngenerated randomly", font=("Courier", 8)).grid(row=menu_row,
                                                                                                column=1)
    menu_row += 1
    tkinter.Button(window, text="Add card",
                   command=lambda: add_new_card()).grid(row=menu_row, column=1)
    column_one_row = menu_row

    menu_row = menu_start + 1
    tkinter.Label(window, text="Add new worker", font=("Courier", 8), fg="blue").grid(row=menu_row, column=2)
    menu_row += 1
    tkinter.Label(window, text="Insert new worker first name: ", font=("Courier", 8)).grid(row=menu_row,
                                                                                           column=2)
    menu_row += 1
    first_name_entry = tkinter.Entry(window)
    first_name_entry.grid(row=menu_row, column=2)
    menu_row += 1
    tkinter.Label(window, text="Insert new worker last name: ", font=("Courier", 8)).grid(row=menu_row, column=2)
    menu_row += 1
    last_name_entry = tkinter.Entry(window)
    last_name_entry.grid(row=menu_row, column=2)
    menu_row += 1
    tkinter.Button(window, text="Add worker",
                   command=lambda: add_new_worker(first_name_entry.get(), last_name_entry.get())).grid(column=2)
    last_name_entry.grid(column=2)

    column_two_row = menu_row

    menu_start = max(column_zero_row, column_one_row, column_two_row)
    menu_row = menu_start + 1
    tkinter.Label(window, text="Connect or disconnect\nchosen terminal", font=("Courier", 10), fg="blue").grid(
        row=menu_row, column=0)
    menu_row += 1
    tkinter.Button(window, text="Connect",
                   command=lambda: connect_terminal(chosen_terminal_id.get())).grid(row=menu_row, column=0)
    menu_row += 1
    tkinter.Button(window, text="Disconnect",
                   command=lambda: disconnect_terminal(chosen_terminal_id.get())).grid(
        row=menu_row, column=0)

    menu_row = menu_start + 1
    tkinter.Label(window, text="Manage card assignment:", font=("Courier", 10), fg="blue").grid(
        row=menu_row, column=1)
    menu_row += 1
    tkinter.Button(window, text="Delete chosen card assignment",
                   command=lambda: remove_card_assignment(chosen_card_id.get())).grid(row=menu_row, column=1)
    menu_row += 1
    tkinter.Button(window, text="Assign chosen card to chosen worker",
                   command=lambda: assign_card(chosen_worker_id.get(), chosen_card_id.get())).grid(
        row=menu_row, column=1)
    menu_row += 1
    tkinter.Button(window, text="Mark chosen card as stolen",
                   command=lambda: mark_card_as_stolen(chosen_card_id.get())).grid(row=menu_row, column=1)
    menu_row += 1
    tkinter.Label(window, text="Open window with current info about system:", font=("Courier", 13), fg="green").grid(
        row=menu_row, column=0, columnspan=3)
    menu_row += 1
    tkinter.Button(window, text="Show current data", command=lambda: open_current_info_window()).grid(row=menu_row,
                                                                                                      column=1)

    menu_row = menu_start + 1
    tkinter.Label(window, text="Create work time csv file", font=("Courier", 10), fg="blue").grid(row=menu_row,
                                                                                                  column=2)
    menu_row += 1
    tkinter.Button(window, text="Create csv for chosen worker",
                   command=lambda: reports_handling.create_csv(chosen_worker_id.get())).grid(row=menu_row,
                                                                                             column=2)


if __name__ == "__main__":
    create_main_window()
    window.mainloop()
