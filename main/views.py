import calendar
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from django.db.models import Max, Min, Count, Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import SignupForm, ReviewAdd, AddressBookForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
# paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
# Create your views here.

# %%%%%%%%%%%%%%%%%%%% HOME PAGE %%%%%%%%%%%%%%%%%%%%


def home(request):
    banners = Banner.objects.all().order_by('-id')
    data = Product.objects.filter(is_featured=True).order_by('-id')
    return render(request, 'index.html', {'data': data, 'banners': banners})

# %%%%%%%%%%%%%%%%%%%% CATEGORY %%%%%%%%%%%%%%%%%%%%


def category_list(request):
    data = Category.objects.all().order_by('-id')
    return render(request, 'category_list.html', {'data': data})

# %%%%%%%%%%%%%%%%%%%% BRAND %%%%%%%%%%%%%%%%%%%%


def brand_list(request):
    data = Brand.objects.all().order_by('-id')
    return render(request, 'brand_list.html', {'data': data})

# %%%%%%%%%%%%%%%%%%%% BROWSE PRODUCTS LIST WITH FILTER %%%%%%%%%%%%%%%%%%%%

def product_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:6]
    return render(request, 'product_list.html',
                  {
                      'data': data,
                      'total_data': total_data,
                  })

# %%%%%%%%%%%%%%%%%%%% LIST PRODUCTS BY CATEGORIES IN CATEGORIES PAGE %%%%%%%%%%%%%%%%%%%%


def category_product_list(request, cat_id):
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by('-id')
    return render(request, 'category_product_list.html',
                  {
                      'data': data,
                  })

# %%%%%%%%%%%%%%%%%%%% LIST PRODUCTS BY BRAND IN BRANDS PAGE %%%%%%%%%%%%%%%%%%%%


def brand_product_list(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    return render(request, 'brand_product_list.html',
                  {
                      'data': data,
                  })

# %%%%%%%%%%%%%%%%%%%% PRODUCT DETAIL PAGE  %%%%%%%%%%%%%%%%%%%%


def product_detail(request, slug, id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(
        category=product.category).exclude(id=id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values(
        'color__id', 'color__title', 'color__color_code').distinct()
    sizes = ProductAttribute.objects.filter(product=product).values(
        'size__id', 'size__title', 'price', 'color__id').distinct()
    reviewForm = ReviewAdd()

    # Check
    canAdd = True
    try:
        reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
    except Exception as e:
        pass
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
    # End

    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'product_detail.html',
                  {
                      'data': product,
                      'related': related_products,
                      'colors': colors,
                      'sizes': sizes,
                      'reviewForm': reviewForm,
                      'canAdd': canAdd,
                      'reviews': reviews,
                      'avg_reviews': avg_reviews
                  })

# %%%%%%%%%%%%%%%%%%%% SEARCH BAR %%%%%%%%%%%%%%%%%%%%


def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'search.html', {'data': data})

# %%%%%%%%%%%%%%%%%%%% FILTER DATA %%%%%%%%%%%%%%%%%%%%


def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)

    if len(colors) > 0:
        allProducts = allProducts.filter(
            productattribute__color__id__in=colors).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(
            category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(
            productattribute__size__id__in=sizes).distinct()
    t = render_to_string('ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})

# %%%%%%%%%%%%%%%%%%%% LOAD MORE PAGINATION %%%%%%%%%%%%%%%%%%%%


def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t})


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%% CART SESSION OPERATIONS %%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# ADD TO CART
def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})

# CART LIST PAGE
def cart_list(request):
    total_amt = 0
    # new
    address = None
    try:
        address = UserAddressBook.objects.filter(user=request.user, status=True).first()
    except Exception as e:
        pass
    # new
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt, 'address':address})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt, 'address':address})


# DELETE CART ITEM
def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

# UPDATE CART ITEM
def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# %%%%%%%%%%%%%%%%%%%% SIGNUP FORM %%%%%%%%%%%%%%%%%%%%

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
    form = SignupForm
    return render(request, 'registration/signup.html', {'form': form})

# %%%%%%%%%%%%%%%%%%%% CHECKOUT PAGE WITH PAYPAL %%%%%%%%%%%%%%%%%%%%


@login_required
def checkout(request):

    try:
        status_unpaid=CartOrder.objects.all().filter(paid_status=False).delete()
    except ObjectDoesNotExist:
        pass

    total_amt = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty'])*float(item['price'])
        # Order
        order = CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt
        )
        # End
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
            # OrderItems
            items = CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price'])
            )
            # End

        # Process Payment
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amt*0.01311,  # MULTIPLY INR WITH USD CONVERSION RATE
            'item_name': 'OrderNo-'+str(order.id),
            'invoice': 'INV-'+str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        
        address = UserAddressBook.objects.filter(user=request.user, status=True).first()
        return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt, 'form': form, 'address': address})


