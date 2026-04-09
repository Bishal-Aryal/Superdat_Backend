from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.models import Product
from product.serializers import ProductListSerializer, ProductSerializer, ReviewSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.parsers import MultiPartParser, FormParser


@extend_schema(
    tags=["Products"],
    summary="List All Products",
    description="""
Returns a list of all available products.  
This endpoint is publicly accessible and does not require authentication.
""",
    responses={
        200: ProductListSerializer(many=True),
    },
    examples=[
        OpenApiExample(
            name="Product List Example",
            description="Example response showing multiple products",
            value=[
                {
                    "id": 1,
                    "title": "iPhone 15",
                    "price": "1200.00",
                    "quantity": 10,
                    "created_at": "2026-04-09T10:00:00Z"
                },
                {
                    "id": 2,
                    "title": "Samsung Galaxy S24",
                    "price": "1100.00",
                    "quantity": 15,
                    "created_at": "2026-04-08T08:30:00Z"
                }
            ],
            response_only=True
        )
    ]
)
class ProductListView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=["Products"],
    summary="Get Product Details",
    description="""
Retrieve detailed information about a specific product using its ID.
""",
    responses={
        200: ProductSerializer,
        404: OpenApiExample(
            name="Product Not Found",
            value={"error": "Product not found"},
            response_only=True,
            status_codes=["404"]
        )
    },
    examples=[
        OpenApiExample(
            name="Product Detail Example",
            description="Example response for a single product",
            value={
                "id": 1,
                "title": "iPhone 15",
                "description": "Latest Apple smartphone",
                "price": "1200.00",
                "quantity": 10,
                "category": 1,
                "subcategory": 2,
                "created_at": "2026-04-09T10:00:00Z"
            },
            response_only=True
        )
    ]
)
class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=["Reviews"],
    summary="Create Product Review",
    description="Create a review for a specific product using product ID.",

    request= ReviewSerializer,

    responses=ReviewSerializer
)
class ProductReviewCreateView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                product.update_average_rating()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)