from django.urls import path
from product.views import ProductListView, ProductDetailView, ProductReviewCreateView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('review/create/<int:pk>/', ProductReviewCreateView.as_view(), name='product-review-create'),
]