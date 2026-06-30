#importing system libraries
import datetime
import subprocess
import time

from os import name, system
from time import sleep

import progressbar
import telebot
from telebot import types

from features.captcha import *
from features.custom import *
from features.gdrive import *
from features.logs import *
from features.short import *

#------------------------------------------------------------------------------------------------------------------

TOKEN = open('./access/token.txt', 'r')
API = TOKEN.read()

# LOGBOT_TOKEN = open('./access/logbot.txt', 'r')
# LOGBOT_API = LOGBOT_TOKEN.read()
# LOGBOT = telebot.TeleBot(LOGBOT_API)

# BOT INFORMATION
BOT = telebot.TeleBot(API)
BOT_NAME = 'Mancing Mania'
BOT_VERSION = "1"
BOT_SITE = "https://alnevtra.gitbook.io/btrack/"

# ADMIN INFORMATION
DEV_NAME = "Xsint Team"
DEV_ID = "1307571787"
DEV_TELEGRAM = "t.me/alnevtra"

# STATUS CODE
E404 = "NOT FOUND"
E403 = "FORBIDDEN"
E500 = "INTERNAL SERVER ERROR"
delmenu = types.ReplyKeyboardRemove()

# ----------------------------------------------------------------------------------------------------------------------

# E403 MESSAGE
def E403_MSG(ctx):
    BOT.send_message(
        DEV_ID,
        f"""<b>ALERT : NOT AUTHORIZED</b>

<b>CODE :</b> <code>403</code> 
<b>STATUS :</b> <code>{E403}</code> 
<b>DATE :</b> <i> {datetime.datetime.now().strftime("%d %m %Y - %H:%M:%S").upper()} </i>

<b>THREAT ACTOR :</b>
 -- <b>First Name  :</b> <i>{ctx.chat.first_name}</i>
 -- <b>Last Name   :</b> <i>{ctx.chat.last_name}</i>
 -- <b>Username    :</b> <i>{ctx.chat.username}</i>
 -- <b>Telegram Id :</b> <i>{ctx.chat.id}</i>

 -- <b>MESSAGE :</b>
User tidak terdaftar mencoba untuk {ctx.text} command 
        """,
        parse_mode="html",
    )

# E404 MESSAGE
def E404_MSG(ctx):
    BOT.send_message(
        DEV_ID,
        f"""<b>ALERT : NOT FOUND</b>

<b>CODE   :</b> <code>404</code>
<b>STATUS :</b> <code>{E404}</code>
<b>DATE   :</b> {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").upper()}

<b>THREAT ACTOR :</b>
 -- <b>First Name  :</b> <i>{ctx.chat.first_name}</i>
 -- <b>Last Name   :</b> <i>{ctx.chat.last_name}</i>
 -- <b>Username    :</b> <i>{ctx.chat.username}</i>
 -- <b>Telegram Id :</b> <i>{ctx.chat.id}</i>

 -- <b>MESSAGE :</b>
User try use {ctx.text} command 
        """,
        parse_mode="html",
    )

# E500 MESSAGE
def E500_MSG(ctx):
    BOT.send_message(
        DEV_ID,
        f"""<b>ALERT : INTERNAL SERVER ERROR</b>

<b>CODE   :</b> <code>500</code>
<b>STATUS :</b> <code>{E500}</code>
<b>DATE   :</b> {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").upper()}

<b>THREAT ACTOR :</b>
 -- <b>First Name  :</b> <i>{ctx.chat.first_name}</i>
 -- <b>Last Name   :</b> <i>{ctx.chat.last_name}</i>
 -- <b>Username    :</b> <i>{ctx.chat.username}</i>
 -- <b>Telegram Id :</b> <i>{ctx.chat.id}</i>

 -- <b>MESSAGE :</b>
Error while running {ctx.text} command 
        """,
        parse_mode="html",
    )


# F403 MESSAGE
def F403_MSG(ctx):
    BOT.send_message(
        ctx.chat.id,
        f"""No Access""",
        parse_mode="html",
    )

# F404 MESSAGE
def F404_MSG(ctx):
    BOT.send_message(
        ctx.chat.id,
        f"""Oops.. It seems that you are trying to use command that does not exist!
For more information please contact {DEV_TELEGRAM}, Thank you!

Best Regards,
{DEV_NAME}
""",
        parse_mode="html",
    )

