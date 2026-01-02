"""
PG APIs
Mostafa Rasouli
mostafarasooli54@gmail.com
2023-11-29
"""

import requests


URL = 'https://panel.aqayepardakht.ir/api/v2/'
PIN = 'EBC207EFC4AFB8B6AE62'
# PIN = 'sandbox'


def pg_get_err(e_code):
    if e_code == '-1':
        return 'مبلغ نمیتواند خالی باشد'
    elif e_code == '-2':
        return 'کد پین درگاه نمی تواند خالی باشد'
    elif e_code == '-3':
        return 'callback نمی تواند خالی باشد'
    elif e_code == '-4':
        return 'amount باید عددی باشد'
    elif e_code == '-5':
        return 'amount باید بین 1,000 تا 100,000,000 تومان باشد'
    elif e_code == '-6':
        return 'کد پین درگاه اشتباه هست'
    elif e_code == '-7':
        return 'transid نمی تواند خالی باشد'
    elif e_code == '-8':
        return 'تراکنش مورد نظر وجود ندارد'
    elif e_code == '-9':
        return 'کد پین درگاه با درگاه تراکنش مطابقت ندارد'
    elif e_code == '-10':
        return 'مبلغ با مبلغ تراکنش مطابقت ندارد'
    elif e_code == '-11':
        return 'درگاه درانتظار تایید و یا غیر فعال است'
    elif e_code == '-12':
        return 'امکان ارسال درخواست برای این پذیرنده وجود ندارد'
    elif e_code == '-13':
        return 'شماره کارت باید 16 رقم چسبیده بهم باشد'
    elif e_code == '-14':
        return 'درگاه برروی سایت دیگری درحال استفاده است'
    else:
        return 'خطای نامشخص'


def pg_get_pay_err(e_code):
    if e_code == '0':
        return 'پرداخت انجام نشد'
    elif e_code == '1':
        return 'پرداخت با موفقیت انجام شد'
    elif e_code == '2':
        return 'تراکنش قبلا وریفای و پرداخت شده است'
    else:
        return 'خطای نامشخص'


def pg_get_trans_id(data):
    body = {
        'pin': PIN,
        'amount': data.get('amount'),
        'callback': 'https://petshoproyal.com/order/verify-payment/',
        'invoice_id': data.get('invoice_id'),
    }
    response = requests.post(f'{URL}create/', json=body)

    return response


def pg_verify(data):
    body = {
        'pin': PIN,
        'amount': data.get('amount'),
        'transid': data.get('transid')
    }
    response = requests.post(f'{URL}verify/', json=body)

    return response
