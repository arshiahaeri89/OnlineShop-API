from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from .utils import upload_to, generate_random_username, random_str


class ShopUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    username = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True, verbose_name='Phone Number')
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    postal_code = models.CharField(max_length=10, verbose_name='Postal Code',
                                   null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f'{self.username} - {self.phone_number}'

    def save(self, *args, **kwargs):
        if not self.username:
            while True:
                random_username = generate_random_username()

                if not ShopUser.objects.filter(username=random_username).exists():
                    self.username = slugify(random_username)
                    break
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Shop User'
        verbose_name_plural = 'Shop Users'


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Category')
    en_name = models.CharField(max_length=50, verbose_name='English Name')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.en_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    brand = models.CharField(max_length=50, verbose_name='Brand')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Category', related_name='products')
    price = models.PositiveIntegerField(verbose_name='Price')
    has_off = models.BooleanField(verbose_name='Has Off')
    price_after_off = models.PositiveIntegerField(verbose_name='Price After Off',
                                                  null=True, blank=True)
    stock = models.IntegerField(verbose_name='Stock Count')
    product_code = models.CharField(max_length=10, unique=True,
                                    verbose_name='Product Code')
    created_at = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)

    def __str__(self):
        return f'{self.product_code} - {self.title} - {self.category}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)
    image_number = models.PositiveIntegerField(verbose_name='Image Number')

    def __str__(self):
        return f'{self.product.product_code} - {self.image_number}'

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE,
                             related_name='comments')
    title = models.CharField(max_length=50, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    rate = models.DecimalField(verbose_name='Rate', max_digits=2, decimal_places=1,
                               validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Order(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE,
                             related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='orders')
    quantity = models.PositiveIntegerField(default=1,
                                           validators=[MinValueValidator(1)],
                                           verbose_name='Quantity')
    total_price = models.PositiveIntegerField(verbose_name='Total Price', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('payed', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'موفق'),
        ('canceled', 'لغو شده'),
        ('returned', 'مرجوع شده'),
        ('refunded', 'هزینه برگشت داده شده'),
    ], default='payed')
    track_code = models.CharField(max_length=10, unique=True,
                                  editable=False, verbose_name='Track Code')

    @staticmethod
    def generate_random_track_code(length):
        while True:
            track_code = random_str(length)
            if not Order.objects.filter(track_code=track_code).first():
                break
        return track_code

    def save(self, *args, **kwargs):
        # Calculating the price
        product_price = self.product.price_after_off if self.product.has_off else self.product.price
        self.total_price = self.quantity * product_price

        # Generating the track_code
        self.track_code = self.generate_random_track_code(10)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.track_code} - {self.product.product_code} - {self.quantity} - {self.status}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
