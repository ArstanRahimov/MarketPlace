
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('product', ProductViewSet, 'product')
router.register('category', CategoryViewSet, 'category')
router.register('cart', CartViewSet, 'cart')

urlpatterns = [
    path('', include(router.urls)),
    path('favourite/', FavouriteView.as_view()),
]
