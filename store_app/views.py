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

# Eatplus for Partner 
from .views_partner import partnerHome

# Eatplus for User 
from .views_user import userHome
from .views_user_manual import userManual
from .views_user_ordering import getSellingTime, selectMenu, getPickupTime, orderConfirm, orderPush
from .views_user_orderCheck import getOrderList, getCoupon, confirmUseCoupon
from .views_user_orderChange import useCoupon, orderCancel, orderPickupTimeChange, getOrderPickupTime


### API Functions ###
