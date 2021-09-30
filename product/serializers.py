from rest_framework import serializers
from product.models import Product, Category, Cart, CartProduct, Favourite
from review.serializers import ReviewDetailSerializer


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'title', 'price', 'image', 'likes', 'favourite')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['reviews'] = ReviewDetailSerializer(instance.reviews.all(), many=True).data
        rep['likes'] = instance.likes.count()
        rep['favourite'] = instance.favourite.count()
        return rep


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_anonymous:
            raise serializers.ValidationError('Добавлять могут только авторизованные пользователи')
        validated_data['user'] = request.user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity', 'final_price']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    products = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        products = validated_data.pop('products')
        if request.user.is_authenticated:
            cart = Cart.objects.create(user=request.user)
        for product in products:
            CartProduct.objects.create(user=request.user, cart=cart, product=product.get("product"), quantity=product.get("quantity"))
        cart.get_total_price()
        return cart

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        representation["products"] = ProductDetailSerializer([products.product for products in instance.cart_products.all()], many=True, context=self.context).data
        return representation


class FavouriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

        def get_favourite(self, obj):
            if obj.favourite:
                return obj.favourite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favourite'] = self.get_favourite(instance)
            return rep
