from rest_framework import serializers
from rest_framework.authtoken.models import Token
from ecommerce.models import Product, Order, OrderDetail
from django.contrib.auth.models import User


class UserSerialiazers(serializers.ModelSerializer):
       
    class Meta:

        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        
        return user

class ProductSerializers(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = ('id', 'name', 'price', 'stock')

class OrderDetailFullSerializers(serializers.ModelSerializer):

    class Meta:

        model = OrderDetail
        fields = ('id','cuantity', 'order', 'product')

class OrderDetailSerializers(serializers.ModelSerializer):

    class Meta:

        model = OrderDetail
        fields = ('id','cuantity', 'product')

class OrderFullSerializers(serializers.ModelSerializer):

    order_detail = OrderDetailSerializers(many=True)

    class Meta:

        model = Order
        fields = ('id', 'date_time', 'get_total', 'get_total_usd', 'order_detail')

class OrderSerializers(serializers.ModelSerializer):

    class Meta:

        model = Order
        fields = ('id', 'date_time', 'get_total', 'get_total_usd',)


class OrderDateSerializers(serializers.Serializer):

    date_time = serializers.DateTimeField(required = True)

