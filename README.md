# EcomerceChallenge
Challenge de ClichOH

## Instalar

* djangorestframework
* numpy
* requests

## Endpoints diseñados

### SOLICITAR UN TOKEN

http://.../api/auth/

### PRODUCTS

Listar todos los productos -> Method 'GET'
http://.../api/products/

Consultar un producto -> Method 'GET'
http://.../api/products/{id_product}/

Registrar/Editar un producto -> Method 'POST'/Method 'PUT'
http://.../api/products/{id_product}/

Eliminar un producto -> Method 'DELETE'
http://.../api/products/{id_product}/

### ORDERS

Listar todas las ordenes -> Method 'GET'
http://.../api/orders/

Consultar una orden y sus detalles -> Method 'GET'
http://.../api/orders/{id_order}/ (simple)
http://.../api/orders/{id_order}/detail_info/ (completo)

Registrar/Editar una orden -> Method 'POST'/Method 'PUT'
http://.../api/orders/{id_order}/

Eliminar una orden -> Method 'DELETE'
http://.../api/orders/{id_order}/

### ORDERS DETAILS

Editar un detalle de una orden -> Method 'PUT'
http://.../api/orderdetails/{id_orderdetail}/

Eliminar un detalle de una orden -> Method 'DELETE'
http://.../api/orderdetails/{id_orderdetail}/


