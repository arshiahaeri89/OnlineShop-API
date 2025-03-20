from django.db import models
from django.utils.text import slugify
from .utils import upload_to


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
                                          null=True)
    stock = models.IntegerField(verbose_name='Stock Count')
    product_code = models.CharField(max_length=10, unique=True,
                                    verbose_name='Product Code')

    # TODO: Add Comments

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
