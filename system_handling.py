import tkinter
import database_handling as db
import reports_handling

window = tkinter.Tk()

term_var = tkinter.StringVar()
card_var = tkinter.StringVar()
worker_var = tkinter.StringVar()


def open_data_window():
    data_window = tkinter.Tk()
    data_window.geometry("300x300")

    terminals = db.get_data(db.database_filename, "terminals")
    cards = db.get_data(db.database_filename, "cards")
    workers = db.get_data(db.database_filename, "workers")

    tkinter.Label(data_window, text="Terminals: ", font=("Courier", 10), fg="blue").grid()

    for terminal in terminals:
        terminal_id = terminal[0]
        if terminal[1] == 1:
            terminal_status = "connected"
        else:
            terminal_status = "disconnected"
        tkinter.Label(data_window, text=terminal_id + "(" + terminal_status + ")", font=("Courier", 8)).grid()

    tkinter.Label(data_window, text="Cards: ", font=("Courier", 10), fg="blue").grid()
    for card in cards:
        card_id = card[0]
        card_owner_id = card[1]

        if card_owner_id == db.STOLEN_CARD_OWNER_ID:
            card_owner = "!!! STOLEN !!!"
        elif card_owner_id is None:
            card_owner = "..."
        else:
            card_owner = workers[card_owner_id - 1][2] + " " + workers[card_owner_id - 1][1]

        tkinter.Label(data_window, text=card_id + " - " + card_owner, font=("Courier", 8)).grid(sticky="W")

    data_window.mainloop()


def create_main_window():
    window.geometry("600x600")
    window.title("System Handling")

    terminals = db.get_data(db.database_filename, "terminals")
    cards = db.get_data(db.database_filename, "cards")
    workers = db.get_data(db.database_filename, "workers")

    first_terminal_id = terminals[0][0]
    term_var.set(first_terminal_id)

    first_card_id = cards[0][0]
    card_var.set(first_card_id)

    first_worker_id = workers[0][0]
    worker_var.set(first_worker_id)

    tkinter.Label(window, text="Choose :", font=("Courier", 10), fg="green").grid(column=1)

    tkinter.Label(window, text="Terminals: ", font=("Courier", 10), fg="blue").grid(row=1, column=0)
    tkinter.Label(window, text="Cards: ", font=("Courier", 10), fg="blue").grid(row=1, column=1)
    tkinter.Label(window, text="Workers: ", font=("Courier", 10), fg="blue").grid(row=1, column=2)

    for terminal in terminals:
        terminal_id = terminal[0]
        tkinter.Radiobutton(window, text=terminal_id, variable=term_var,
                            value=terminal_id,
                            font=("Courier", 8)).grid()

    row = 1
    for card in cards:
        card_id = card[0]
        row += 1
        tkinter.Radiobutton(window, text=card_id, variable=card_var,
                            value=card_id,
                            font=("Courier", 8)).grid(row=row, column=1)

    row = 1
    for worker in workers:
        row += 1
        worker_id = worker[0]
        worker_name = worker[2] + " " + worker[1]
        tkinter.Radiobutton(window, text=worker_name, variable=worker_var,
                            value=worker_id,
                            font=("Courier", 8)).grid(row=row, column=2, sticky="W")

    tkinter.Label(window, text="Open window with current info about system:", font=("Courier", 10), fg="green").grid(
        rowspan=2, column=1)
    tkinter.Button(window, text="Show current data",
                   command=lambda: open_data_window()).grid(column=1)

    tkinter.Label(window, text="Connect or disconnect terminal:", font=("Courier", 10), fg="green").grid(column=1)
    tkinter.Button(window, text="Connect chosen terminal to system",
                   command=lambda: db.connect_terminal_to_system(db.database_filename, term_var.get())).grid(column=1)
    tkinter.Button(window, text="Disconnect chosen terminal from system",
                   command=lambda: db.disconnect_terminal_from_system(db.database_filename, term_var.get())).grid(
        column=1)

    tkinter.Label(window, text="Manage card assignment:", font=("Courier", 10), fg="green").grid(
        column=1)
    tkinter.Button(window, text="Delete chosen card assignment",
                   command=lambda: db.remove_card_assignment(db.database_filename, card_var.get())).grid(column=1)
    tkinter.Button(window, text="Assign chosen card to chosen worker",
                   command=lambda: db.assign_card(db.database_filename, worker_var.get(), card_var.get())).grid(
        column=1)
    tkinter.Button(window, text="Mark chosen card as stolen",
                   command=lambda: db.mark_card_as_stolen(db.database_filename, card_var.get())).grid(column=1)

    tkinter.Label(window, text="Create work time csv file", font=("Courier", 10), fg="green").grid(column=1)
    tkinter.Button(window, text="Create csv for chosen worker",
                   command=lambda: reports_handling.create_csv(worker_var.get())).grid(column=1)


if __name__ == "__main__":
    create_main_window()
    window.mainloop()
