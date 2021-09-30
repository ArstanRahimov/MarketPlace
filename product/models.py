from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название', max_length=75)
    slug = models.SlugField(primary_key=True)


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='products')
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField('Изображения')
    price = models.DecimalField('Цена', max_digits=10,
                                decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='products',
                             verbose_name='Автор',
                             default=User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

    def total_favourites(self):
        return self.favourites.count()


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='likes')
    likes = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='likes')


class Favourite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='favourite')
    favourite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favourite')


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='cart_products')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE,
                             related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='cart_products')
    final_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=True, verbose_name='Общая сумма')

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='cart', verbose_name='Владелец')
    products = models.ManyToManyField(CartProduct, blank=True, related_name='carts')
    total_products = models.PositiveIntegerField(default=0, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        self.total_products = sum([p.quantity for p in self.cart_products.all()])
        self.final_price = sum([cartproduct.final_price for cartproduct in self.cart_products.all()])


