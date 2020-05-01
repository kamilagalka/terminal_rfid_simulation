import paho.mqtt.client as mqtt
import tkinter
import database_handling as db
import keyboard
import time

CARD_BLOCKAGE_TIME = 5

broker = "LAPTOP-KQDKQ66Q"
port = 8883

terminal_id = "T1"
client = mqtt.Client()

window = tkinter.Tk()

cards_data = db.get_data(db.database_filename, "cards")
list_of_cards = tkinter.Listbox(window, width=30, height=10)

cards_last_use_time = []
unknown_card_id = db.generate_random_card_id()


def create_main_window():
    window.geometry("410x310")
    window.title("Client %s" % terminal_id)

    # label with instruction
    tkinter.Label(window,
                  text="Click on this window to use %s terminal,\n"
                       "then choose card and press 'space' \n"
                       "to simulate card use" % terminal_id,
                  font=("Courier", 12), fg="green").grid()

    # cards
    tkinter.Label(window, text="Cards: ", font=("Courier", 15)).grid()
    for card_data in cards_data:
        card_id = card_data[0]
        list_of_cards.insert(tkinter.END, card_id)
    list_of_cards.insert(tkinter.END, "Unknown card")
    list_of_cards.grid()

    # exit instruction label
    tkinter.Label(window, text="Press 'esc' to exit", font=("Courier", 12), fg="red").grid()

    # prevent window closing using standard way
    def disable_event():
        pass

    window.protocol("WM_DELETE_WINDOW", disable_event)


def read_used_card_id():
    used_card_id = list_of_cards.get(tkinter.ANCHOR)
    if used_card_id == "Unknown card":
        used_card_id = unknown_card_id
    return used_card_id


def card_availability(used_card_id):
    for card in cards_last_use_time:
        card_id = card[0]
        if card_id == used_card_id:
            return False
    return True


def manage_new_log():
    used_card_id = read_used_card_id()
    is_any_card_marked = used_card_id != ''

    if is_any_card_marked:
        is_card_available = card_availability(used_card_id)

        if is_card_available:
            client.publish("%s/log" % terminal_id, used_card_id + "." + terminal_id, )
            print("%s/log" % terminal_id, used_card_id + "." + terminal_id, )
            cards_last_use_time.append((used_card_id, time.time()))


def connect_to_broker():
    client.tls_set("ca.crt")
    client.username_pw_set(username='client', password='password')
    client.connect(broker, port)
    client.publish("%s/status" % terminal_id, "online.%s" % terminal_id)


def disconnect_from_broker():
    client.publish("%s/status" % terminal_id, "offline.%s" % terminal_id)
    client.disconnect()


def update_cards_used_in_last_ten_secs():
    for card in cards_last_use_time:
        card_use_time = card[1]
        time_passed = time.time() - card_use_time

        if time_passed > CARD_BLOCKAGE_TIME:
            cards_last_use_time.remove(card)


def run():
    while True:
        window.update()
        update_cards_used_in_last_ten_secs()

        if window.focus_get():
            if keyboard.is_pressed('space'):
                manage_new_log()
            if keyboard.is_pressed('esc'):
                break

    # this sleep is added to prevent turning all clients off at once
    time.sleep(0.2)


if __name__ == "__main__":
    # create_clients()
    connect_to_broker()
    create_main_window()
    run()
    disconnect_from_broker()
