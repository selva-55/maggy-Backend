"""
URL configuration for swiggy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import login_user, Resigter,hotelReg, fetch, LocationSetup, User, CartAdd, CartDelete, CartItems, RestaurantsItem, Remove_different_cart_restaurant, AddAddress, OrderItem, OrderItemRemoveCart, passwordCheck,userUpdate, OrderHistoryFetch, ReorderToCart, ResetPassword

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login', login_user),
    path('user/', User),
    path('userUpdate', userUpdate),
    path('register', Resigter),
    path('hotelreg', hotelReg),
    path('hotels', fetch),
    path('location', LocationSetup),
    path('cartAdd', CartAdd),
    path('cartDelete/', CartDelete),
    path('cartItems/', CartItems),
    path('RestaurantsItem/', RestaurantsItem),
    path('removeDifferentcartItem', Remove_different_cart_restaurant),
    path('updateaddress', AddAddress),
    path('order', OrderItem),
    path('orderRemoveCartItem/', OrderItemRemoveCart),
    path('passwordcheck', passwordCheck),
    path('orderHistory/', OrderHistoryFetch),
    path('reorder', ReorderToCart),
    path('resetPassword', ResetPassword),



]
