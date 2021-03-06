# Models
from eatple_app.models import *

# Define
from eatple_app.define import *

DEFAULT_QUICKREPLIES_MAP = [
    {
        'action': 'block',
        'label': '🏠  홈',
        'messageText': KAKAO_EMOJI_LOADING,
        'blockId': KAKAO_BLOCK_USER_HOME,
        'extra': {}
    },
    {
        'action': 'block',
        'label': '잇플패스 확인하기',
        'messageText': KAKAO_EMOJI_LOADING,
        'blockId': KAKAO_BLOCK_USER_EATPLE_PASS,
        'extra': {}
    },
]


def userLocationValidation(user):
    try:
        try:
            location = Location.objects.get(user=user)
        except AttributeError:
            location = Location.objects.filter(user=user)[:1]

        return location
    except Location.DoesNotExist:
        return None


def isB2BUser(user):
    try:
        B2BUser = UserB2B.objects.get(phone_number=user.phone_number)

        if(user.type != USER_TYPE_B2B or user.company == None or (user.company != Company.objects.get(id=int(B2BUser.company.id)))):
            user.company = Company.objects.get(id=int(B2BUser.company.id))
            user.type = USER_TYPE_B2B
            user.save()

        if(user.company.status != OC_OPEN):
            return False

        return True
    except UserB2B.DoesNotExist:
        user.company = None
        user.type = USER_TYPE_NORMAL
        user.save()
        return False

    return False


def sellingTimeCheck(include=False):
    # DEBUG
    if(VALIDATION_DEBUG_MODE):
        return SELLING_TIME_LUNCH

    orderTimeSheet = OrderTimeSheet()

    currentDate = orderTimeSheet.GetCurrentDate()

    # Prev Lunch Order Time
    prevLunchOrderTimeStart = orderTimeSheet.GetPrevLunchOrderEditTimeStart()
    prevLunchOrderTimeEnd = orderTimeSheet.GetPrevLunchOrderEditTimeEnd()

    # Dinner Order Time
    dinnerOrderTimeStart = orderTimeSheet.GetDinnerOrderEditTimeStart()
    dinnerOrderTimeEnd = orderTimeSheet.GetDinnerOrderTimeEnd()

    # Next Lunch Order Time
    nextLunchOrderTimeStart = orderTimeSheet.GetNextLunchOrderEditTimeStart()
    nextLunchOrderTimeEnd = orderTimeSheet.GetNextLunchOrderEditTimeEnd()

    if(prevLunchOrderTimeEnd <= currentDate) and (currentDate < dinnerOrderTimeStart):
        if(include):
            return SELLING_TIME_DINNER
        else:
            return None

    elif(dinnerOrderTimeEnd <= currentDate) and (currentDate < nextLunchOrderTimeStart):
        if(include):
            return SELLING_TIME_LUNCH
        else:
            return None
    elif(prevLunchOrderTimeStart <= currentDate) and (currentDate < prevLunchOrderTimeEnd):
        return SELLING_TIME_LUNCH
    elif(nextLunchOrderTimeStart <= currentDate) and (currentDate < nextLunchOrderTimeEnd):
        return SELLING_TIME_LUNCH
    elif(dinnerOrderTimeStart <= currentDate) and (currentDate < dinnerOrderTimeEnd):
        return SELLING_TIME_DINNER
    else:
        return None


def weekendTimeCheck(sellingTime):
    orderTimeSheet = OrderTimeSheet()
    currentDate = orderTimeSheet.GetCurrentDate()
    currentDateWithoutTime = orderTimeSheet.GetCurrentDateWithoutTime()

    # DEBUG
    if(VALIDATION_DEBUG_MODE):
        return False

    if(sellingTime == SELLING_TIME_LUNCH):
        closedDateStart = orderTimeSheet.GetPrevLunchOrderTimeEnd()
        closedDateEnd = orderTimeSheet.GetNextLunchOrderEditTimeStart()

        if(currentDate.strftime('%A') == 'Friday'):
            if(currentDate >= closedDateStart):
                return True
            else:
                return False
        elif(currentDate.strftime('%A') == 'Saturday'):
            return True
        elif(currentDate.strftime('%A') == 'Sunday'):
            if(currentDate <= closedDateEnd):
                return True
            else:
                return False
        else:
            return False
    elif(sellingTime == SELLING_TIME_DINNER):
        dinnerTimeStart = orderTimeSheet.GetDinnerOrderEditTimeStart()
        dinnerTimeEnd = orderTimeSheet.GetDinnerOrderTimeEnd()

        if(currentDate.strftime('%A') == 'Friday'):
            if(currentDate >= dinnerTimeEnd):
                return True
            else:
                return False
        elif(currentDate.strftime('%A') == 'Saturday'):
            return True
        elif(currentDate.strftime('%A') == 'Sunday'):
            return True
        else:
            return False
    else:
        return True


def vacationTimeCheck():
    currentDate = dateNowByTimeZone()
    currentDateWithoutTime = currentDate.replace(
        hour=0, minute=0, second=0, microsecond=0)

    vacationMap = [
        {
            'from_month': 4,
            'from_days': 30,
            'to_month': 5,
            'to_days': 1
        },
        {
            'from_month': 5,
            'from_days': 5,
            'to_month': 5,
            'to_days': 5
        },
    ]

    for vacation in vacationMap:
        closedDateStart = currentDate.replace(
            month=vacation['from_month'], day=vacation['from_days'], hour=0, minute=0, second=0, microsecond=0)
        closedDateEnd = currentDate.replace(
            month=vacation['to_month'], day=vacation['to_days'], hour=23, minute=59, second=59, microsecond=0)

        if(closedDateStart <= currentDate and currentDate <= closedDateEnd):
            return True

    return False
