#Django Library
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#External Library
import json

#Models
from .models_order import Order
from .models_store import Store, Menu

#View Modules
from .module_KakaoForm import Kakao_SimpleForm, Kakao_CarouselForm

from .views_system import EatplusSkillLog, errorView

@csrf_exempt
def userHome(request):
    EatplusSkillLog("Home")

    HOME_QUICKREPLIES_MAP = [
        {'action': "message", 'label': "주문 하기",    'messageText': "주문시간 선택", 'blockid': "none", 'extra': { 'Status': "OK" }},
        {'action': "message", 'label': "식권 보기",    'messageText': "식권 보기", 'blockid': "none", 'extra': { 'Status': "OK" }},
        {'action': "message", 'label': "주문 내역",    'messageText': "주문 내역", 'blockid': "none", 'extra': { 'Status': "OK" }},
        {'action': "message", 'label': "위치 변경",    'messageText': "위치 변경", 'blockid': "none", 'extra': { 'Status': "OK" }},
    ]

    try:
        KakaoForm = Kakao_SimpleForm()
        KakaoForm.SimpleForm_Init()

        KakaoForm.SimpleText_Add("잇플 홈 화면입니다! 아래 명령어 중에 골라주세요!")


        for entryPoint in HOME_QUICKREPLIES_MAP:
            KakaoForm.QuickReplies_Add(entryPoint['action'], entryPoint['label'], entryPoint['messageText'], entryPoint['blockid'], entryPoint['extra'])

        return JsonResponse(KakaoForm.GetForm())

    except (RuntimeError, TypeError, NameError, KeyError) as ex:
        return errorView("{}".format(ex))


