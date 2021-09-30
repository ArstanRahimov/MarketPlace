from django.contrib import admin
from .models import Product, Category, Cart, CartProduct, Favourite


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Favourite)