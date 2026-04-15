from rest_framework import serializers
from product.models import Product, Review, FAQS, ProductImage, Category, SubCategory


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

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQS
        fields = [
            'id',
            'product',
            'question',
            'answer',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductListSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id' ,'categories', 'sub_categories', 'title', 'description', 'sub_description', 'image', 'color', 'quantity', 'price', 'average_rating', 'created_at']
        read_only_fields = ['id', 'average_rating', 'created_at']

    def get_categories(self, obj):
        result = []
        for category in obj.categories.all():
            result.append({'category_title':category.title})

        return result

    def get_sub_categories(self, obj):
        result = []
        for sub_category in obj.sub_categories.all():
            result.append({'sub_category_title':sub_category.title})

        return result

class ProductSerializer(serializers.ModelSerializer):    
    additional_images = ProductImageSerializer(many=True, read_only=True, source='images')
    faqs = FAQSerializer(many=True, read_only=True, source='product_faqs')
    reviews = ReviewSerializer(many=True, read_only=True, source= 'product_reviews')
    categories = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id' , 'categories', 'sub_categories','title', 'description', 'sub_description', 'color', 'image', 'additional_images', 'faqs', 'quantity', 'price', 'average_rating', 'reviews', 'created_at']
        read_only_fields = ['id', 'average_rating', 'created_at']


    def validate_image(self, value):
        """
        Validates the image file for size and format.

        Ensures that the image does not exceed 5MB in size and is in an
        allowed format (JPEG, JPG, PNG). Raises a ValidationError if the
        conditions are not met.

        Args:
            value: The image file to validate.

        Returns:
            The validated image file.

        Raises:
            serializers.ValidationError: If the image file size exceeds 5MB
            or the format is not JPEG, JPG, or PNG.
        """

        if value:
            if value.size > 5 * 1024 * 1024:  # 5MB limit
                raise serializers.ValidationError(
                    "Profile picture size should not exceed 5MB"
                )

            allowed_formats = ["image/jpeg", "image/jpg", "image/png"]
            if value.content_type not in allowed_formats:
                raise serializers.ValidationError(
                    "Only JPEG, JPG and PNG files are allowed"
                )
            
    def validate_additional_images(self, value):
        """
        Validates the additional images for size and format.

        Ensures that the image does not exceed 5MB in size and is in an
        allowed format (JPEG, JPG, PNG). Raises a ValidationError if the
        conditions are not met.

        Args:
            value: The image file to validate.

        Returns:
            The validated image file.

        Raises:
            serializers.ValidationError: If the image file size exceeds 5MB
            or the format is not JPEG, JPG, or PNG.
        """
        if value:
            if value.size >5 *1024 *1024:
                raise serializers.ValidationError(
                    "Profile picture size should not exceed 5MB"
                )
            allowed_formats = ["image/jpeg", "image/jpg", "image/png"]
            if value.content_type not in allowed_formats:
                raise serializers.ValidationError(
                    "Only JPEG, JPG and PNG files are allowed"
                )

        return value
    
    def get_categories(self, obj):
        result = []
        for category in obj.categories.all():
            result.append({'category_title':category.title})

        return result

    def get_sub_categories(self, obj):
        result = []
        for sub_category in obj.sub_categories.all():
            result.append({'sub_category_title':sub_category.title})

        return result


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductCategorySerializer(serializers.ModelSerializer):
    subcategories = ProductSubCategorySerializer(many=True, read_only=True)
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'subcategories', 'products', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_products(self, obj):
        products = obj.products_category.all()
        return [
            {
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'image': product.image.url if product.image else None
            }
            for product in products
        ] 