# F500 MESSAGE
def F500_MSG(ctx):
    BOT.send_message(
        ctx.chat.id,
        f"""Oops.. Sepertinya terjadi kesalahan didalam system Bot.

Kemungkinan error :
- kesalahan dalam input data
- Koneksi di server pusat tidak stabil
- Server tidak bisa mengirimkan pesan
- API Service error atau gangguan.

Check kembali data yang anda cari dan ulangi proses pencarian beberapa saat lagi.""",
        parse_mode="html",
    )

# START MESSAGE
def START_MSG(ctx):
    BOT.send_message(
        ctx.chat.id,
        f"""<b>Welcome To {BOT_NAME},</b> <i>{ctx.chat.username}</i>

<b>TERM & CONDITION MANCING MANIA Bot :</b>

<b>1. BOT INI DIGUNAKAN OLEH APARAT DENGAN KEWENANGAN KHUSUS, TIDAK UNTUK KEPENTINGAN PRIBADI DAN HANYA UNTUK UPAYA PENEGAKKAN HUKUM.</b>

<b>2. BOT INI TIDAK BOLEH DIKOMERSILKAN KEMBALI TANPA SEIJIN DARI PIHAK PENYEDIA BOT RESMI. </b>

<b>3. ISI DAN HASIL DARI PENCARIAN DALAM BOT BAIK SEBAGIAN MAUPUN KESELURUHAN, DILARANG UNTUK DISEBARLUASKAN ATAU DIPERJUALBELIKAN DALAM BENTUK FILE, SCREENSHOT, EKSTENSI, DAN / ATAU DI PUBLIKASIKAN DENGAN CARA APAPUN DI MEDIA SOSIAL, DI MEDIA UMUM LAINNYA KEPADA MASYARAKAT SIPIL ATAU DILUAR DARI APARAT PENEGAK HUKUM.</b>

Gunakan /help untuk mengetahui penjelasan dari menu
Dan /menu untuk membuka menu.

Jika ada kendala atau fitur tidak berfungsi hubungi {DEV_TELEGRAM}. 

Terima Kasih.
        """,
        parse_mode="html",
    )

# MAINMENU MESSAGE
MAINMENU_MESSAGE = """<b>{}</b> Version {}

<b>What's new in v{} :</b>
    <i>- Stable script</i>

<b>Premium Expired in:</b> <i>{}</i>

<i>Silahkan pilih menu yang tersedia</i>"""

# ----------------------------------------------------------------------------------------------------------------------

# BOT_CPR
def BOT_CPR():
    print(f'''
=========================== STARTING BOT ===========================

[!] BOT Name : {BOT_NAME}
[!] BOT Version : {BOT_VERSION}

This code originally written by @alnevtra,

Instagram : @alnevtra
Telegram : t.me/alnevtra

DIGUNAKAN OLEH APARAT DENGAN KEWENANGAN KHUSUS,
TIDAK UNTUK KEPENTINGAN PRIBADI DAN HANYA UNTUK UPAYA PENEGAKAN HUKUM.

============================ START LOGS =============================
''')

