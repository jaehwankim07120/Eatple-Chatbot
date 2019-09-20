#Django Library
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#External Library
import json
import sys

#Models
from .models_config import Config


from .models_order import Order
from .models_store import Store, Menu

#View Modules
from .module_KakaoForm import Kakao_SimpleForm, Kakao_CarouselForm

#GLOBAL CONFIG
KAKAO_PARAM_STATUS          = Config.KAKAO_PARAM_STATUS
KAKAO_PARAM_STATUS_OK       = Config.KAKAO_PARAM_STATUS_OK
KAKAO_PARAM_STATUS_NOT_OK   = Config.KAKAO_PARAM_STATUS_NOT_OK


# SKill Log
def EatplusSkillLog(flow="some flow"):
    print("- - - - - - - - - - - - - - - - - - - - - - - - -")
    print("- [ {} ]".format(flow))
    print("-  func() => {}   ".format(sys._getframe(1).f_code.co_name + "()"))
    print("- - - - - - - - - - - - - - - - - - - - - - - - -")

# Error View
def errorView(error_log="error message"):
    print("- - - - - - - - - - - - - - - - - - - - - - - - -")
    print("- [ ERROR! ]")
    print("-  func() => {}   ".format(sys._getframe(1).f_code.co_name + "()"))
    print("-  error  => {}   ".format(error_log))
    print("- - - - - - - - - - - - - - - - - - - - - - - - -")
    
    KakaoForm = Kakao_SimpleForm()
    KakaoForm.SimpleForm_Init()

    ERROR_QUICKREPLIES_MAP = [
        {'action': "message", 'label': "홈으로 돌아가기",    'messageText': "홈으로 돌아가기", 'blockid': "none", 'extra': { KAKAO_PARAM_STATUS: KAKAO_PARAM_STATUS_OK }},
    ]

    for entryPoint in ERROR_QUICKREPLIES_MAP:
        KakaoForm.QuickReplies_Add(entryPoint['action'], entryPoint['label'], entryPoint['messageText'], entryPoint['blockid'], entryPoint['extra'])

    KakaoForm.SimpleText_Add("진행하는 도중 문제가생겼어요ㅠㅜ")

    return JsonResponse(KakaoForm.GetForm())