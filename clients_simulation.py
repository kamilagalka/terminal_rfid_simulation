import paho.mqtt.client as mqtt
import tkinter
import database_handling as db
import keyboard
import time
import random

broker = "localhost"

window = tkinter.Tk()

term_var = tkinter.StringVar()
card_var = tkinter.StringVar()

terminals = db.get_data(db.database_filename, "terminals")
cards = db.get_data(db.database_filename, "cards")

clients = []


def create_clients():
    for term in terminals:
        is_term_connected_to_system = term[1]
        if is_term_connected_to_system:
            term_id = term[0]
            clients.append(mqtt.Client(term_id))


def generate_random_card_id():
    card_id = "["
    for i in range(5):
        card_id += (random.randint(0, 999)).__str__()
        if i != 4:
            card_id += ", "

    card_id += "]"
    return card_id


def read_card_id():
    card_id = card_var.get()

    if card_id == "unknown":
        card_id = generate_random_card_id()

    return card_id


def read_terminal_id():
    return term_var.get()


def get_client(term_id):
    for client in clients:
        if client.client_id.__str__() == "b'%s'" % term_id:
            return client


def create_main_window():
    window.geometry("400x500")
    window.title("Clients")

    first_terminal_id = terminals[0][0]
    term_var.set(first_terminal_id)
    first_card_id = cards[0][0]
    card_var.set(first_card_id)

    # labels with instruction
    tkinter.Label(window, text="Choose used terminal and card", font=("Courier", 12), fg="green").grid()
    tkinter.Label(window, text="then press 'space' to simulate card use", font=("Courier", 12), fg="green").grid()

    # terminals radiobuttons
    tkinter.Label(window, text="Terminals: ", font=("Courier", 15)).grid()

    for terminal in terminals:
        is_term_connected_to_system = terminal[1]
        if is_term_connected_to_system == 1:
            terminal_id = terminal[0]
            tkinter.Radiobutton(window, text=terminal_id, variable=term_var, value=terminal_id,
                                font=("Courier", 10)).grid()

    # cards radiobuttons
    tkinter.Label(window, text="Cards: ", font=("Courier", 15)).grid()

    for card in cards:
        card_id = card[0]
        tkinter.Radiobutton(window, text=card_id, variable=card_var, value=card_id, font=("Courier", 10)).grid()
    tkinter.Radiobutton(window, text="Unknown card", variable=card_var, value="unknown", font=("Courier", 10)).grid()

    # exit instruction label
    tkinter.Label(window, text="Press 'esc' to exit", font=("Courier", 12), fg="red").grid()

    def disable_event():
        pass

    window.protocol("WM_DELETE_WINDOW", disable_event)


def run():
    while True:
        window.update()
        if keyboard.is_pressed('space'):
            manage_new_log()
            time.sleep(2)
        if keyboard.is_pressed('esc'):
            break


def manage_new_log():
    card_id = read_card_id()
    term_id = read_terminal_id()
    client = get_client(term_id)
    if client is not None:
        client.publish("terminal/log", card_id + "." + term_id, )


def connect_to_broker():
    for client in clients:
        client.connect(broker)
        client.publish("client/status", "connected.%s" % client.client_id)


def disconnect_from_broker():
    for client in clients:
        client.publish("client/status", "disconnected.%s" % client.client_id)
        client.disconnect()


if __name__ == "__main__":
    create_clients()
    connect_to_broker()
    create_main_window()
    run()
    disconnect_from_broker()
