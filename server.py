import paho.mqtt.client as mqtt
import tkinter
import database_handling as db
import datetime

broker = "localhost"
client = mqtt.Client()

window = tkinter.Tk()

database_filename = "test2.db"


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    if not message_decoded[0].__contains__("connected") and not message_decoded[0].__contains__("disconnected"):
        card_id = message_decoded[0]
        term_id = message_decoded[1]

        date_time_now = datetime.datetime.now()
        log_date = date_time_now.strftime("%d") + "." + date_time_now.strftime("%m") + "." + date_time_now.strftime(
            "%y")
        log_time = date_time_now.strftime("%X")

        worker_id = db.find_owner_id(database_filename, card_id)
        if worker_id == -1:
            stolen_card_procedure()

        db.add_log(database_filename, log_date, log_time, term_id, card_id, worker_id)
        print("Card %s has been used on %s on %s, %s" % (card_id, term_id, log_date, log_time))
        log_msg = "Card %s has been used on %s on %s, %s" % (card_id, term_id, log_date, log_time)
        tkinter.Label(window, text=log_msg).grid()
    else:
        print(message_decoded[0])
        tkinter.Label(window, text=message_decoded[0]).grid()


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
