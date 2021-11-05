from ecommerce.models import Product, Order
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiazers

    def list(self, request, *args, **kwargs):

        response = {'massege': 'Not available'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):

        response = {'massege': 'Not available'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ProductViewset(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def update(self, request, *args, **kwargs):

        if 'only_stock' in request.data:

            try:
                cantidad = int(request.data.dict()[f'only_stock'])

            except:

                response = {'massege': 'Cuantity must be a number'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            instance = self.get_object()
            instance.stock = cantidad

            response = {'massege': 'Stock changed success!'}
            return Response(response, status=status.HTTP_200_OK)

        else:
            viewsets.ModelViewSet.update(self, request, *args, **kwargs)

class OrderDetailViewset(viewsets.ModelViewSet):

    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailFullSerializers

    def create(self, request, *args, **kwargs):

        response = {'massege': 'Not available'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        product = Product.objects.get(id = instance.product.id)
        product.stock += instance.cuantity
        product.save()

        instance.delete()

        response = {'massege': 'Success!, stock restored'}
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        product = Product.objects.get(id = instance.product.id)

        try:
            cantidad_verificar = int(request.data.dict()['cuantity'])

        except:

            response = {'massege': 'Cuantity must be a number'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if cantidad_verificar > (instance.cuantity + product.stock):

            response = {'massege': f'Insufficient stock for {product.name}'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:

            instance.cuantity = int(request.data.dict()['cuantity'])
            instance.save()

            response = {'massege': 'Updates success!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class OrderViewset(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    @action(detail=True, methods=["GET"])
    def detail_info(self, request, pk):

        order = Order.objects.get(id = pk)
        serializer = OrderFullSerializers(order, many=False)

        response = {'Detail': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        orders_details = OrderDetail.objects.filter(order = instance)

        for order_detail in orders_details:
            product = Product.objects.get(id = order_detail.product.id)
            product.stock += order_detail.cuantity
            product.save()

        instance.delete()

        response = {'massege': 'Success!, stock restored'}
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        serializer_order = OrderDateSerializers(data=request.data)

        if serializer_order.is_valid():

            if 'product' in request.data and 'cuantity' in request.data:

                ## -> Vamos a chequear toda la combinación de product - cuantity. Aqui supongo que el Front me mandara cada registro con un numero que me indique la posición

                product_list = []
                product_to_update = []

                for key_name in request.data.dict().keys():
                    
                    if 'product' in key_name:

                        ## -> Verificación de valor

                        if len(key_name.split("_")) > 1:

                            producto_verificar = request.data.dict()[f'product_{key_name.split("_")[1]}']
                            
                            try:
                                cantidad_verificar = int(request.data.dict()[f'cuantity_{key_name.split("_")[1]}'])

                            except:

                                response = {'massege': 'Cuantity must be a number'}
                                return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        else:

                            producto_verificar = request.data.dict()['product']

                            try:
                                cantidad_verificar = int(request.data.dict()['cuantity'])

                            except:

                                response = {'massege': 'Cuantity must be a number'}
                                return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        ## -> Verificación de exitencia

                        try:

                            producto = Product.objects.get(id = producto_verificar)

                        except:

                            response = {'massege': f'Not match for product ID {producto_verificar}'}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                         ## -> Verificación de minimo

                        if cantidad_verificar == 0:

                            response = {'massege': f'Not cuantity for {producto.name}'}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        ## -> Verificación de cantidad

                        if cantidad_verificar > producto.stock:

                            response = {'massege': f'Insufficient stock for {producto.name}'}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        ## -> Verificación de no duplicado

                        if producto_verificar in product_list:

                            response = {'massege': f'Duplicate product: {producto_verificar}'}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        else:

                            product_list.append(producto_verificar)

                        ## -> Superado este punto, podemos crear la orden, por lo cual almacenare la conbinación producto-cantidad

                        product_to_update.append((producto.id, cantidad_verificar))

                new_order = Order.objects.create(date_time = serializer_order.data.get("date_time"))

                for order_detail in product_to_update:
                    
                    product = Product.objects.get(id = order_detail[0])
                    new_order_detail = OrderDetail.objects.create(order = new_order, product = product, cuantity = order_detail[1])
                    
                    product.stock -= new_order_detail.cuantity
                    product.save()

                serializer_order_detail = OrderFullSerializers(new_order, many=False)
                response = {'massege': 'Order created success!', 'result': serializer_order_detail.data}
                return Response(response, status=status.HTTP_201_CREATED)


