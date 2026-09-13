from curl_cffi import requests
import re
import secrets
import string
from telethon import TelegramClient, events
from datetime import datetime, timedelta,timezone

def WriteLog(message):
    utc_now = datetime.now(timezone.utc)
    utc_plus_8 = utc_now + timedelta(hours=8)
    time_str = utc_plus_8.strftime("%Y-%m-%d %H:%M:%S")
    with open("ccs.txt", "a+", encoding="utf-8") as f:
        f.write(time_str+'\t'+message+'\n')
    print(time_str+'\t'+message)

def gen_str(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def gen_num(length=3):
    chars = string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

data_2 = {
    'validate_promo_code':'1',
    'code':'',
    'service_id':'',
}

data_3 = {
    "promo_code": "",
    "additional_requests": "",
    "subzone_id": "0",
    "addon_1_1": "0",
    "addon_1_2": "0",
    "addon_1_3": "0",
    "addon_2_1": "0",
    "addon_2_2": "0",
    "addon_2_3": "0",
    "addon_2_4": "0",
    "global_16_1": "0",
    "global_5_1": "0",
    "global_5_2": "0",
    "global_5_3": "0",
    "account_data_first_name": "",#
    "account_data_last_name": "",#
    "account_data_organization": "",
    "account_data_email": "",#
    "account_data_phone": "",#
    "account_data_address": "",#
    "account_data_city": "",#
    "account_data_us_can_state": "OR",
    "account_data_country": "US",
    "account_data_zipcode": "",#
    "account_data_password1": "",#
    "account_data_password2": "",#
    "referred_by": "0",
    "referred_by_comment": "",
    "account_billing_payment_method": "1",
    "agree_tos": "on",
    "currency": "USD",
    "payment_term": "annual",
    "add_registration_form": "1",
    "requiredfield": "",
    "age": "",
    "service_id": "644"
}
data_3["account_data_password2"] = data_3["account_data_password1"]

def Gene_Data():
    data_3["account_data_first_name"] = gen_str()
    data_3["account_data_last_name"] = gen_str()
    data_3["account_data_phone"] = gen_num(10)
    data_3["account_data_address"] = gen_str()
    data_3["account_data_city"] = gen_str()
    data_3["account_data_zipcode"] = gen_num(5)
    data_3["account_data_email"] = 'a'+gen_str(11) + "@outlook.com"
    data_3["account_data_password1"] = 'Aa1.'+gen_str(8)
    data_3["account_data_password2"] = data_3["account_data_password1"]

url_1 = 'https://portal.colocrossing.com/register/order/service/650'
url_2 = 'https://portal.colocrossing.com/register/async'
url_3 = 'https://portal.colocrossing.com/register/register'

def CreateOrder(pid,code):
    data_2['service_id'] = f"{pid}"
    data_2['code'] = f"{code}"
    data_3["service_id"] = f"{pid}"
    data_3["promo_code"] = f"{code}"
    url_1 = 'https://portal.colocrossing.com/register/order/service/'+f'{pid}'
    Gene_Data()

    session = requests.Session(impersonate="chrome101")
    ret_1 = session.get(url_1, impersonate="chrome101")
    ret_2 = session.post(url_2, data=data_2, impersonate="chrome101")
    ret_3 = session.post(url_3,data=data_3, impersonate="chrome101")

    WriteLog(pid)
    WriteLog(code)
    WriteLog(ret_2.text)
    WriteLog(data_3["account_data_email"])
    WriteLog(data_3["account_data_password2"])

    with open(f"1.html", "w", encoding="utf-8") as f:
        f.write(ret_1.text)
    with open(f"2.html", "w", encoding="utf-8") as f:
        f.write(ret_2.text)
    with open(f"3.html", "w", encoding="utf-8") as f:
        f.write(ret_3.text)

#*********************************************************************

api_id = 1
api_hash = ""

client = TelegramClient('tg', api_id, api_hash)

#ccs频道id -1003063081571
@client.on(events.NewMessage(chats=-1003063081571))
async def handler(event):
    message = event.message.message
    redi_url = re.search(r'temporary-url\.com\/([A-Za-z0-9]+)', event.message.message)
    if (redi_url):
        temp_id = redi_url.group(1)
        url_temp = f"https://www.temporary-url.com/message.php?code={temp_id}"
        message = requests.get(url_temp,impersonate="chrome101").text
    pid = re.search(r'(?<=/service/)\d+', message)
    code = re.search(r'Coupon Code:\s*([A-Za-z0-9]+)', message,re.IGNORECASE)
    if pid and code:
        pid = pid.group(0)
        code = code.group(1)
        CreateOrder(pid,code)


client.start()
client.run_until_disconnected()
