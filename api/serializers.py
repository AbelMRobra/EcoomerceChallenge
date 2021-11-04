from rest_framework import serializers
from ecommerce.models import Product, Order, OrderDetail

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

