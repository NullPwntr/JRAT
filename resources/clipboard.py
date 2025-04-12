from PIL import ImageGrab
import pyperclip

def getClipboard():
    image = ImageGrab.grabclipboard()
    clipboard_content = pyperclip.paste()

    return image if image else clipboard_content