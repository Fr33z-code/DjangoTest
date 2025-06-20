import json
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from app1.models import Product, Cart, CartItem


@login_required
def place_order(request):
    cart = Cart.objects.get(user_id=request.user)
    CartItem.objects.filter(cart_id=cart.id).delete()
    return redirect('home')


@login_required
@csrf_exempt
def add_to_cart_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product id'})
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@never_cache
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_amount = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount
    }
    return render(request, 'cart.html', context)


@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)

        for item in cart.items.all():
            new_quantity = request.POST.get(f'quantity_{item.id}')
            if new_quantity and new_quantity.isdigit():
                item.quantity = int(new_quantity)
                item.save()

        return redirect('cart')
    return None


@require_POST
@login_required
def update_cart_item(request):
    item_id = request.POST.get('item_id')
    quantity = request.POST.get('quantity')

    if not item_id or not quantity:
        return JsonResponse({'success': False, 'error': 'Недопустимые данные'})

    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Неверное количество'})

    try:
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.quantity = quantity
        item.save()
        return JsonResponse({'success': True})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Товар не найден'})


@login_required
def delete_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=product_id, cart=cart)
    item.delete()
    return redirect('view_cart')


# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if product.in_stock:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_item, item_created = CartItem.objects.get_or_create(
#             cart=cart,
#             product=product,
#             defaults={'quantity': 1}
#         )
#
#         if not item_created:
#             cart_item.quantity += 1
#             cart_item.save()
#
#         return redirect('catalog')
#     else:
#         messages.error(request, 'Товара нет в наличии.')
#         return redirect('catalog')


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def catalog(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    prices = Product.objects.filter(in_stock=True).values_list('price', flat=True)
    min_catalog_price = min(prices) if prices else None
    max_catalog_price = max(prices) if prices else None

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'min_price': min_catalog_price,
        'max_price': max_catalog_price,
        'min_price_filter': min_price,
        'max_price_filter': max_price,
        'categories': dict(Product.CATEGORY_CHOICES),
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'catalog/catalog.html', context)


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog')
    return render(request, 'login.html', {
        'form': form,
        'yandex_client_id': settings.YANDEX_CLIENT_ID,
        'redirect_uri': settings.YANDEX_REDIRECT_URI,
    })


@login_required
def profile_view(request):
    user = request.user
    username = user.username
    if user.password == '':
        username = username.split('_')[0]
    return render(request, 'profile.html', {'username': username})


def yandex_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('login')
    token_url = 'https://oauth.yandex.ru/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.YANDEX_CLIENT_ID,
        'client_secret': settings.YANDEX_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to get access token'}, status=400)

    token_data = response.json()
    access_token = token_data.get('access_token')

    user_info_url = 'https://login.yandex.ru/info'
    headers = {'Authorization': f'OAuth {access_token}'}
    user_response = requests.get(user_info_url, headers=headers)

    if user_response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch user info'}, status=400)

    user_data = user_response.json()
    yandex_id = user_data.get('id')
    email = user_data.get('default_email') or f'{yandex_id}@yandex.fake'
    username = f"{user_data.get('login')}_{yandex_id}"
    User = get_user_model()
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    login(request, user)

    return redirect('catalog')
