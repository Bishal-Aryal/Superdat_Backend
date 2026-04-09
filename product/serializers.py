from rest_framework import serializers
from product.models import Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'name',
            'email',
            'image',
            'rating',
            'comment',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'title', 'description', 'subdescription', 'color', 'quantity', 'price', 'average_rating', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True, source= 'product_reviews')
    class Meta:
        model = Product
        fields = ['id' , 'title', 'description', 'subdescription', 'color', 'quantity', 'price', 'average_rating', 'reviews', 'created_at']



