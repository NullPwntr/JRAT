import requests

def send_limited(exipre_time : str, file_bytes : str):
    files = {
        'fileToUpload': file_bytes 
    }

    payload = {
        'time': exipre_time, #1h, 12h, 1d, 3d
        'reqtype': 'fileupload'
    }

    response = requests.post('https://litterbox.catbox.moe/resources/internals/api.php',files=files, data=payload)

    return response.status_code, response.text
