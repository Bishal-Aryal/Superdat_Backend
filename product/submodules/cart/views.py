from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from product.submodules.cart.models import Cart, CartItem
from product.submodules.cart.serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

@extend_schema(
    tags=["Cart"],
    summary="Add product to cart",
    description="Add a product to cart using cart_id. If cart does not exist, it will be created.",
    request={
        "application/json": {
            "example": {
                "product_id": 1,
                "quantity": 2
            }
        }
    },
    responses={
        200: OpenApiExample(
            "Success",
            value={
                "message": "Added to cart",
                "cart_id": "uuid-string"
            }
        )
    }
)
class AddToCartView(APIView):
    def post(self, request):
        cart_id = request.data.get('cart_id')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(cart_id)
        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({
            "message": "Added to cart",
            "cart_id": str(cart.cart_id)
        })

@extend_schema(
    tags=["Cart"],
    summary="Get cart details",
    description="Retrieve cart using cart_id",
    parameters=[
        OpenApiParameter(
            name='cart_id',
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Cart UUID"
        )
    ],
    responses={200: CartSerializer}
)
class CartView(APIView):
    def get(self, request):
        cart_id = request.query_params.get('cart_id')

        cart = get_object_or_404(Cart, cart_id=cart_id)
        serializer = CartSerializer(cart, context={'request': request})

        return Response(serializer.data)


@extend_schema(
    tags=["Cart"],
    summary="Update cart item quantity",
    description="Update quantity of a cart item. If quantity <= 0, item is removed.",
    request={
        "application/json": {
            "example": {
                "cart_id": "uuid-string",
                "quantity": 3
            }
        }
    },
    responses={
        200: OpenApiExample(
            "Updated",
            value={"message": "Updated"}
        ),
        200: OpenApiExample(
            "Removed",
            value={"message": "Item removed"}
        )
    }
)
class UpdateCartItemView(APIView):
    def patch(self, request, pk):
        cart_id = request.data.get('cart_id')
        quantity = int(request.data.get('quantity'))

        cart = get_object_or_404(Cart, cart_id=cart_id)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)

        if quantity <= 0:
            item.delete()
            return Response({"message": "Removed"})

        item.quantity = quantity
        item.save()

        return Response({"message": "Updated"})


@extend_schema(
    tags=["Cart"],
    summary="Remove item from cart",
    description="Delete a specific cart item",
    request={
        "application/json": {
            "example": {
                "cart_id": "uuid-string"
            }
        }
    },
    responses={
        200: OpenApiExample(
            "Success",
            value={"message": "Removed"}
        )
    }
)
class RemoveCartItemView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk)
        item.delete()

        return Response({"message": "Removed"})