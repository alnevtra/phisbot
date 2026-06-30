import telebot
import subprocess
import os
import sys
import argparse
import requests
import traceback
from time import sleep
from os import path, kill, mkdir
from json import loads, decoder
from packaging import version
from ipaddress import ip_address

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

def short_url(ctx):
    url = ctx.text
    isgd = requests.get(f'https://is.gd/create.php?format=simple&url={url}').text
    BOT.send_message(ctx.chat.id, f"""<b>[ Berhasil Shorting URL ]</b>

<b>Real URL :</b> {url}

<b>Shorted URL :</b> {isgd}""", parse_mode="html")