@csrf_exempt
def payment_done(request):
    # newcode
    cartModel=CartOrder.objects.get(user=request.user, paid_status=False)
    cartModel.paid_status=True
    cartModel.save()
    returnData = request.POST
    return render(request, 'payment-success.html', {'data': returnData})


# new

def cash_on_delivery(request):
    cartModel=CartOrder.objects.get(user=request.user, paid_status=False)
    cartModel.paid_status=None
    cartModel.order_status='CashonDelivery'
    cartModel.save()
    return redirect('my_orders')

# new


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment-fail.html')

# %%%%%%%%%%%%%%%%%%%% SAVE REVIEW %%%%%%%%%%%%%%%%%%%%


def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})

# %%%%%%%%%%%%%%%%%%%% USER DASHBOARD %%%%%%%%%%%%%%%%%%%%


@login_required
def my_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).annotate(month=ExtractMonth('order_dt')).values(
        'month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'user/dashboard.html', {'monthNumber': monthNumber, 'totalOrders': totalOrders})

# %%%%%%%%%%%%%%%%%%%% MY ORDERS %%%%%%%%%%%%%%%%%%%%


@login_required
def my_orders(request):
    address = UserAddressBook.objects.filter(user=request.user, status=True).first()
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html', {'orders': orders, 'address':address})

# %%%%%%%%%%%%%%%%%%%% ORDER DETAIL %%%%%%%%%%%%%%%%%%%%


@login_required
def my_order_items(request, id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html', {'orderitems': orderitems})

# %%%%%%%%%%%%%%%%%%%% WISHLIST %%%%%%%%%%%%%%%%%%%%


def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(
        product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)

# %%%%%%%%%%%%%%%%%%%% MY WISHLIST %%%%%%%%%%%%%%%%%%%%


@login_required
def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html', {'wlist': wlist})

# %%%%%%%%%%%%%%%%%%%% DELETE WISHLIST %%%%%%%%%%%%%%%%%%%%


@login_required
def delete_wishlist(request, id):
    Wishlist.objects.get(pk=id).delete()
    return redirect('my_wishlist')

# %%%%%%%%%%%%%%%%%%%% MY REVIEWS %%%%%%%%%%%%%%%%%%%%


@login_required
def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html', {'reviews': reviews})

# %%%%%%%%%%%%%%%%%%%% DELETE REVIEW %%%%%%%%%%%%%%%%%%%%


@login_required
def delete_review(request, id):
    ProductReview.objects.get(pk=id).delete()
    return redirect('my-reviews')

# %%%%%%%%%%%%%%%%%%%% MY ADDRESSES %%%%%%%%%%%%%%%%%%%%


@login_required
def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/addressbook.html', {'addbook': addbook})

# %%%%%%%%%%%%%%%%%%%% SAVE ADDRESSES BOOK %%%%%%%%%%%%%%%%%%%%


@login_required
def save_address(request):
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.filter(user=request.user).update(status=False)
            saveForm.save()
            msg = 'Address Added Successfully'
    form = AddressBookForm
    return render(request, 'user/add-address.html', {'form': form, 'msg': msg})

# %%%%%%%%%%%%%%%%%%%% ACTIVATE ADDRESS %%%%%%%%%%%%%%%%%%%%


@login_required
def activate_address(request):
    a_id = str(request.GET['id'])
    UserAddressBook.objects.filter(user=request.user).update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool': True})

# %%%%%%%%%%%%%%%%%%%% EDIT PROFILE %%%%%%%%%%%%%%%%%%%%


@login_required
def edit_profile(request):
    msg = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Profile Updated'
    form = ProfileForm(instance=request.user)
    return render(request, 'user/edit-profile.html', {'form': form, 'msg': msg})

# %%%%%%%%%%%%%%%%%%%% UPDATE ADDRESS %%%%%%%%%%%%%%%%%%%%


@login_required
def update_address(request, id):
    address = UserAddressBook.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.filter(user=request.user).update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm(instance=address)
    return render(request, 'user/update-address.html', {'form': form, 'msg': msg})

# %%%%%%%%%%%%%%%%%%%% DELETE ADDRESS %%%%%%%%%%%%%%%%%%%%


@login_required
def delete_address(request, id):
    UserAddressBook.objects.get(pk=id).delete()
    return redirect('my-addressbook')