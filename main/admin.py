from django.contrib import admin
from main.models import *

# Register your models here.

admin.site.register(Brand)
admin.site.register(Size)

##################### Banner in admin panel ####################
class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(Banner, BannerAdmin)

##################### category in admin panel ####################
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','title','image_tag')
admin.site.register(Category, CategoryAdmin)

##################### color in admin panel ####################
class ColorAdmin(admin.ModelAdmin):
    list_display=('id','title','color_bg')
admin.site.register(Color, ColorAdmin)

##################### Product in admin panel ####################
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','status', 'is_featured')
    list_editable=('status', 'is_featured')
    prepopulated_fields = {'slug':('title',)}
admin.site.register(Product, ProductAdmin)

##################### Product Attribute ####################
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','product','image_tag','price','color','size')
admin.site.register(ProductAttribute, ProductAttributeAdmin)

##################### Order ####################
class CartOrderAdmin(admin.ModelAdmin):
    # list_editable=('paid_status', 'order_status')
    list_display=('user','total_amt','paid_status','order_dt', 'order_status')
admin.site.register(CartOrder, CartOrderAdmin)

##################### Order Items ####################
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems, CartOrderItemsAdmin)

##################### Product Review ####################
class ProductReviewAdmin(admin.ModelAdmin):
    list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview, ProductReviewAdmin)

##################### Wishlist ####################
class WishlistAdmin(admin.ModelAdmin):
    list_display=('user', 'product')
admin.site.register(Wishlist, WishlistAdmin)

##################### User Addreses ####################
class UserAddressBookAdmin(admin.ModelAdmin):
    list_display=('user', 'address', 'status')
admin.site.register(UserAddressBook, UserAddressBookAdmin)
