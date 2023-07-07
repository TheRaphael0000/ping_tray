import json
import time
import threading
import os

import pystray
from pystray import MenuItem as item
import requests
from PIL import Image


icon_size = 16
timeout = 120
root = os.path.dirname(os.path.abspath(__file__))
urls_path = os.path.join(root, "urls.json")


def mkimg(color):
    image = Image.new('RGB', (icon_size, icon_size), color)
    return image


def stop():
    icon.stop()


def resume(rs):
    lines = ""
    for r in rs:
        lines += f"{r.status_code} : {r.url}\n"
    return lines


def loop():
    while True:
        urls = json.load(open(urls_path))
        rs = []
        for url in urls:
            r = requests.get(url)
            rs.append(r)
        are_ok_status = [r.status_code == 200 for r in rs]

        if all(are_ok_status):
            icon.icon = mkimg("slategray")
            print(resume(rs))
        else:
            icon.icon = mkimg("red")
            icon.notify(resume(rs))

        if e.wait(timeout):
            break


e = threading.Event()
icon = pystray.Icon("ping tray", mkimg("orange"),
                    "Ping Tray", (item('Exit', stop),))

thread = threading.Thread(target=loop)
thread.start()
icon.run()
e.set()
