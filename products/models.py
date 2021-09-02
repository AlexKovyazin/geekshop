from django.db import models


class ProductsCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get_items():
        # return Products.objects.filter(is_active=True).order_by('category', 'name')
        return Products.objects.order_by('category', 'name')
