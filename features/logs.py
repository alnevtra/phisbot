import telebot
import subprocess
import json

# ----------------------------------------------------------------------------------------------------------------------
# ACCESS TOKEN
TOKEN = subprocess.check_output(
    "cat ./access/token.txt",
    shell=True,
    encoding="utf-8",
).strip()
API = f"{TOKEN}"
BOT = telebot.TeleBot(API)

# ----------------------------------------------------------------------------------------------------------------------