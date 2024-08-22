import requests


def profile_photo(file_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    r = requests.get(url).json()
    path = r["result"]["file_path"]
    return f"https://api.telegram.org/file/bot{bot_token}/{path}"