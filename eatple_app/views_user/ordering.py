# Django Library
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Models
from eatple_app.models import *

# Define
from eatple_app.define import *

# Modules
from eatple_app.module_kakao.ReponseForm import *
from eatple_app.module_kakao.RequestForm import *
from eatple_app.module_kakao.Validation import *

# View-System
from eatple_app.views_system.debugger import *

# Wordings
from eatple_app.views_user.wording import wordings

from eatple_app.views import *


# STATIC CONFIG
MENU_LIST_LENGTH = 8
CATEGORY_LIST_LENGTH = 5

DEFAULT_QUICKREPLIES_MAP = [
    {
        'action': "message",
        'label': wordings.RETURN_HOME_QUICK_REPLISE,
        'messageText': wordings.RETURN_HOME_QUICK_REPLISE,
        'blockId': "",
        'extra': {}
    },
]

# # # # # # # # # # # # # # # # # # # # # # # # #
#
# Static View
#
# # # # # # # # # # # # # # # # # # # # # # # # #

def sellingTimeCheck():
    nowDate = dateNowByTimeZone()
    nowDateWithoutTime = nowDate.replace(
        hour=0, minute=0, second=0, microsecond=0)

    # Prev Lunch Order Time 16:30 ~ 10:30
    prevlunchOrderTimeStart = nowDateWithoutTime + \
        timedelta(hours=16, minutes=30, days=-1)
    prevlunchOrderTimeEnd = nowDateWithoutTime + \
        timedelta(hours=10, minutes=30)

    # Dinner Order Time 10:30 ~ 16:30
    dinnerOrderTimeStart = nowDateWithoutTime + timedelta(hours=10, minutes=30)
    dinnerOrderTimeEnd = nowDateWithoutTime + timedelta(hours=16, minutes=30)

    # Next Lunch Order Time 16:30 ~ 10:30
    nextlunchOrderTimeStart = nowDateWithoutTime + \
        timedelta(hours=16, minutes=30)
    nextlunchOrderTimeEnd = nowDateWithoutTime + \
        timedelta(hours=10, minutes=30, days=1)

    if(dinnerOrderTimeStart <= nowDate) and (nowDate <= dinnerOrderTimeEnd):
        return SELLING_TIME_DINNER
    elif(prevlunchOrderTimeStart < nowDate) and (nowDate < prevlunchOrderTimeEnd):
        return SELLING_TIME_LUNCH
    elif(nextlunchOrderTimeStart < nowDate) and (nowDate < nextlunchOrderTimeEnd):
        return SELLING_TIME_LUNCH
    else:
        return None


def MenuListup(user, sellingTime):
    QUICKREPLIES_MAP = [
        {
            'action': "block",
            'label': "홈으로 돌아가기",
            'messageText': "로딩중..",
            'blockId': KAKAO_BLOCK_HOME,
            'extra': {}
        },
    ]
    
    MenuList = Menu.objects.filter(sellingTime=sellingTime)[:MENU_LIST_LENGTH]

    if MenuList:
        KakaoForm = Kakao_CarouselForm()
        KakaoForm.BasicCard_Init()

        # Menu Carousel Card Add
        for menu in MenuList:
            try:
                thumbnail = {"imageUrl": "{}{}".format(
                    HOST_URL, menu.imgURL())}
                
                kakaoMapUrl = "https://map.kakao.com/link/map/{},{}".format(
                    menu.store.name, getLatLng(menu.store.addr))
            except () as ex:
                print(ex)

            buttons = [
                {
                    'action': "block",
                    'label': "주문하기",
                    'messageText': "로딩중..",
                    'blockId': KAKAO_BLOCK_SET_PICKUP_TIME,
                    'extra': {
                        KAKAO_PARAM_STORE_ID:         menu.store.store_id,
                        KAKAO_PARAM_MENU_ID:          menu.menu_id,
                    }
                },
                {
                    'action': "webLink", 
                    'label': wordings.SHOW_LOCATION_BTN,
                    "webLinkUrl": kakaoMapUrl
                },
            ]

            KakaoForm.BasicCard_Add("{}".format(menu.name), "{} - {}원".format(
                menu.store.name,
                menu.price
            ), thumbnail, buttons)

        # Quick Replise Add
        for entryPoint in QUICKREPLIES_MAP:
            KakaoForm.QuickReplies_Add(entryPoint['action'], entryPoint['label'],
                                       entryPoint['messageText'], entryPoint['blockId'], entryPoint['extra'])

    else:
        KakaoForm = Kakao_SimpleForm()
        KakaoForm.SimpleForm_Init()

        for entryPoint in QUICKREPLIES_MAP:
            KakaoForm.QuickReplies_Add(
                entryPoint['action'], entryPoint['label'], entryPoint['messageText'], entryPoint['blockId'], entryPoint['extra'])

        KakaoForm.SimpleText_Add("판매중인 {} 메뉴가 없어요ㅠㅜ".format(sellingTime))

    return JsonResponse(KakaoForm.GetForm())


