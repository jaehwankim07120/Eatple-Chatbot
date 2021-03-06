# View-System
from eatple_app.views_system.include import *
from eatple_app.views_system.debugger import *

KAKAO_BIZ_HOST_URL = 'talkapi.lgcns.com'

LG_CNS_API_KEY = 'HWJAKot/V7GtnRdKxnuqCA=='
LG_CNS_API_ID = 'eatple2020'
LG_CNS_SERVICE_ID = 1910037945


class KakaoBiz():
    def request(self, message, phone_number):
        headers = {
            'authToken': LG_CNS_API_KEY,
            'serverName': LG_CNS_API_ID,
            'paymentType': 'P',
        }

        data = {
            'service': LG_CNS_SERVICE_ID,

            'message': message,
            'mobile': phone_number,

            'template': '10008',
        }

        apiURL = '{shcme}{host}{url}'.format(
            shcme='https://', host=KAKAO_BIZ_HOST_URL, url='/request/kakao.json')

        kakaoResponse = requests.post(
            apiURL, data=json.dumps(data), headers=headers)

        return kakaoResponse
