import pyotp
import ghasedakpack
from datetime import datetime, timedelta
import http.client
import requests


def send_otp(request):
    sms = ghasedakpack.Ghasedak("759303b8731b6d7ce9370120b314fbeea5150d1012e5e1d1acb7724eacb6f2c3")
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key']= totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date']= str(valid_date)
    phone = request.session['phone']
    # sms.send({'message': f"کد شما برای ورود:  {otp}", 'receptor': f'0{phone}', 'linenumber': '30005006008968', 'checkid': 1})
    # sms.send({'message': f"کد شما برای ورود:  {otp}", 'receptor': f'0{phone}', 'linenumber': '30005006008968', 'checkid': 1})
    # sms.verification({'receptor': f'0{phone}', 'type': '1', 'template': 'test1', 'param1': otp})

    # print(sms.status({'id': 1, 'type': '1'}))


    url = "https://api.ghasedak.me/v2/verification/send/simple"
    payload = f"receptor=0{phone}&template=test1&type=1&param1={otp}"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'apikey': "759303b8731b6d7ce9370120b314fbeea5150d1012e5e1d1acb7724eacb6f2c3",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text

    # print(f"code is {otp}")




