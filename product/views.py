from django.http import Http404
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import action

from product.models import Product, Category, Cart, CartProduct, User, Like, Favourite
from product.permissions import (IsAuthorOrIsAdmin, IsAuthor, IsAdminUser)
from product.serializers import (ProductListSerializer, CategorySerializer,
                                 ProductDetailSerializer, CartSerializer, CartItemSerializer,
                                 FavouriteProductSerializer, ProductCreateSerializer)


class ProductFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'created_at')


class CategoryFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Category
        fields = ('name', 'created_at')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter,
                       rest_filter.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductCreateSerializer

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(product=product, user=user)
            like.likes = not like.likes
            if like.likes:
                like.save()
            else:
                like.delete()
            message = 'нравится' if like.likes else 'не нравится'
        except Like.DoesNotExist:
            Like.objects.create(product=product, user=user, likes=True)
            message = 'нравится'
        return Response(message, status=200)

    @action(['POST'], detail=True)
    def favourite(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            favourite = Favourite.objects.get(product=product, user=user)
            favourite.favourite = not favourite.favourite
            if favourite.favourite:
                favourite.save()
            else:
                favourite.delete()
            message = 'в избранном' if favourite.favourite else 'не в избранном'
        except Favourite.DoesNotExist:
            Favourite.objects.create(product=product, user=user, favourite=True)
            message = 'в избранном'
        return Response(message, status=200)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'list':
            return []
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        elif self.action in ['like', 'favourite']:
            return [IsAuthenticated()]
        else:
            return []


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter,
                       rest_filter.OrderingFilter]
    filterset_class = CategoryFilter
    search_fields = ['name']
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        elif self.action == 'retrieve':
            return CategorySerializer
        return CategorySerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthorOrIsAdmin, IsAuthenticated]

    @staticmethod
    def _get_or_create_cart_product(user: User, cart: Cart, product: Product):
        cart_product, created = CartProduct.objects.get_or_create(
            user=user,
            product=product,
            cart=cart
        )
        return cart_product, created


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = Cart.objects.all()


class FavouriteView(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteProductSerializer


class FavouritesListView(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
