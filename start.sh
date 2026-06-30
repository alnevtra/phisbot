kill $(ps aux | grep '[p]hp' | awk '{print $2}')
kill $(ps aux | grep 'serveo' | awk '{print $2}')
id="${1}"
pkill -f phis.py
for x in $(ls | grep "-");do rm -rf "$x"; done
python3 phis.py
token=`cat ./access/token.txt`
text="<b>Bot Berhasil Di Restart, gunakan /menu kembali untuk membuka menu</b>"
sleep 5
curl -s "https://api.telegram.org/bot${token}/sendMessage?chat_id=${id}&text=${text}&parse_mode=HTML" &> /dev/null