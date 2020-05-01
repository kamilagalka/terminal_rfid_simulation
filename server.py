import paho.mqtt.client as mqtt
import tkinter
import database_handling as db
import datetime

broker = "LAPTOP-KQDKQ66Q"
port = 8883
client = mqtt.Client()


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    if not message_decoded[0] == "online" and not message_decoded[0] == "offline":
        used_card_id = message_decoded[0]
        used_terminal_id = message_decoded[1]
        process_new_log(used_card_id, used_terminal_id)
    else:
        client_id = message_decoded[1]
        client_status = message_decoded[0]
        tkinter.Label(window, text="%s is %s" % (client_id, client_status)).grid()


def process_new_log(used_card_id, used_terminal_id):
    date_time_now = datetime.datetime.now()
    log_date = get_date_from_datetime(date_time_now)
    log_time = get_time_from_datetime(date_time_now)

    owner_id = db.find_card_owner_id(db.database_filename, used_card_id)
    if owner_id == db.STOLEN_CARD_OWNER_ID:
        stolen_card_procedure()

    db.add_log(db.database_filename, log_date, log_time, used_terminal_id, used_card_id, owner_id)

    card_assignment_info = db.get_card_assignment_info(db.database_filename, used_card_id)
    log_msg = "Card %s has been used on %s on %s, %s. Card assignment: %s" % (
        used_card_id, used_terminal_id, log_date, log_time, card_assignment_info)

    tkinter.Label(window, text=log_msg).grid(sticky="W")


def get_date_from_datetime(date_time):
    date = date_time.strftime("%d") + "." + date_time.strftime("%m") + "." + date_time.strftime(
        "%y")
    return date


def get_time_from_datetime(date_time):
    time = date_time.strftime("%X")
    return time


def stolen_card_procedure():
    tkinter.Label(window, text="A STOLEN CARD HAS BEEN USED!!!", fg="red").grid()


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
    client.tls_set("ca.crt")
    client.username_pw_set(username='server', password='password')
    client.connect(broker, port)
    client.on_message = process_message
    client.loop_start()
    subscribe_connected_terminals()


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


def create_main_window():
    window.geometry("600x400")
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
