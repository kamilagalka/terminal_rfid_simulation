import paho.mqtt.client as mqtt
import tkinter
import database_handling as db
import datetime
import reports_handling

broker = "localhost"
client = mqtt.Client()


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    if not message_decoded[0] == "online" and not message_decoded[0] == "offline":
        card_id = message_decoded[0]
        term_id = message_decoded[1]

        date_time_now = datetime.datetime.now()
        log_date = date_time_now.strftime("%d") + "." + date_time_now.strftime("%m") + "." + date_time_now.strftime(
            "%y")
        log_time = date_time_now.strftime("%X")

        owner_id = db.find_card_owner_id(db.database_filename, card_id)
        if owner_id == db.STOLEN_CARD_OWNER_ID:
            stolen_card_procedure()

        card_possession_info = db.get_card_possession_info(db.database_filename, card_id)

        db.add_log(db.database_filename, log_date, log_time, term_id, card_id, owner_id)

        log_msg = "Card %s has been used on %s on %s, %s. Card owner: %s" % (
            card_id, term_id, log_date, log_time, card_possession_info)
        tkinter.Label(window, text=log_msg).grid(sticky="W")

    else:
        client_id = message_decoded[1]
        client_status = message_decoded[0]
        tkinter.Label(window, text="%s is %s" % (client_id, client_status)).grid()


def stolen_card_procedure():
    tkinter.Label(window, text="A STOLEN CARD HAS BEEN USED!!!", fg="red").grid()


def assign_card(worker_id, card_id):
    db.assign_card(db.database_filename, worker_id, card_id)


def remove_card_assignment(card_id):
    db.remove_card_assignment(db.database_filename, card_id)


def connect_terminal(terminal_id):
    db.connect_terminal_to_system(db.database_filename, terminal_id)
    subscribe_terminal(terminal_id)


def mark_card_as_stolen(card_id):
    db.mark_card_as_stolen(db.database_filename, card_id)


def disconnect_terminal(terminal_id):
    db.disconnect_terminal_from_system(db.database_filename, terminal_id)
    unsubscribe_terminal(terminal_id)


def subscribe_terminal(terminal_id):
    client.subscribe("%s/log" % terminal_id)
    client.subscribe("%s/status" % terminal_id)


def unsubscribe_terminal(terminal_id):
    client.unsubscribe("%s/log" % terminal_id)
    client.unsubscribe("%s/status" % terminal_id)


def subscribe_connected_terminals():
    for terminal_data in terminals_data:
        terminal_id = terminal_data[0]
        is_term_connected_to_system = terminal_data[1]
        if is_term_connected_to_system:
            subscribe_terminal(terminal_id)


def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    subscribe_connected_terminals()


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


def create_main_window():
    window.geometry("230x400")
    window.title("Server")
    tkinter.Button(window, text="Stop", command=window.quit).grid()
    tkinter.Label(window, text="Logs and system info:", font=("Courier", 12), fg="green").grid()


if __name__ == "__main__":
    terminals_data = db.get_data(db.database_filename, "terminals")

    window = tkinter.Tk()
    connect_to_broker()
    create_main_window()
    window.mainloop()
    disconnect_from_broker()