# CLEARSCREEN
def BOT_CLEAR():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# LOADING
def BOT_LOADING(ctx):
    widgets = ['LOADING : ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
      
    for i in range(ctx):
        time.sleep(0.1)
        bar.update(i)

# BOT_POLLING
def BOT_POLLING():
    BOT.infinity_polling(timeout=10, long_polling_timeout=5)

# BOT_STATUS
def BOT_STATUS():
    BOT_CLEAR()
    print("SYSTEM : STARTING..")
    BOT_LOADING(5)
    print("SYSTEM : STARTED")

    i = 0
    for i in range(3):
        BOT_LOADING(5)
        sleep(0.5)
        i+=1

    BOT_CLEAR()
    print("SYSTEM : BOT IS RUNNING..")
    BOT_CPR()
    BOT_POLLING()
    if BOT_POLLING() == True:
        BOT_CLEAR()
        print("SYSTEM : BOT IS RUNNING..")
    else:
        BOT_CLEAR()
        print("SYSTEM : STOPPED..")

# BOT_AUTH
def BOT_AUTH(ctx):
    try:
        USERS = open("./access/users.txt", "r")  # Open users.txt
        USERS = USERS.read()  # Read users.txt

        if str(ctx.chat.username) in USERS:
            return True
        else:
            return False
    except:
        E500_MSG(ctx=ctx)

# BOT_LOG
def BOT_USERLOGS(ctx,perintah): # start logging
    try:
        date = datetime.datetime.now()
        date = date.strftime('%d-%B-%Y %H:%M:%S')
        username = ctx.chat.username
        userid = ctx.chat.id
        usermsg = ctx.text
        logs_text = '{}, {}:{} Check => {} {} \n'.format(date, username, userid, perintah, usermsg)
        logs_cli = '{}, {}:{} Check => {} {}'.format(date, username, userid, perintah, usermsg)
        # send_to_admin = '{}, <b>{}</b> Check : {} <code>{}</code>'.format(date, username, perintah, usermsg)
        # LOGBOT.send_message(DEV_ID, '{}'.format(send_to_admin), parse_mode='html')
        print(logs_cli)
        BOT_logging = open('./logs/users/user_logs.txt','a')
        BOT_logging.write(logs_text)
        BOT_logging.close()
    except:
        BOT.send_message(DEV_ID, 'Theres an error in logs function')

# ----------------------------------------------------------------------------------------------------------------------

# BOT_START
def BOT_START(ctx):
    BOT_AUTH(ctx=ctx)
    if BOT_AUTH(ctx=ctx) == True:
        START_MSG(ctx=ctx)
    else:
        F403_MSG(ctx=ctx)
        E403_MSG(ctx=ctx)

# BOT_MENU
def BOT_MAINMENU(ctx):
    BOT_AUTH(ctx=ctx)
    if BOT_AUTH(ctx=ctx) == True:
        try:
            USERS_EXPIRED_DATE = subprocess.check_output(
                f"cat ./access/users.txt | grep -i '{ctx.chat.username}'",
                shell=True,
                encoding="utf8",
            ).rstrip()
            USERS_EXPIRED_DATES = USERS_EXPIRED_DATE.split("|", 3)[2]
            DATE_NOW = datetime.datetime.now()
            DATE_EXPIRED = datetime.datetime.strptime(USERS_EXPIRED_DATES, "%d/%m/%Y")
            EXPIRED = "%d days" % ((DATE_EXPIRED - DATE_NOW).days)
            USER_STATUSES = USERS_EXPIRED_DATE.split("|", 3)[1]
            if str(ctx.chat.username) == "alnevtra":
                EXPIRED = "Unlimited (You Are Bot Developer)"

            elif DATE_EXPIRED < DATE_NOW:
                if USER_STATUSES == "user":
                    BOT.send_message(
                        ctx.chat.id,
                        f"""<b>PREMIUM ACCESS EXPIRED</b>
                    
Untuk tetap menggunakan <b>{BOT_NAME}</b>, Silahkan Perpanjang Premium Anda.

<b>Payment :</b>

<b>BCA</b>
<b>No rekening :</b> <code>7900339997</code>
<b>Atas nama :</b> <i>Hilmy Rizal, SH</i>

<i>Mohon untuk mengirimkan bukti transfer setelah melakukan pembayaran kepada t.me/hilmibrewok, Terima Kasih.</i>
                    """,
                    parse_mode="html",
                    )
                    return
                elif USER_STATUSES == "demo":
                    BOT.send_message(
                        ctx.chat.id,
                        f"""<b>DEMO ACCESS EXPIRED</b>

Untuk tetap menggunakan <b>{BOT_NAME}</b>, Silahkan upgrade ke akun premium.

<b>Payment :</b>

<b>BCA</b>
<b>No rekening :</b> <code>7900339997</code>
<b>Atas nama :</b> <i>Hilmy Rizal, SH</i>

<i>Mohon untuk mengirimkan bukti transfer setelah melakukan pembayaran kepada t.me/hilmibrewok, Terima Kasih.</i>""",
                        parse_mode="html",
                    )
                    return
            
            elif USER_STATUSES == "admin":
                EXPIRED = "Unlimited (You Are Bot Admin)"
            elif USER_STATUSES == "partner":
                EXPIRED = "Unlimited (Special Access From Admin)"
        except:
            E500_MSG(ctx=ctx)
        
        # start main menu
        MAINMENU = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )

        x01 = types.KeyboardButton("CREATE")
        x02 = types.KeyboardButton("SHORT URL")
        x03 = types.KeyboardButton("LOGS")
        x04 = types.KeyboardButton("Close Menu")

        MAINMENU.row(x01, x02)
        MAINMENU.row(x03)
        MAINMENU.row(x04)
        
        msg = BOT.send_message(
            ctx.chat.id,
            MAINMENU_MESSAGE.format(BOT_NAME, BOT_VERSION, BOT_VERSION, EXPIRED),
            reply_markup=MAINMENU,
            parse_mode="html",
        )
        BOT.register_next_step_handler(
            msg, 
            MAINMENU_INPUT
        )
        
    else:
        F403_MSG(ctx=ctx)
        E403_MSG(ctx=ctx)

