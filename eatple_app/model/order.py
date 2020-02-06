# Define
from eatple_app.define import *

from eatple_app.views_slack.slack_logger import SlackLogPayOrder, SlackLogCancelOrder
# Django Library
from django.urls import reverse
from django.db import models
from django.db.models import Q
from django_mysql.models import Model

def iamportOrderValidation(order):
    iamport = Iamport(imp_key=IAMPORT_API_KEY,
                      imp_secret=IAMPORT_API_SECRET_KEY)
    try:
        response = iamport.find(merchant_uid=order.order_id)
    except KeyError:
        return order
    
    except Iamport.ResponseError as e:
        order.payment_status = IAMPORT_ORDER_STATUS_FAILED
        order.save()
        print(e.code)
        print(e.message)
        
        return order
    
    except Iamport.HttpError as http_error:
        print(http_error.code)
        print(http_error.reason)

        if(order.payment_status != IAMPORT_ORDER_STATUS_FAILED):
            order.payment_status = IAMPORT_ORDER_STATUS_NOT_PUSHED            
            order.save()
        
        return order

    
    print(response['status'])
    order.payment_status = response['status']
    order.save()
    
    return order    

def iamportOrderCancel(order, description='주문취소'):
    iamport = Iamport(imp_key=IAMPORT_API_KEY, imp_secret=IAMPORT_API_SECRET_KEY)

    try:
        response = iamport.cancel(description, merchant_uid=order.order_id)    
    except (KeyError, Iamport.ResponseError):
        return False
            
    except Iamport.HttpError as http_error:
        return False
    
    return True

#@PROMOTION 
def promotionOrderUpdate(order):
    paymentDate = dateByTimeZone(order.payment_date)
    paymentDateWithoutTime = paymentDate.replace(
        hour=0, minute=0, second=0, microsecond=0)

    currentDate = dateNowByTimeZone()
    currentDateWithoutTime = currentDate.replace(
        hour=0, minute=0, second=0, microsecond=0)
    
    promotion_month = 12
    promotion_day = int(order.menu.name[0:2])

    PROMOTION_DAY = currentDate.replace(month=promotion_month, day=promotion_day, hour=0, minute=0, second=0, microsecond=0)
    TOMORROW  = PROMOTION_DAY + datetime.timedelta(days=1)
    YESTERDAY = PROMOTION_DAY + datetime.timedelta(days=-1)  # Yesterday start

    # Order Edit Time 16:30 ~ 10:25(~ 10:30)
    OrderEditTimeStart = PROMOTION_DAY + datetime.timedelta(days=-14)
    OrderEditTimeEnd = PROMOTION_DAY + datetime.timedelta(hours=17, minutes=55, days=-1)
    OrderTimeEnd = PROMOTION_DAY + datetime.timedelta(hours=18, minutes=0, days=-1)

    # Pickup Time (10:30 ~)11:00 ~ 16:00
    PickupTimeStart = PROMOTION_DAY + datetime.timedelta(hours=11, minutes=0)
    PickupTimeEnd = TOMORROW
        
    # Lunch Order
    if((currentDate <= TOMORROW)):
        # Order Lunch
        if(OrderTimeEnd <= currentDate) and (currentDate < PickupTimeStart):
            order.status = ORDER_STATUS_PICKUP_PREPARE
            order.save()
            
        elif(PickupTimeStart <= currentDate) and (currentDate < PickupTimeEnd):
            if(currentDate >= order.pickup_time + datetime.timedelta(minutes=-15)):
                order.status = ORDER_STATUS_PICKUP_WAIT
                order.save()
            else:
                order.status = ORDER_STATUS_PICKUP_PREPARE
                order.save()
        # Order Prepare
        else:
            if(OrderEditTimeStart <= currentDate) and (currentDate < OrderTimeEnd):
                if currentDate <= OrderEditTimeEnd:
                    order.status = ORDER_STATUS_ORDER_CONFIRMED
                    order.save()
                else:
                    order.status = ORDER_STATUS_PICKUP_PREPARE
                    order.save()

            # Invalid Time Range is Dinner Order Time ( prev phase lunch order ~ dinner order ~ next phase lunch order )
            else:
                order.status = ORDER_STATUS_ORDER_EXPIRED
                order.save()

    # Promotion Expire 
    else:
        order.status = ORDER_STATUS_ORDER_EXPIRED
        order.save()

    return order
  
