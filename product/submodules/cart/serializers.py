from rest_framework import serializers
from product.submodules.cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total_price']
        read_only_fields = ['id','total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
    
    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.title,
            "price": obj.product.price,
            "image": self.context['request'].build_absolute_uri(obj.product.image.url) if obj.product.image else None
        }
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    cart_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_id', 'items','cart_count', 'created_at']
        read_only_fields = ['cart_id', 'created_at', 'items']
    
    def get_cart_count(self, obj):
        return obj.items.count()