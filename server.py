import paho.mqtt.client as mqtt
import tkinter
import database_handling as db
import datetime

broker = "localhost"
client = mqtt.Client()

window = tkinter.Tk()


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    print(message_decoded)
    if not message_decoded[0] == "connected" and not message_decoded[0] == "disconnected":
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

        log_msg = "Card %shas been used on %son %s, %s. Card owner: %s" % (
            card_id, term_id, log_date, log_time, card_possession_info)
        tkinter.Label(window, text=log_msg).grid(sticky="W")

    else:
        client_id = message_decoded[1]
        client_status = message_decoded[0]
        tkinter.Label(window, text="%s is %s" % (client_id, client_status)).grid()


def stolen_card_procedure():
    tkinter.Label(window, text="A STOLEN CARD HAS BEEN USED!!!", fg="red").grid()


def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("terminal/log")
    client.subscribe("client/status")


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


def create_main_window():
    window.geometry("230x400")
    window.title("Server")
    tkinter.Button(window, text="Stop", command=window.quit).grid()
    tkinter.Label(window, text="Logs and system info:", font=("Courier", 12), fg="green").grid()


if __name__ == "__main__":
    connect_to_broker()
    create_main_window()
    window.mainloop()
    disconnect_from_broker()
