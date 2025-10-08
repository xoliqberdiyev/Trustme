import requests

from config.env import env

def send_sms_code(code, type, phone):
    url = f'https://api.telegram.org/bot{env.str('BOT_TOKEN')}/sendMessage'
    payload = {
        'chat_id': '-1003156599780',
        'text': f'Sizning tasdiqlash kodingiz: {code}, \n Type: {type} \n Telefon raqam: {phone}',
        'parse_mode': 'HTML', 
    }
    return requests.post(url, data=payload)
    