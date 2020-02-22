from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from food.views import *
from blog.views import *
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from api.views import  UserViewSet, api_root, PostViewSet, ProductViewSet,CartViewSet
# from food import views
# from blog import views
from .import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'carts', views.CartViewSet)


product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

cart_list = CartViewSet.as_view({
    'get': 'list'
})
cart_detail = CartViewSet.as_view({
    'get': 'retrieve'
})


post_list = PostViewSet.as_view({
    'get':'list'
    })
post_detail = PostViewSet.as_view({
    'get':'retrieve'

    })


# API endpoints
urlpatterns = format_suffix_patterns([
	path('', api_root),
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('posts/', post_list, name='post-list'),
    path('posts/<int:pk>/', post_detail, name='post-detail'),
    path('cart_list/', cart_list, name='cart-list'),
    path('cart_detail/<int:pk>/', cart_detail, name='cart-detail'),

])