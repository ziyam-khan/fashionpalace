from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# from jet.dashboard.dashboard_modules import google_analytics_views

urlpatterns=[
    path('', views.home, name='home'),
# SEARCH
    path('search', views.search, name='search'),
# CATEGORIES LIST PAGE
    path('category-list', views.category_list, name='category-list'),
# BRANDS LIST PAGE
    path('brand-list',views.brand_list,name='brand-list'),
# PRODUCTS & BROWSE LIST PAGE
    path('product-list',views.product_list,name='product-list'),
# LIST PRODUCTS BY CATEGORIES IN CATEGORIES PAGE
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
# LIST PRODUCTS BY BRANDS IN BRANDS PAGE
    path('brand-product-list/<int:brand_id>',views.brand_product_list,name='brand-product-list'),
# PRODUCT DETAIL PAGE
    path('product/<str:slug>/<int:id>', views.product_detail, name='product_detail'),
# FILTER
    path('filter-data', views.filter_data, name='filter-data'),
# LOAD MORE PAGINATION
    path('load-more-data', views.load_more_data, name='load_more_data'),
# ADD TO CART
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
# CART PAGE
    path('cart', views.cart_list, name='cart'),
# DELETE ITEM FROM CART
    path('delete-from-cart', views.delete_cart_item, name='delete-from-cart'),
# UPDATE ITEM FROM CART
    path('update-cart', views.update_cart_item, name='update-cart'),
# SIGNUP FORM
    path('accounts/signup', views.signup, name='signup'),
# CHECKOUT PAGE
    path('checkout', views.checkout, name='checkout'),
# PAYPAL
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
# REVIEW
    path('save-review/<int:pid>', views.save_review, name='save-review'),
# USER SECTION
    path('my-dashboard', views.my_dashboard, name='my_dashboard'),
# MY ORDERS SECTION
    path('my-orders', views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>', views.my_order_items, name='my_order_items'),
# WISHLIST
    path('add-wishlist', views.add_wishlist, name='add_wishlist'),
    path('my-wishlist', views.my_wishlist, name='my_wishlist'),
    path('delete-wishlist/<int:id>', views.delete_wishlist, name='delete-wishlist'),
# MY REVIEWS SECTION
    path('my-reviews', views.my_reviews, name='my-reviews'),
    path('delete-review/<int:id>', views.delete_review, name='delete-review'),
# MY ADDRESSES SECTION
    path('my-addressbook', views.my_addressbook, name='my-addressbook'),
    path('add-address', views.save_address, name='add-address'),
    path('activate-address', views.activate_address, name='activate-address'),
#  EDIT PROFILE
    path('edit-profile', views.edit_profile, name='edit-profile'),
# UPDATE ADDRESS
    path('update-address/<int:id>', views.update_address, name='update-address'),
    path('delete-address/<int:id>', views.delete_address, name='delete-address'),
# CASH ON DELIVERY
    path('cash-on-delivery', views.cash_on_delivery, name='cash-on-delivery')
# RESET PASSWORD
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)