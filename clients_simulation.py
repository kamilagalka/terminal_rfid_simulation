import paho.mqtt.client as mqtt
import tkinter
import database_handling as db
import keyboard
import time
import random

broker = "LAPTOP-KQDKQ66Q"
port = 8883
window = tkinter.Tk()

chosen_terminal_id = tkinter.StringVar()
chosen_card_id = tkinter.StringVar()

terminals_data = db.get_data(db.database_filename, "terminals")
cards_data = db.get_data(db.database_filename, "cards")

clients = []


def create_main_window():
    window.geometry("400x500")
    window.title("Clients")

    first_terminal_id = terminals_data[0][0]
    chosen_terminal_id.set(first_terminal_id)

    first_card_id = cards_data[0][0]
    chosen_card_id.set(first_card_id)

    # labels with instruction
    tkinter.Label(window, text="Choose used terminal and card", font=("Courier", 12), fg="green").grid()
    tkinter.Label(window, text="then press 'space' to simulate card use", font=("Courier", 12), fg="green").grid()

    # terminals radiobuttons
    tkinter.Label(window, text="Terminals: ", font=("Courier", 15)).grid()

    for terminal_data in terminals_data:
        # is_term_connected_to_system = terminal_data[1]
        # if is_term_connected_to_system:
        terminal_id = terminal_data[0]
        tkinter.Radiobutton(window, text=terminal_id, variable=chosen_terminal_id, value=terminal_id,
                            font=("Courier", 10)).grid()

    # cards radiobuttons
    tkinter.Label(window, text="Cards: ", font=("Courier", 15)).grid()

    for card_data in cards_data:
        card_id = card_data[0]
        card_owner_info = db.get_card_assignment_info(db.database_filename, card_id)
        tkinter.Radiobutton(window, text=card_id + " - " + card_owner_info, variable=chosen_card_id, value=card_id,
                            font=("Courier", 10)).grid()
    tkinter.Radiobutton(window, text="Unknown card", variable=chosen_card_id, value="unknown",
                        font=("Courier", 10)).grid()

    # exit instruction label
    tkinter.Label(window, text="Press 'esc' to exit", font=("Courier", 12), fg="red").grid()

    def disable_event():
        pass

    window.protocol("WM_DELETE_WINDOW", disable_event)


def create_clients():
    for terminal_data in terminals_data:
        term_id = terminal_data[0]
        clients.append(mqtt.Client(term_id))


def get_client(term_id):
    for client in clients:
        if client.client_id.__str__() == "b'%s'" % term_id:
            return client


def read_used_card_id():
    used_card_id = chosen_card_id.get()
    if used_card_id == "unknown":
        used_card_id = db.generate_random_card_id()
    return used_card_id


def read_used_terminal_id():
    return chosen_terminal_id.get()


def manage_new_log():
    card_id = read_used_card_id()
    terminal_id = read_used_terminal_id()
    client = get_client(terminal_id)
    if client is not None:
        client.publish("%s/log" % terminal_id, card_id + "." + terminal_id, )
        print("%s/log" % terminal_id, card_id + "." + terminal_id,)


def connect_to_broker():
    for client in clients:
        client.tls_set("ca.crt")
        client.username_pw_set(username='client', password='password')
        client.connect(broker, port)
        terminal_id = (client.client_id.__str__()).split("'")[1]
        client.publish("%s/status" % terminal_id, "online.%s" % terminal_id)


def disconnect_from_broker():
    for client in clients:
        terminal_id = (client.client_id.__str__()).split("'")[1]
        client.publish("%s/status" % terminal_id, "offline.%s" % terminal_id)
        client.disconnect()


def run():
    while True:
        window.update()
        if keyboard.is_pressed('space'):
            manage_new_log()
            time.sleep(2)
        if keyboard.is_pressed('esc'):
            break


if __name__ == "__main__":
    create_clients()
    connect_to_broker()
    create_main_window()
    run()
    disconnect_from_broker()
