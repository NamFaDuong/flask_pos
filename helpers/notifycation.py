import requests
def sendNotifycation(html):
    bot_token = "7057681083:AAFcX4Xzw7s1bziMR7SKvSq3k2ZcgfIGQrA"
    chat_id = "@my_notification01"
    link = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={html}&parse_mode=HTML"
    res = requests.get(link)
    ress = res.status_code
    return ress
