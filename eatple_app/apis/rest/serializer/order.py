from rest_framework import serializers
from eatple_app.models import Order
from eatple_app.system.model_type import *


class OrderSerializer(serializers.ModelSerializer):
    menu = serializers.CharField(max_length=200)
    store = serializers.CharField(max_length=200)
    totalPrice = serializers.SerializerMethodField()
    payment_date = serializers.DateTimeField(
        format="%Y년 %m월 %d일 %H시%M분%S초", required=False, read_only=True)
    payment_type = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    user = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    
    def get_payment_type(self, obj):
        return dict(ORDER_PAYMENT_TYPE)[obj.payment_type]

    def get_payment_status(self, obj):
        return dict(EATPLE_ORDER_STATUS)[obj.payment_status]

    def get_totalPrice(self, obj):
        return '{}원'.format(format(obj.totalPrice, ","))
    
    def get_user(self, obj):
        return obj.ordersheet.user.nickname
        
    def get_phone_number(self, obj):
        return obj.ordersheet.user.phone_number.as_national
        
    class Meta:
        model = Order
        exclude = ()
