import subprocess

def GetWifiPasswords() -> dict:
    profiles = list()
    passwords = dict()

    for line in subprocess.run('netsh wlan show profile', shell= True, capture_output= True).stdout.decode(errors= 'ignore').strip().splitlines():
        if 'All User Profile' in line:
            name= line[(line.find(':') + 1):].strip()
            profiles.append(name)
    
    for profile in profiles:
        found = False
        for line in subprocess.run(f'netsh wlan show profile "{profile}" key=clear', shell= True, capture_output= True).stdout.decode(errors= 'ignore').strip().splitlines():
            if 'Key Content' in line:
                passwords[profile] = line[(line.find(':') + 1):].strip()
                found = True
                break
        if not found:
            passwords[profile] = '(None)'
    return passwords if passwords != {} else "NONE"


def get_wifis_formatted():
    pws = GetWifiPasswords()

    if pws != "NONE":
        res = "%-35s%s" % ("Network","Password") + "\n"
        res += "%-35s%s" % ("───────","────────") + "\n"
        for i in pws:
            res += "%-35s%s" % (i,pws[i]) + "\n"
        return res
    else:
        return pws #NONE
