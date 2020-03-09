# Define
from eatple_app.define import *

# Django Library
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Models
from eatple_app.models import *

# Modules
from eatple_app.module_kakao.responseForm import *
from eatple_app.module_kakao.requestForm import *
from eatple_app.module_kakao.kakaoPay import *
from eatple_app.module_kakao.form import *
from eatple_app.module_kakao.validation import *

KAKAO_PAY_HOST_URL = 'kapi.kakao.com'
KAKAO_PAY_ONE_CLICK_API_ID = '5e5e74aa296f014f20f49d97'

KAKAO_PAY_CID = 'CADONE0860'


class KakaoPay():
    def OrderSheet(self, user, order_id, menu_name, menu_id, total_amount=6000, quantity=1, order=None):
        headers = {
            'Authorization': 'KakaoAK {app_key}'.format(app_key=KAKAO_ADMIN_KEY),
        }

        data = {
            'cid': KAKAO_PAY_CID,

            'partner_order_id': order_id,
            'partner_user_id': user.app_user_id,

            'item_name': menu_name,
            'item_code': menu_id,

            'quantity': 1,

            'total_amount': total_amount,
            'vat_amount': 200,

            'tax_free_amount': 0,

            'approval_url': 'https://dev.eatple.com/success',
            'cancel_url': 'https://dev.eatple.com/fail',
            'fail_url': 'https://dev.eatple.com/cancel',
        }

        apiURL = '{shcme}{host}{url}'.format(
            shcme='https://', host=KAKAO_PAY_HOST_URL, url='/v1/payment/ready')

        kakaoResponse = requests.post(apiURL, data=data, headers=headers)

        return kakaoResponse

    def PaymentApprove(self, tid, order_id, user_id, pg_token, cid_secret=None, payload=None, total_amount=0):
        headers = {
            'Authorization': 'KakaoAK {app_key}'.format(app_key=KAKAO_ADMIN_KEY),
        }

        apiURL = '{shcme}{host}{url}'.format(
            shcme='https://', host=KAKAO_PAY_HOST_URL, url='/v1/payment/approve')

        data = {
            'cid': KAKAO_PAY_CID,
            'tid': tid,
            'pg_token': pg_token,

            'partner_order_id': order_id,
            'partner_user_id': user_id,

            'total_amount': total_amount,
        }

        print(data)

        kakaoResponse = requests.post(apiURL, data=data, headers=headers)

        return kakaoResponse
