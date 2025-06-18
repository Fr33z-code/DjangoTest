from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Product


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def catalog(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search', '')

    products = Product.objects.filter(in_stock=True)

    if category:
        products = products.filter(category=category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': dict(Product.CATEGORY_CHOICES),
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'catalog/catalog.html', context)


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
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})
