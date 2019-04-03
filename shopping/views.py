from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from shopping.models import Product, Cart, Item
from shopping.forms import SignUpForm
import string
import random

# Create your views here.
def index(request):
    user = request.user
    items = ''
    if user.is_anonymous:
        user = ''
    else:
        items = Item.objects.filter(cart__user=user, cart__checked_out=False)
        items = items.count() if items else 0
    products = Product.objects.filter(total_items__gt=0)

    return render(request, 'index.html', {'products':products, 'user':user, 'items':items, 'page':'home'})

def add_to_cart(request):
    user = request.user
    if user.is_anonymous:
        chars = string.ascii_uppercase + string.digits
        user_name = ''.join(random.choice(chars) for _ in range(9))
        password = '1234567a'
        user = User.objects.create(username=user_name, first_name='guest', last_name='guest', email='guest@gmail.com', is_active=True, is_staff=True)
        user.set_password(password)
        user.save()
        user = authenticate(username=user_name, password=password)
        if user:
            login(request, user)
    
    product_id = request.GET.get('product_id')
    cart = Cart.objects.filter(checked_out=False, user=user)
    cart = cart[0] if cart else ''
    if not cart:
        cart = Cart.objects.create(user=user)
    Item.objects.create(cart=cart, product_id=product_id, quantity=1)
    return redirect('index')

def calculate_sum(cart_items):
    items_sum = 0
    for item in cart_items:
        items_sum = items_sum + (item.quantity * item.product.unit_price)
    return items_sum

def cart(request):
    user = request.user
    items= ''
    cart_items = []
    if user.is_anonymous:
        user = ''
    else:
        cart_items = Item.objects.filter(cart__user=user, cart__checked_out=False)
        items = cart_items.count() if cart_items else 0
    items_sum = calculate_sum(cart_items)
    return render(request, 'cart.html', {'user':user, 'items':items, 'page':'cart', 'cart_items': cart_items, 'sum':items_sum})

def update_item_quantity(request):
    item_id = request.GET.get('item_id')
    quantity = request.GET.get('quantity')
    item = Item.objects.get(id=item_id)
    if item.product.total_items > int(quantity):
        item.quantity = quantity
        item.save()
    return redirect('cart')

def thank_you(request):
    user = request.user
    items = ''
    cart_items = []
    if user.is_anonymous:
        user = ''
    else:
        cart_items = Item.objects.filter(cart__user=user, cart__checked_out=False)
        items = cart_items.count() if cart_items else 0
    items_sum = calculate_sum(cart_items)
    return render(request, 'thankyou.html', {'user':user, 'items':items, 'page':'cart', 'cart_items':cart_items, 'sum':items_sum})

def remove_item(request):
    item_id = request.GET.get('item_id')
    Item.objects.get(id=item_id).delete()
    return redirect('cart')

def confirm_order(request):
    user = request.user
    cart_items = Item.objects.filter(cart__user=user, cart__checked_out=False)
    items_sum = calculate_sum(cart_items)
    cart = Cart.objects.get(user=user, checked_out=False)
    cart.checked_out = True
    cart.save()
    User.objects.filter(username=user.username).delete()
    return render(request, 'thankyou.html', {'user':user, 'items':0, 'page':'cart', 'cart_items':cart_items, 'sum':items_sum, 'shopping':'Continue Shopping'})

def credit_card_page(request):
    return render(request, 'credit_card.html',{})

#@login_required(redirect_field_name='login')
def login_home(request):
    auth = True
    if not request.user.is_authenticated:
        auth = False
    return render(request, 'login_home.html', {'auth':auth})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(is_staff=True, is_active=True, **form.cleaned_data)
            messages.success(request, "Your response has been recorded")
            if login_user(request, user):
                return redirect('login_home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def login_user(request, user):
    login(request, user)
    return True

def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login_home')
        else:
            messages.error(request, "Please check your user name and password!")
    return render(request, 'login.html')

@login_required(redirect_field_name='login')
def change_password(request):
    if request.POST:
        user = request.user
        password = request.POST.get('password', None)
        if password:
            user.set_password(password)
            user.save()
        return redirect('login_home')
    return render(request, 'change_password.html')

def logout_view(request):
    logout(request)
    return redirect('login')