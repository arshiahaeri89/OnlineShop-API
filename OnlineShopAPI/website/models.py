from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from .utils import upload_to, generate_random_username


class ShopUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True, verbose_name='Phone Number')
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    postal_code = models.CharField(max_length=10, verbose_name='Postal Code',
                                   null=True, blank=True)

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
                                 verbose_name='Category')
    price = models.IntegerField(verbose_name='Price')
    has_off = models.BooleanField(verbose_name='Has Off')
    price_after_off = models.IntegerField(verbose_name='Price After Off',
                                          null=True, blank=True)
    stock = models.IntegerField(verbose_name='Stock Count')
    product_code = models.CharField(max_length=10, unique=True,
                                    verbose_name='Product Code')

    def __str__(self):
        return f'{self.product_code} - {self.title} - {self.category}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)
    image_number = models.IntegerField(verbose_name='Image Number')

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
    rate = models.FloatField(verbose_name='Rate',
                               validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.user.username} - {self.product}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
