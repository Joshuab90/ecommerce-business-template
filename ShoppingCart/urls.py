from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib import admin
from shopping.views import *

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', index, name="index"),
    path(r'index/', index, name="index"),
    path(r'update_item/', update_item_quantity, name="update_item_quantity"),
    path(r'thankyou/', thank_you, name="thank_you"),
    path(r'confirm_order/', confirm_order, name="confirm_order"),
    path(r'remove_item/', remove_item, name="remove_item"),
    path(r'cart/', cart, name="cart"),
    path(r'credit_card_page/', credit_card_page, name="credit_card"),
    path(r'add_to_cart/', add_to_cart, name="add_to_cart"),
    path(r'signup/', signup, name='signup'),
    path(r'login/', login_view, name='login'),
    path(r'logout/', logout_view, name='logout'),
    path(r'change_password/', change_password, name='change_password'),
    path(r'login_home/', login_home, name='login_home'),
    path(r'auth/', include('social_django.urls', namespace='social')),
]