# # # # # # # # # # # # # # # # # # # # # # # # #
#
# External View
#
# # # # # # # # # # # # # # # # # # # # # # # # #

@csrf_exempt
def GET_Menu(request):
    EatplusSkillLog("Get Menu")

    try:
        kakaoPayload = KakaoPayLoad(request)

        # User Validation
        user = userValidation(kakaoPayload)
        if (user == None):
            return GET_UserHome(request)

        # User's Order Validation
        orderStatus = orderValidation(user)
        
        if(orderStatus != None):
            return orderStatus

        currentSellingTime = sellingTimeCheck()

        try:
            orderRecordSheet = OrderRecordSheet.objects.latest('update_date')
        except OrderRecordSheet.DoesNotExist:
            orderRecordSheet = OrderRecordSheet()

        orderRecordSheet.user = user
                    
        if (orderRecordSheet.recordUpdate(ORDER_RECORD_GET_MENU)):
            print("TimeOut")
            newOrderRecordSheet = OrderRecordSheet()
            newOrderRecordSheet.user = user
            newOrderRecordSheet.recordUpdate(ORDER_RECORD_GET_MENU)
        
        if (currentSellingTime == None):
            return errorView("Get Invalid Selling Time", "잘못된 주문 시간입니다.")
        elif currentSellingTime == SELLING_TIME_DINNER:
            """
                @NOTE Dinner Time Close In Alpha 
            """

            # return MenuListup(user, SELLING_TIME_LUNCH)
            return errorView("Get Invalid Selling Time", "오늘 점심은 이미 마감되었어요.\n내일 점심을 기대해주세요.")

        return MenuListup(user, currentSellingTime)

    except (RuntimeError, TypeError, NameError, KeyError, AttributeError, ValueError) as ex:
        return errorView("{}".format(ex))


'''
    @name GET_PickupTime
    @param userID, storeID, menuID, sellingTime 

    @note
    @bug
    @todo
'''
@csrf_exempt
def GET_PickupTime(request):
    EatplusSkillLog("Get PickupTime")
    
    try:
        kakaoPayload = KakaoPayLoad(request)

        # User Validation
        user = userValidation(kakaoPayload)
        if (user == None):
            return GET_UserHome(request)

        # User's Order Validation
        orderStatus = orderValidation(user)
        
        if(orderStatus != None):
            return orderStatus

        currentSellingTime = sellingTimeCheck()
        
        try:
            orderRecordSheet = OrderRecordSheet.objects.latest('update_date')
        except OrderRecordSheet.DoesNotExist:
            orderRecordSheet = OrderRecordSheet()

        orderRecordSheet.user = user
                    
        orderRecordSheet.recordUpdate(ORDER_RECORD_SET_PICKUP_TIEM)         

        KakaoForm = Kakao_SimpleForm()
        KakaoForm.SimpleForm_Init()

        KakaoForm.SimpleText_Add(
            "음식을 가지러 갈 픽업시간을 설정해주세요."
        )

        PICKUP_TIME_QUICKREPLIES_MAP = []

        if currentSellingTime == SELLING_TIME_LUNCH:
            pikcupTime_Start = store.lunch_pickupTime_start
            pikcupTime_End = store.lunch_pickupTime_end
        else:
  
            pikcupTime_Start = store.dinner_pickupTime_start
            pikcupTime_End = store.dinner_pickupTime_end

        for index, pickupTime in ENTRY_PICKUP_TIME_MAP:
            if(pikcupTime_Start <= index) and (index <= pikcupTime_End):
                PICKUP_TIME_QUICKREPLIES_MAP += {'action': "message", 'label': pickupTime, 'messageText': wordings.ORDER_CONFIRM_COMMAND,
                                                 'blockId': "none", 'extra': {**allExtraData, KAKAO_PARAM_PICKUP_TIME: pickupTime}},

        for entryPoint in PICKUP_TIME_QUICKREPLIES_MAP:
            KakaoForm.QuickReplies_Add(entryPoint['action'], entryPoint['label'],
                                       entryPoint['messageText'], entryPoint['blockId'], entryPoint['extra'])

        return JsonResponse(KakaoForm.GetForm())

    except (RuntimeError, TypeError, NameError, KeyError) as ex:
        return errorView("{}".format(ex))