#BOT_MAINMENU_INPUT
def MAINMENU_INPUT(ctx):
    if ctx.text == "CREATE":
        BOT_CREATE(ctx=ctx)
    
    elif ctx.text == "SHORT URL":
        SHORT_MSG = """Short URL adalah versi singkat dari suatu URL yang memudahkan orang lain mengingat suatu URL, misalnya URL website bisnis, URL promosi, dan sebagainya. Short URL juga memberi kesan rapi ketika URL yang panjang dibagikan ke media sosial.
        
Silakan input dengan URL/link yang ingin anda short:"""
        msg = BOT.send_message(
            ctx.chat.id,
            SHORT_MSG,
            parse_mode="html",
        )
        BOT.register_next_step_handler(msg, BOT_SHORT)

    elif ctx.text == "LOGS":
        log_file = open('./db/result_logs.txt', 'rb')
        BOT.send_document(ctx.chat.id, log_file)
        log_file.close()
    
    elif ctx.text == "Close Menu":
        BOT.send_message(
            ctx.chat.id, 
            "<b>MENU CLOSED!!</b>", 
            parse_mode="html", 
            reply_markup=delmenu
        )
    else:
        F404_MSG(ctx=ctx)
        BOT_MAINMENU(ctx=ctx)

# BOT_CREATE
def BOT_CREATE(ctx):
    CREATEMENU = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    C1 = types.KeyboardButton("CAPTCHA")
    C2 = types.KeyboardButton("GDRIVE")
    C3 = types.KeyboardButton("CUSTOM")
    C4 = types.KeyboardButton("Back")
    C5 = types.KeyboardButton("Close Menu")
    CREATEMENU.row(C1, C2, C3)
    CREATEMENU.row(C4, C5)
    msg = BOT.send_message(
        ctx.chat.id,
        """Berikut adalah pilihan menu yang tersedia pilih salah satu sesuai kebutuhan phising
        
<b>CHAPTCA</b> : Untuk membuat phising chaptca
<b>GDRIVE</b> : Untuk membuat phising gdrive
<b>CUSTOM</b> : Untuk membuat phising custom""",
        reply_markup=CREATEMENU,
        parse_mode="html",
    )
    BOT.register_next_step_handler(msg, CREATE_INPUT)

# BOT_CREATE_INPUT
def CREATE_INPUT(ctx):
    CHAPTCA_MSG = """Captcha phising adalah phising yang meminta korban untuk memasukan captcha terlebih dahulu sebelum masuk ke halaman asli.

Silahkan input dengan link berita, sosmed, youtube, atau apapun yang ingin anda phising

contoh : https://www.cnn.com"""

    GDRIVE_MSG = """Gdrive phising adalah phising yang mengharuskan target klik allow location untuk mendapatkan file google drive yg asli.

Silahkan input dengan link file google drive 

contoh : https://drive.google.com/blablablabla"""

    CUSTOM_MSG = """Custom adalah phising location yang pada saat mengirim ke target akan sangat mirip ketika kita mengirim link asli nya
    
Silahkan input dengan link berita, sosmed, youtube, atau apapun yang ingin anda phising"""

    if ctx.text == "CAPTCHA":
        msg = BOT.send_message(
            ctx.chat.id,
            CHAPTCA_MSG,
            parse_mode="html",
        )
        BOT.register_next_step_handler(msg, BOT_CAPTCHA)

    elif ctx.text == "GDRIVE":
        msg = BOT.send_message(
            ctx.chat.id,
            GDRIVE_MSG,
            parse_mode="html",
        )
        BOT.register_next_step_handler(msg, BOT_GDRIVE)

    elif ctx.text == "CUSTOM":
        msg = BOT.send_message(
            ctx.chat.id,
            CUSTOM_MSG,
            parse_mode="html",
        )
        BOT.register_next_step_handler(msg, BOT_CUSTOM)

    elif ctx.text == "Close Menu":
        BOT.send_message(
            ctx.chat.id, 
            "<b>MENU CLOSED!!</b>", 
            parse_mode="html", 
            reply_markup=delmenu
        )
    else:
        F404_MSG(ctx=ctx)
        BOT_CREATE(ctx=ctx)