def orderUpdate(order):                 
    # B2B User Pass
    if(order.ordersheet.user.type == USER_TYPE_B2B and 
       order.ordersheet.user.company != None and
       order.ordersheet.user.company.status != OC_CLOSE
       ):
        order.payment_status = order.payment_status
        order.save()
        
    #Normal User Pass
    else:
        if(order.menu == None or order.store == None):
            order.payment_status = IAMPORT_ORDER_STATUS_NOT_PUSHED
            order.save()
        else:
            order = iamportOrderValidation(order)
            
    #Payment State Update
    if(order.payment_status == IAMPORT_ORDER_STATUS_CANCELLED):
        #@PROMOTION
        if(order.type == ORDER_TYPE_PROMOTION):
            order.ordersheet.user.cancelPromotion()
            
        order.status = ORDER_STATUS_ORDER_CANCELED
        order.save()
        print('주문 취소됨')

    if(order.payment_status == IAMPORT_ORDER_STATUS_READY):
        print('주문 미결제 또는 진행중')
        
    if(order.payment_status == IAMPORT_ORDER_STATUS_FAILED):
        order.status = ORDER_STATUS_ORDER_FAILED
        order.save()
        print('주문 실패')
        
    if(order.payment_status == IAMPORT_ORDER_STATUS_NOT_PUSHED):
        order.status = ORDER_STATUS_MENU_CHOCIED
        order.save()
        print('메뉴 선택중')
        
    if(order.payment_status == IAMPORT_ORDER_STATUS_PAID):
        if(order.status == ORDER_STATUS_MENU_CHOCIED):
            order.status = ORDER_STATUS_ORDER_CONFIRM_WAIT
            order.save()
            
            #@SLACK LOGGER
            SlackLogPayOrder(order)
            
        #@PROMOTION
        if(order.type == ORDER_TYPE_PROMOTION):
            order.ordersheet.user.applyPromotion()

        print('주문 결제됨')
        
    if(order.payment_status != IAMPORT_ORDER_STATUS_PAID):
        return order

    if(order.status == ORDER_STATUS_PICKUP_COMPLETED or order.status == ORDER_STATUS_ORDER_EXPIRED):
        return order
        
    #@PROMOTION
    if(order.type == ORDER_TYPE_PROMOTION):
        return promotionOrderUpdate(order)
    
    #Ordering State Update    
    menu = order.menu

    paymentDate = dateByTimeZone(order.payment_date)
    paymentDateWithoutTime = paymentDate.replace(
        hour=0, minute=0, second=0, microsecond=0)

    currentDate = dateNowByTimeZone()
    currentDateWithoutTime = currentDate.replace(
        hour=0, minute=0, second=0, microsecond=0)
    
    YESTERDAY = currentDateWithoutTime + \
        datetime.timedelta(days=-1)  # Yesterday start
    TODAY = currentDateWithoutTime
    TOMORROW = currentDateWithoutTime + \
        datetime.timedelta(days=1)  # Tommorrow start

    PICKUP_DAY = dateByTimeZone(order.pickup_time).replace(hour=0, minute=0, second=0, microsecond=0)
    PICKUP_YESTER_DAY = PICKUP_DAY + datetime.timedelta(days=-1)

    # Prev Lunch Order Edit Time 16:30 ~ 시:25(~ 10:30)
    prevlunchOrderEditTimeStart = currentDateWithoutTime + datetime.timedelta(hours=16, minutes=30, days=-1)
    prevlunchOrderEditTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=10, minutes=25)
    prevlunchOrderTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=10, minutes=30)

    # Dinner Order Edit Time 11:30 ~ 16:25(~ 16:30)
    dinnerOrderEditTimeStart = currentDateWithoutTime + datetime.timedelta(hours=11, minutes=30)
    dinnerOrderEditTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=16, minutes=25)
    dinnerOrderTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=16, minutes=30)

    # Next Lunch Order Edit Time 16:30 ~ 9:30(~ 10:30)
    nextlunchOrderEditTimeStart = currentDateWithoutTime + datetime.timedelta(hours=16, minutes=30)
    nextlunchOrderEditTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=9, minutes=30, days=1)
    nextlunchOrderTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=10, minutes=30, days=1)

    # Lunch Order Pickup Time (10:30 ~)11:30 ~ 14:00
    lunchOrderPickupTimeStart = currentDateWithoutTime + datetime.timedelta(hours=11, minutes=30)
    lunchOrderPickupTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=14, minutes=00)

    # Dinner Order Pickup Time (16:30 ~)17:30 ~ 21:00
    dinnerOrderPickupTimeStart = currentDateWithoutTime + datetime.timedelta(hours=17, minutes=30)
    dinnerOrderPickupTimeEnd = currentDateWithoutTime + datetime.timedelta(hours=21, minutes=0)
    
    # Lunch Order
    if (SELLING_TIME_LUNCH == menu.selling_time) and \
        ((PICKUP_YESTER_DAY <= paymentDateWithoutTime) and (TODAY <= PICKUP_DAY)):
        # Pickup Prepare Time 10:30  ~ 11:30
        if(prevlunchOrderTimeEnd <= currentDate) and (currentDate <= lunchOrderPickupTimeStart) and \
           (TODAY == PICKUP_DAY):
            print("픽업 대기중 - A")
            order.status = ORDER_STATUS_PICKUP_PREPARE
            order.save()
        # PickupTime Waiting Time 11:31 ~ 13:59
        elif(lunchOrderPickupTimeStart < currentDate) and (currentDate <= lunchOrderPickupTimeEnd) and \
            (TODAY == PICKUP_DAY):
            # Over Order Pickup Time
            if(currentDate >= order.pickup_time + datetime.timedelta(minutes=-15)):
                print("픽업 대기중 - B")
                order.status = ORDER_STATUS_PICKUP_WAIT
                order.save()
            else:
                print("픽업 준비중 - A")
                order.status = ORDER_STATUS_PICKUP_PREPARE
                order.save()
        # Order Time Range
        else:      
            print(nextlunchOrderEditTimeStart)
            print(nextlunchOrderEditTimeEnd)
            print(currentDate)
            print(paymentDate)

            # prev phase Order YD 16:30 ~ TD 10:30
            if(prevlunchOrderEditTimeStart <= currentDate) and (currentDate <= prevlunchOrderTimeEnd):
                if currentDate <= prevlunchOrderEditTimeEnd:
                    print("주문 완료 - A")
                    order.status = ORDER_STATUS_ORDER_CONFIRMED
                    order.save()
                else:
                    print("픽업 준비중 - B")
                    order.status = ORDER_STATUS_PICKUP_PREPARE
                    order.save()

            # next phase Lunch order
            elif ((nextlunchOrderEditTimeStart + datetime.timedelta(minutes=-5)) <= currentDate) and \
                 (currentDate <= nextlunchOrderEditTimeEnd) and \
                 (paymentDate >= (nextlunchOrderEditTimeStart + datetime.timedelta(minutes=-5)):
                print("주문 완료 - B")
                order.status = ORDER_STATUS_ORDER_CONFIRMED
                order.save()

            # Invalid Time Range is Dinner Order Time ( prev phase lunch order ~ dinner order ~ next phase lunch order )
            else:
                print("픽업 완료 - A")
                order.status = ORDER_STATUS_PICKUP_COMPLETED
                order.save()

    # Dinner Order
    elif (SELLING_TIME_DINNER == menu.selling_time) and (paymentDateWithoutTime == TODAY):
        # Meal Pre-
        if(dinnerOrderTimeEnd <= currentDate) and (currentDate <= dinnerOrderPickupTimeStart):
            print("픽업 준비중 - A")
            order.status = ORDER_STATUS_PICKUP_PREPARE
            order.save()
        # PickupTime Range
        elif(dinnerOrderPickupTimeStart <= currentDate) and (currentDate <= dinnerOrderPickupTimeEnd):
            # Over Order Pickup Time
            if(currentDate >= orderPickupTime):
                print("픽업 대기중 - A")
                order.status = ORDER_STATUS_PICKUP_WAIT
                order.save()
            else:
                print("픽업 준비중 - A")
                order.status = ORDER_STATUS_PICKUP_PREPARE
                order.save()
        else:
            # Today Order
            if(dinnerOrderEditTimeStart < currentDate) and (currentDate < dinnerOrderTimeEnd):

                if paymentDate <= dinnerOrderEditTimeEnd:
                    print("주문 완료 - A")
                    order.status = ORDER_STATUS_ORDER_CONFIRMED
                    order.save()

                else:
                    print("픽업 준비중 - B")
                    order.status = ORDER_STATUS_PICKUP_PREPARE
                    order.save()
            # Invalid Time Range is Lunch Order Time ( prev phase lunch order ~ dinner order ~ next phase lunch order )
            else:
                print("픽업 완료 - A")
                order.status = ORDER_STATUS_PICKUP_COMPLETED
                order.save()

    # Invalid Order Selling Time
    else:
        print("주문 만료 - A")
        order.status = ORDER_STATUS_ORDER_EXPIRED
        order.save()

    return order

class Order(models.Model):
    class Meta:
        verbose_name = "주문 내역"
        verbose_name_plural = "주문 내역"
        
        ordering = ['-order_date']

    order_id = models.CharField(
        max_length=MANAGEMENT_CODE_LENGTH,
        blank=True,
        null=True,
        verbose_name="주문 번호"
    )

    ordersheet = models.ForeignKey(
        'OrderSheet',
        on_delete=models.CASCADE,
        null=True,
        verbose_name="주문시트 번호"
    )

    store = models.ForeignKey(
        'Store',
        on_delete=models.CASCADE,
        null=True,
        verbose_name="상점"
    )

    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        null=True,
        verbose_name="메뉴"
    )

    totalPrice = models.IntegerField(
        default=0,
        verbose_name="총 금액"
    )

    count = models.IntegerField(
        default=1,
        verbose_name="주문 개수"    
    )

    pickup_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="픽업 시간"
    )

    payment_status = models.CharField(
        max_length=10,
        choices=IAMPORT_ORDER_STATUS,
        default=IAMPORT_ORDER_STATUS_NOT_PUSHED,
        verbose_name="결제 상태"
    )

    status = models.IntegerField(
        choices=ORDER_STATUS,
        default=ORDER_STATUS_MENU_CHOCIED,
        verbose_name="주문 상태"
    )

    type = models.CharField(
        max_length=WORD_LENGTH, 
        default=ORDER_TYPE_NORMAL,
        choices=ORDER_TYPE,
        verbose_name="주문 타입" 
    )
    
    delegate = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="위임자" 
    )
    
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name="마지막 수정일"    
    )
    
    order_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="주문 시간"
    )
    payment_date  = models.DateTimeField(
        default=timezone.now,
        verbose_name="결제 완료 시간"
    )

    def save(self, *args, **kwargs):
        super().save()

    @staticmethod
    def pickupTimeToDateTime(pickup_time):
        pickup_time = [x.strip() for x in pickup_time.split(':')]

        currentTime = dateNowByTimeZone()
        datetime_pickup_time = currentTime.replace(
                                    hour=int(pickup_time[0]), 
                                    minute=int(pickup_time[1]),
                                    second=0,
                                    microsecond=0
                                    )

        if(datetime_pickup_time < currentTime):
            datetime_pickup_time += datetime.timedelta(days=1)
        
        return datetime_pickup_time

    def orderStatusUpdate(self):
        return orderUpdate(self)

    def orderCancel(self):
        
        #@SLACK LOGGER
        SlackLogCancelOrder(self)

        # B2B User Pass
        if(self.ordersheet.user.type == USER_TYPE_B2B and 
           self.ordersheet.user.company != None and
           self.ordersheet.user.company.status != OC_CLOSE):
            self.payment_status = IAMPORT_ORDER_STATUS_CANCELLED
            self.save()
            return True
        else:
            return iamportOrderCancel(self)

    def orderUsed(self):
        self.status = ORDER_STATUS_PICKUP_COMPLETED
        self.save()
        
        return self
    
    def orderDelegate(self, order):
        if(self.delegate != None):
            return None
        
        if(self.menu == order.menu and
           self.store == order.store and
           self.pickup_time == order.pickup_time):
            
           self.delegate = order.ordersheet.user
           self.save()
           
        return self
    
    def orderDelegateCancel(self):
        self.delegate = None
        self.save()
        
        return self
    
    # Methods
    def __str__(self):
        return '{}'.format(self.order_id)
    
