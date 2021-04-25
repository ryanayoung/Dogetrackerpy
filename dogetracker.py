import PySimpleGUI as sg
import json, time, sys
from websocket import create_connection

for i in range(3):
    try:
        ws = create_connection("wss://ws.kraken.com")
    except Exception as error:
        print('Caught this error: ' + repr(error))
        time.sleep(5)
    else:
        break

ws.send(json.dumps({
    "event": "subscribe",
    "pair": ["DOGE/USD"],
    "subscription": {"name": "ticker"}
}))

try:
        result = ws.recv()
        result = json.loads(result)
except Exception as error:
        print('Caught this error: ' + repr(error))

try:
        result = ws.recv()
        result = json.loads(result)
except Exception as error:
        print('Caught this error: ' + repr(error))
column_data = [
    [sg.Text('Connecting...', size=(40,1), auto_size_text=True,justification='left', background_color='black', text_color='red', font=('Franklin Gothic Book',16), relief='sunken', key="_DISPLAY_")],
    [sg.Text('Doge to track'),sg.InputText('0', size=(20, 1)),sg.Button('WOW')]
]

layout: list = [
    [sg.Image(filename = "Dogecoin_Logo.png"),sg.Column(column_data)]
]

window = sg.Window('Much Track', layout,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0), finalize=True,
                   right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT)

def update_display(display_value: str):
    window['_DISPLAY_'].update(value=display_value)

def time_as_int():
    return int(round(time.time() * 100))

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

my_doge = 0
max_count = 0
while True:
    # --------- Read and update window --------
    event, values = window.read(timeout=10)
    current_time = time_as_int() - start_time
    if event in (sg.WIN_CLOSED, None):        # ALWAYS give a way out of program
        ws.close()
        break
    if event in ['WOW']:
        #print(values)
        try:
            my_doge = float(values[1])
            output = "XDG/USD: $%(val)4f Your Doge: $%(mine)4f" % {"val":doge_val, "mine":doge_val * my_doge}
            update_display(output)
        except ValueError:
            update_display("Numbers Only")
    current_sec = (current_time // 100) % 60
    if current_sec >= max_count:
        start_time = time_as_int()
        max_count = 30
        try:
            result = ws.recv()
            result = json.loads(result)
            #print("XDG/USD: %(val)s Your Doge: %(mine)4f" % {"val":result[1]['a'][0], "mine":float(result[1]['a'][0]) * 6826.80200729})
            doge_val = float(result[1]['a'][0])
        except KeyError:
            #print('test')
            max_count = 5
            pass

        output = "XDG/USD: $%(val)4f Your Doge: $%(mine)4f" % {"val":doge_val, "mine":doge_val * my_doge}
        update_display(output)

