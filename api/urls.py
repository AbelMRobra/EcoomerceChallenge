from api import views
from rest_framework import routers
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewset)
router.register(r'products', views.ProductViewset)
router.register(r'orders', views.OrderViewset)
router.register(r'orderdetails', views.OrderDetailViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),

]