class OrderManager():
    def __init__(self, user):
        self.orderList = Order.objects.all()

    def availableOrderStatusUpdate(self):
        availableOrders = self.getAvailableOrders()

        # Order Status Update   
        for order in availableOrders:
            orderUpdate(order)

        return self.getAvailableOrders()

    def orderPenddingCleanUp(self):
        currentDate = dateNowByTimeZone()
        expireDate = currentDate + datetime.timedelta(hours=-24)

        readyPayOrders = Order.objects.filter(
            Q(payment_status=IAMPORT_ORDER_STATUS_NOT_PUSHED) &
            Q(payment_date__gte=expireDate) &
            ~Q(store=None) &
            ~Q(menu=None)
        ).order_by('order_date')
    
        # Order Status Update
        for order in readyPayOrders:
            orderUpdate(order)
            if(order.payment_status != IAMPORT_ORDER_STATUS_PAID):
                order.payment_status = IAMPORT_ORDER_STATUS_FAILED
                order.status = ORDER_STATUS_MENU_CHOCIED
                order.save()

    def orderPaidCheck(self):
        currentDate = dateNowByTimeZone()
        expireDate = currentDate + datetime.timedelta(hours=-24)
        
        readyPayOrders = Order.objects.filter(
            Q(payment_status=IAMPORT_ORDER_STATUS_NOT_PUSHED) &
            Q(payment_date__gte=expireDate) &
            ~Q(store=None) &
            ~Q(menu=None)
        ).order_by('order_date')
    
        # Order Status Update
        for order in readyPayOrders:
            orderUpdate(order)

    def getUnavailableOrders(self):
        unavailableOrders = self.orderList.filter(
            Q(status=ORDER_STATUS_ORDER_EXPIRED) |
            Q(status=ORDER_STATUS_ORDER_CANCELED) |
            Q(status=ORDER_STATUS_PAYMENT_CHECK) |
            Q(status=ORDER_STATUS_PICKUP_COMPLETED)
        )

        return unavailableOrders

    def getAvailableOrders(self):
        currentDate = dateNowByTimeZone()
        expireDate = currentDate + datetime.timedelta(hours=-24)
        
        availableOrders = self.orderList.filter(
            (
                Q(status=ORDER_STATUS_PICKUP_WAIT) |
                Q(status=ORDER_STATUS_PICKUP_PREPARE) |
                Q(status=ORDER_STATUS_ORDER_CONFIRM_WAIT) |
                Q(status=ORDER_STATUS_ORDER_CONFIRMED)
            ) &
            Q(payment_date__gte=expireDate)
        )

        return availableOrders

    def getAvailableLunchOrderPurchased(self):
        availableOrders = self.getAvailableOrders()
        lunchOrders = availableOrders.filter(
            menu__selling_time=SELLING_TIME_LUNCH
        )

        return lunchOrders

    def getAvailableDinnerOrderPurchased(self):
        availableOrders = self.getAvailableOrders()
        dinnerOrders = availableOrders.filter(
            menu__selling_time=SELLING_TIME_DINNER
        )
        
        return dinnerOrders
    
