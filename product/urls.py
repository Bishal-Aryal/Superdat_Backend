from django.urls import path
from product.views import ProductListView, ProductDetailView, ProductReviewCreateView, ProductCategoryListView, ProductSubCategoryListView, ProductSubCategoryByCategoryView, ProductByCategoryView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('review/create/<int:pk>/', ProductReviewCreateView.as_view(), name='product-review-create'),
    path('categories/', ProductCategoryListView.as_view(), name='category-list'),
    path('subcategories/', ProductSubCategoryListView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', ProductSubCategoryByCategoryView.as_view(), name='subcategory-by-category'),
    path('category/<int:pk>/products/', ProductByCategoryView.as_view(), name='packages-by-direct-category'),
]