'''
    @name SET_OrderSheet
    @param storeID, menuID, userID, pickupTime

    @note
    @bug
    @todo
'''
@csrf_exempt
def SET_OrderSheet(request):
    try:
        kakaoPayload = KakaoPayLoad(request)

        # Invalied Path Access
        if(kakaoPayload.userID == NOT_APPLICABLE) or (kakaoPayload.storeID == NOT_APPLICABLE) or (kakaoPayload.menuID == NOT_APPLICABLE) or (kakaoPayload.pickupTime == NOT_APPLICABLE):
            return errorView("Parameter Error")
        else:
            try:
                userInstance = User.objects.get(
                    identifier_code=kakaoPayload.userID)
            except User.DoesNotExist:
                return errorView("User ID is Invalid")

            storeInstance = Store.objects.get(id=kakaoPayload.storeID)
            menuInstance = Menu.objects.get(id=kakaoPayload.menuID)

        if(orderValidation(kakaoPayload.userID, kakaoPayload.menuID) == False):
            return errorView("Order Validate Failed!", "정상적인 경로로 주문해주세요!")

        EatplusSkillLog("Order Flow")

        KakaoForm = Kakao_CarouselForm()
        KakaoForm.BasicCard_Init()

        # Menu Carousel Card Add
        thumbnail = {"imageUrl": "{}{}".format(
            HOST_URL, menuInstance.imgURL())}

        kakaoMapUrl = "https://map.kakao.com/link/map/{},{}".format(
            storeInstance.name, getLatLng(storeInstance.addr))
        buttons = [
            # {'action': "webLink", 'label': wordings.ORDER_PUSH_COMMAND,  'messageText': wordings.ORDER_PUSH_COMMAND, 'extra': kakaoPayload.dataActionExtra,

            # "webLinkUrl": "http://eatple.com/payment?storeName={storeName}&menuName={menuName}&menuPrice={menuPrice}".format(storeName=storeInstance.name, menuName=menuInstance.name, menuPrice=menuInstance.price )},
            # "webLinkUrl": "http://localhost:3000/payment?storeName={storeName}&menuName={menuName}&menuPrice={menuPrice}".format(storeName=storeInstance.name, menuName=menuInstance.name, menuPrice=menuInstance.price )},

            {'action': "message", 'label': wordings.ORDER_PUSH_COMMAND,
                'messageText': wordings.ORDER_PUSH_COMMAND, 'extra': kakaoPayload.dataActionExtra}
        ]

        KakaoForm.BasicCard_Add("{}".format(menuInstance.name), "{} - {}원\n - 픽업 시간 [ {} ]".format(
            storeInstance.name,
            menuInstance.price,
            kakaoPayload.pickupTime
        ), thumbnail, buttons)

        GET_PICKUP_TIME_QUICKREPLIES_MAP = [
            {'action': "message", 'label': "{}하기".format(wordings.ORDER_PICKUP_TIME_CHANGE_COMMAND),  'messageText': "{} {}".format(
                kakaoPayload.sellingTime, wordings.GET_PICKUP_TIME_COMMAND), 'blockId': "none", 'extra': kakaoPayload.dataActionExtra},
            {'action': "message", 'label': wordings.RETURN_HOME_QUICK_REPLISE, 'messageText': wordings.RETURN_HOME_QUICK_REPLISE,
                'blockId': "none", 'extra': {}},
        ]

        for entryPoint in GET_PICKUP_TIME_QUICKREPLIES_MAP:
            KakaoForm.QuickReplies_Add(entryPoint['action'], entryPoint['label'],
                                       entryPoint['messageText'], entryPoint['blockId'], entryPoint['extra'])

        return JsonResponse(KakaoForm.GetForm())

    except (RuntimeError, TypeError, NameError, KeyError) as ex:
        return errorView("{}".format(ex))


