#Django Library
from django.conf import settings

#External Library
from datetime import datetime, timedelta
import pytz

class Config():
    #SYSTEM
    USE_TZ               = settings.USE_TZ
    TIME_ZONE            = settings.TIME_ZONE

    NOT_APPLICABLE       = "N/A"
    DEFAULT_OBJECT_ID    = 1
    DEFAULT_USER_ID      = 2

    #USER LENGTH
    USER_NICKNAME_LENGTH = 18
    USER_ID_LENGTH       = 18
    USER_SERIAL_LENGTH   = 12

    #STRING LENGTH
    STRING_LENGTH        = 255
    WORD_LENGTH          = 32

    #MENU
    MANAGEMENT_CODE_DEFAULT    = "ABCDEF123456"
    MANAGEMENT_CODE_LENGTH     = 12

    SELLING_TIME_LUNCH         = 0
    SELLING_TIME_DINNER        = 1
    SELLING_TIME_CATEGORY_DICT = {'점심': SELLING_TIME_LUNCH, '저녁': SELLING_TIME_DINNER}
    SELLING_TIME_CATEGORY      = [
        ('점심', '점심'),
        ('저녁', '저녁'),
    ]

    #ORDERING
    ORDER_STATUS_DICT = {'주문 확인중': 0, '주문 완료': 1, '픽업 준비중': 2, '픽업 가능': 3, '픽업 완료': 4, '주문 만료': 5, '주문 취소': 6}
    ORDER_STATUS = [
        ('주문 확인중',  '주문 확인중'),
        ('주문 완료',   '주문 완료'),
        ('픽업 준비중',  '픽업 준비중'),
        ('픽업 가능',   '픽업 가능'),
        ('픽업 완료',   '픽업 완료'),
        ('주문 만료',   '주문 만료'),
        ('주문 취소',   '주문 취소'),
    ]

    #Kakao Param Data
    KAKAO_PARAM_ORDER_ID          = 'orderID'
    KAKAO_PARAM_USER_ID           = 'userID'
    KAKAO_PARAM_STORE_ID          = 'storeID'
    KAKAO_PARAM_MENU_ID           = 'menuID' 

    KAKAO_PARAM_MENU_CATEGORY     = 'menuCategory'
    KAKAO_PARAM_SELLING_TIME      = 'sellingTime'
    KAKAO_PARAM_PICKUP_TIME       = 'pickupTime'

    KAKAO_PARAM_STATUS            = 'status'
    KAKAO_PARAM_STATUS_OK         = True
    KAKAO_PARAM_STATUS_NOT_OK     = False


def dateNowByTimeZone():
    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    if settings.USE_TZ:
        tz = pytz.timezone(settings.TIME_ZONE)
        return tz.localize(datetime.now())
    else:
        return datetime.now()