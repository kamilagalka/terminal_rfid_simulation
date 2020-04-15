import tkinter
import database_handling as db
import server

window = tkinter.Tk()

chosen_terminal_id = tkinter.StringVar()
chosen_card_id = tkinter.StringVar()
chosen_worker_id = tkinter.StringVar()


def open_data_window():
    data_window = tkinter.Tk()
    data_window.title("data_window")
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
    chosen_terminal_id.set(first_terminal_id)

    first_card_id = cards[0][0]
    chosen_card_id.set(first_card_id)

    first_worker_id = workers[0][0]
    chosen_worker_id.set(first_worker_id)

    tkinter.Label(window, text="Choose :", font=("Courier", 10), fg="green").grid(column=1)

    tkinter.Label(window, text="Terminals: ", font=("Courier", 10), fg="blue").grid(row=1, column=0)
    tkinter.Label(window, text="Cards: ", font=("Courier", 10), fg="blue").grid(row=1, column=1)
    tkinter.Label(window, text="Workers: ", font=("Courier", 10), fg="blue").grid(row=1, column=2)

    for terminal in terminals:
        terminal_id = terminal[0]
        tkinter.Radiobutton(window, text=terminal_id, variable=chosen_terminal_id,
                            value=terminal_id,
                            font=("Courier", 8)).grid()

    row = 1
    for card in cards:
        card_id = card[0]
        row += 1
        tkinter.Radiobutton(window, text=card_id, variable=chosen_card_id,
                            value=card_id,
                            font=("Courier", 8)).grid(row=row, column=1)

    row = 1
    for worker in workers:
        row += 1
        worker_id = worker[0]
        worker_name = worker[2] + " " + worker[1]
        tkinter.Radiobutton(window, text=worker_name, variable=chosen_worker_id, value=worker_id,
                            font=("Courier", 8)).grid(row=row, column=2, sticky="W")

    tkinter.Label(window, text="Open window with current info about system:", font=("Courier", 10), fg="green").grid(
        rowspan=2, column=1)
    tkinter.Button(window, text="Show current data", command=lambda: open_data_window()).grid(column=1)

    tkinter.Label(window, text="Connect or disconnect terminal:", font=("Courier", 10), fg="green").grid(column=1)
    tkinter.Button(window, text="Connect chosen terminal to system",
                   command=lambda: server.connect_terminal(chosen_terminal_id.get())).grid(column=1)
    tkinter.Button(window, text="Disconnect chosen terminal from system",
                   command=lambda: server.disconnect_terminal(chosen_terminal_id.get())).grid(
        column=1)

    tkinter.Label(window, text="Manage card assignment:", font=("Courier", 10), fg="green").grid(
        column=1)
    tkinter.Button(window, text="Delete chosen card assignment",
                   command=lambda: server.remove_card_assignment(chosen_card_id.get())).grid(column=1)
    tkinter.Button(window, text="Assign chosen card to chosen worker",
                   command=lambda: server.assign_card(chosen_worker_id.get(), chosen_card_id.get())).grid(
        column=1)
    tkinter.Button(window, text="Mark chosen card as stolen",
                   command=lambda: server.mark_card_as_stolen(chosen_card_id.get())).grid(column=1)

    tkinter.Label(window, text="Create work time csv file", font=("Courier", 10), fg="green").grid(column=1)
    tkinter.Button(window, text="Create csv for chosen worker",
                   command=lambda: server.reports_handling.create_csv(chosen_worker_id.get())).grid(column=1)


if __name__ == "__main__":
    create_main_window()
    window.mainloop()
