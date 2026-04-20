from django.urls import path
from product.submodules.cart.views import AddToCartView, CartView, UpdateCartItemView, RemoveCartItemView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('view/', CartView.as_view(), name='cart-detail'),
    path('item/update/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('item/remove/<int:pk>/', RemoveCartItemView.as_view(), name='remove-cart-item'),

]