# ----------------------------------------------------------------------------------------------------------------------

@BOT.message_handler(commands=["start"])
def msg(ctx): # START Endpoint
    BOT.send_chat_action(ctx.chat.id, "typing")  # Send typing action
    BOT_USERLOGS(ctx,'Start')
    try:
        BOT_START(ctx=ctx)
    except:
        E500_MSG(ctx=ctx)

@BOT.message_handler(commands=["restart"])
def msg(ctx): # RESTART Endpoint
    chat_id = ctx.chat.id
    os.system(f'bash start.sh {chat_id}')

# ----------------------------------------------------------------------------------------------------------------------

@BOT.message_handler(commands=["menu"])
def msg(ctx): # MAINMENU Endpoint
    BOT.send_chat_action(ctx.chat.id, "typing")  # Send typing action
    if str(ctx.text) == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    try:
        BOT_MAINMENU(ctx=ctx)
    except:
        E500_MSG(ctx=ctx)
        F500_MSG(ctx=ctx)

def msg(ctx): # MAINMENU Input Endpoint
    BOT.send_chat_action(ctx.chat.id, "typing")  # Send typing action
    if str(ctx.text) == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    try:
        MAINMENU_INPUT(ctx=ctx)
    except:
        E500_MSG(ctx=ctx)
        F500_MSG(ctx=ctx)

def msg(ctx): # OSINTMENU Endpoint
    BOT.send_chat_action(ctx.chat.id, "typing")  # Send typing action
    if str(ctx.text) == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    try:
        BOT_CREATE(ctx=ctx)
    except:
        E500_MSG(ctx=ctx)
        F500_MSG(ctx=ctx)

def msg(ctx): # OSINTMENU Input Endpoint
    BOT.send_chat_action(ctx.chat.id, "typing")  # Send typing action
    if str(ctx.text) == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    try:
        CREATE_INPUT(ctx=ctx)
    except:
        E500_MSG(ctx=ctx)
        F500_MSG(ctx=ctx)

def BOT_SHORT(ctx): # Start Number Endpoint
    if ctx.text == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    BOT.send_chat_action(ctx.chat.id, "typing")
    try:
        short_url(ctx=ctx)
    except Exception as e:
        # print(e)
        F500_MSG(ctx=ctx)
        E500_MSG(ctx=ctx)
        BOT.send_message(DEV_ID, f'Error : {e} on BOT_CHAPTCA')

def BOT_CAPTCHA(ctx): # Start Number Endpoint
    if ctx.text == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    BOT.send_chat_action(ctx.chat.id, "typing")
    try:
        captcha(ctx=ctx)
    except Exception as e:
        # print(e)
        F500_MSG(ctx=ctx)
        E500_MSG(ctx=ctx)
        BOT.send_message(DEV_ID, f'Error : {e} on BOT_CHAPTCA')
        
def BOT_GDRIVE(ctx): # Start IMEI Endpoint
    if ctx.text == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    BOT.send_chat_action(ctx.chat.id, "typing")
    try:
        gdrive(ctx=ctx)
    except Exception as e:
        # print(e)
        F500_MSG(ctx=ctx)
        E500_MSG(ctx=ctx)
        BOT.send_message(DEV_ID, f'Error : {e} on BOT_GDRIVE')

def BOT_CUSTOM(ctx): # Start Email Endpoint
    if ctx.text == "/menu":
        BOT_MAINMENU(ctx=ctx)
        return
    elif ctx.text == "/cancel":
        BOT.send_message(
            ctx.chat.id,
            '''<b>Features Canceled</b>

Gunakan /menu untuk membuka kembali menu utama''',
            parse_mode="html",
        )
        return
    BOT.send_chat_action(ctx.chat.id, "typing")
    try:
        custom(ctx=ctx)
    except Exception as e:
        # print(e)
        F500_MSG(ctx=ctx)
        E500_MSG(ctx=ctx)
        BOT.send_message(DEV_ID, f'Error : {e} on BOT_CUSTOM')

# ----------------------------------------------------------------------------------------------------------------------

BOT_STATUS()