'''
    @name POST_Order
    @param storeID, menuID, userID, pickupTime

    @note
    @bug
    @todo
'''
@csrf_exempt
def POST_Order(request):
    try:
        kakaoPayload = KakaoPayLoad(request)

        # Invalied Path Access
        if(kakaoPayload.userID == NOT_APPLICABLE) or (kakaoPayload.storeID == NOT_APPLICABLE) or (kakaoPayload.menuID == NOT_APPLICABLE) or (kakaoPayload.pickupTime == NOT_APPLICABLE):
            return errorView("Parameter Invalid")
        else:
            try:
                userInstance = User.objects.get(
                    identifier_code=kakaoPayload.userID)
            except User.DoesNotExist:
                return errorView("User ID is Invalid")

            storeInstance = Store.objects.get(id=kakaoPayload.storeID)
            menuInstance = Menu.objects.get(id=kakaoPayload.menuID)

        if(orderValidation(kakaoPayload.userID, kakaoPayload.menuID) == False):
            return errorView("Order Validate Failed!", "정상적인 경로로 주문해주세요!")

        # Order Validation
        OrderManagerInstance = OrderManager(kakaoPayload.userID)
        if OrderManagerInstance.getAvailableLunchOrderPurchased().exists() and (menuInstance.sellingTime == SELLING_TIME_CATEGORY[SELLING_TIME_LUNCH][0]):
            return errorView("Invalid Access Order")

        elif OrderManagerInstance.getAvailableDinnerOrderPurchased().exists() and (menuInstance.sellingTime == SELLING_TIME_CATEGORY[SELLING_TIME_DINNER][0]):
            return errorView("Invalid Access Order")

        EatplusSkillLog("Order Flow")

        requests.get

        pushedOrder = Order.pushOrder(userInstance=userInstance,
                                      storeInstance=storeInstance,
                                      menuInstance=menuInstance,
                                      pickupTime=kakaoPayload.pickupTime)

        KakaoForm = Kakao_CarouselForm()
        KakaoForm.BasicCard_Init()

        thumbnail = {"imageUrl": ""}

        kakaoMapUrl = "https://map.kakao.com/link/map/{},{}".format(
            storeInstance.name, getLatLng(storeInstance.addr))

        buttons = [
            {'action': "webLink", 'label': wordings.SHOW_LOCATION_BTN,
                "webLinkUrl": kakaoMapUrl},
            {'action': "message", 'label': wordings.ORDER_CANCEL_COMMAND,  'messageText': wordings.ORDER_CANCEL_COMMAND,
             'extra': {KAKAO_PARAM_ORDER_ID: pushedOrder.id}}
        ]

        KakaoForm.BasicCard_Add(
            "잇플패스가 발급되었습니다.",
            "주문번호: {}\n--------------------\n - 주문자: {}\n\n - 매장: {} \n - 메뉴: {}\n\n - 제 금액: {}원\n\n - 픽업 시간: {}\n--------------------\n - 매장 위치: {}".format(
                pushedOrder.management_code,
                pushedOrder.userInstance.name,
                pushedOrder.storeInstance.name,
                pushedOrder.menuInstance.name,
                pushedOrder.menuInstance.price,
                pushedOrder.pickupTime.astimezone().strftime('%H시%M분 %m월%d일'),
                pushedOrder.storeInstance.addr
            ),
            thumbnail, buttons
        )

        for entryPoint in DEFAULT_QUICKREPLIES_MAP:
            KakaoForm.QuickReplies_Add(entryPoint['action'], entryPoint['label'],
                                       entryPoint['messageText'], entryPoint['blockId'], entryPoint['extra'])

        return JsonResponse(KakaoForm.GetForm())

    except (RuntimeError, TypeError, NameError, KeyError) as ex:
        return errorView("{}".format(ex))