class UserOrderManager(OrderManager):
    def __init__(self, user):
        self.orderList = Order.objects.filter(
            Q(ordersheet__user=user) |
            Q(delegate=user)
        )
        
class PartnerOrderManager(OrderManager):
    def __init__(self, partner):
        self.orderList = Order.objects.filter(store=partner.store)

class OrderSheet(models.Model):
    class Meta:
        verbose_name = "주문 내역 시트"
        verbose_name_plural = "주문 내역 시트"
        
        ordering = ['-create_date']

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=True,
        verbose_name="소유자" 
    )

    management_code = models.CharField(
        max_length=MANAGEMENT_CODE_LENGTH,
        blank=True,
        null=True,
        verbose_name="주문시트 관리번호" 
    )

    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name="마지막 수정일" 
    )
    create_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="생성일자" 
    )

    def __init__(self, *args, **kwargs):
        super(OrderSheet, self).__init__(*args, **kwargs)

        if (self.id == None):
            try:
                self.id = OrderSheet.objects.latest('id').id + 1
            except (OrderSheet.DoesNotExist) as ex:
                self.id = 1

        if(self.create_date == None):
            self.create_date = datetime.datetime.now()

        self.management_code = 'E{area:06X}P{id:03X}'.format(
            area=int(self.create_date.strftime('%f')), id=self.id)

    def save(self, *args, **kwargs):
        super().save()

    def pushOrder(self, user, store, menu, pickup_time, totalPrice, count, type):
        self.user = user
        super().save()

        try:
            order_id = Order.objects.latest('id').id + 1
        except (Order.DoesNotExist) as ex:
            order_id = 1

        order_id = 'EP{area:08X}{id:04X}'.format(
            area=int(datetime.datetime.now().strftime('%f')), id=self.id)
        
        order = Order()
        order.ordersheet = self
        order.order_id = order_id
        order.menu = menu
        order.store = store
        
        order.pickup_time = order.pickupTimeToDateTime(pickup_time)
        
        order.totalPrice = totalPrice
        order.count = count
        order.type = type
        order.save()

        return order

    # Methods
    def __str__(self):
        return '{}'.format(self.management_code)
