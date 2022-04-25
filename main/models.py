from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
# Create your models here.

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Homepage Banner Slider $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

class Banner(models.Model):
    img = models.ImageField(upload_to="banner_imgs/")
    alt_text = models.CharField(max_length=300)

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" />' % (self.img.url))

    class Meta:
        verbose_name_plural = 'Banners'

    def __str__(self):
        return self.alt_text

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Category $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural = 'Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="150px" height="150px" />' % (self.image.url))

    def __str__(self):
        return self.title

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Brand $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.title

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Product Color $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Colors'

    def color_bg(self):
        return mark_safe('<div style="width:60px; height:30px; background-color:%s;">  </div>' % (self.color_code))

    def __str__(self):
        return self.title

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Product size $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

class Size(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.title

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Product Model $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

class Product(models.Model):
    title = models.CharField(max_length=200)
    # slug = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True)
    details = models.TextField()
    specs = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Product Attribute $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="product_imgs/", null=True)

    class Meta:
        verbose_name_plural = 'Product Details'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />' % (self.image.url))

    def __str__(self):
        return self.product.title

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Order $$$$$$$$$$$$$$$$$$$$$$$$$$$$$

status_choice=(
    ('OrderProcessed','OrderProcessed'),
    ('CashonDelivery','CashonDelivery'),
    ('OrderDelivered','OrderDelivered'),
)
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False, null=True)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice, default='OrderProcessed', max_length=150)

    class Meta:
        verbose_name_plural = 'Orders'

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Order Items $$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    class Meta:
        verbose_name_plural = 'Ordered Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Product Review $$$$$$$$$$$$$$$$$$$$$$$$$$$$$

RATING = (
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.CharField(choices=RATING, max_length=150)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def get_review_rating(self):
        return self.review_rating

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Wishlist $$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Wishlists'

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Address Book $$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class UserAddressBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10,null=True)
    address = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Users Addresses'