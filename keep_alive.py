from flask import Flask
from threading import Thread
import datetime


app = Flask('')


@app.route('/')
def main():
    return "Your bot is alive!"
def run():
    app.run(host="0.0.0.0", port=8080)
    print(now.strftime("%d-%m-%Y %H:%M"))

def keep_alive():
    server = Thread(target=run)
    server.start()

