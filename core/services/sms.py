from config.env import env

import requests

def send_sms_eskiz(phone, code):
    login_url = "https://notify.eskiz.uz/api/auth/login"
    token_res = requests.post(login_url, json={
        "email": env("ESKIZ_EMAIL"),
        "password": env("ESKIZ_PASSWORD")
    })
    token = token_res.json()['data']['token']

    sms_url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "mobile_phone": phone,
        "message": f"Sizning tasdiqlash kodingiz: {code}",
        "from": "4546"
    }

    response = requests.post(sms_url, headers=headers, json=data)
    return response.json()
