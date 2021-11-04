import requests
import numpy as np
from enum import unique
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import AutoField

# Create your models here.

class Product(models.Model):

    id = models.CharField(max_length=30, verbose_name="Product ID", unique=True, primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Product Name")
    price = models.FloatField(validators=[MinValueValidator(0.0)], verbose_name="Product Price")
    stock = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Product Stock")

    class Meta:

        verbose_name = "Product"
        verbose_name_plural = "Products"
        unique_together = (('name', 'price'),)

    def __str__(self):

        return f'{self.id}: {self.name}'

class Order(models.Model):

    id = models.AutoField(primary_key = True,  verbose_name="Order ID")
    date_time = models.DateTimeField(verbose_name="Order date time")

    class Meta:

        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_total(self):

        orders_detailes = OrderDetail.objects.filter(order = self)
        total = sum(np.array(orders_detailes.values_list("cuantity", flat = True))*np.array(orders_detailes.values_list("product__price", flat = True)))
        
        return round(total, 2)

    def get_total_usd(self):

        url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"

        request = requests.get(url)

        for request_dic in request.json():

            if request_dic['casa']['nombre'] == "Dolar Blue":
                
                valor_usd_blue = request_dic['casa']['venta']

                break

        total_usd = round(self.get_total()/float(str(valor_usd_blue).replace(",", ".")), 2)

        return total_usd


    def __str__(self):

        return f'Order nº: {self.id}'

class OrderDetail(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order", related_name="order_detail")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    cuantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Product quantity")

    class Meta:

        verbose_name = "Order detail"
        verbose_name_plural = "Order details"
        unique_together = (('order', 'product'),)

    def __str__(self):

        return f'{self.order.id}: {self.product.name}'
