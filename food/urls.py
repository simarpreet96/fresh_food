from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views 
from food.views import SignUpView, ActivateAccount

urlpatterns = [
	path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
	path('user_list/', views.user_list, name='user_list'),
	path('user/<int:pk>/edit/', views.user_edit, name='user_edit'),
	path('user/<pk>/del/', views.user_del, name='user_del'),
	path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('search/', views.search, name='search'),  
	path('fruit_list/', views.fruit_list, name='fruit_list'),
	path('veg_list/', views.veg_list, name='veg_list'),
	path('ext_list/', views.ext_list, name='ext_list'),
	path('', views.product_list, name='product_list'),
	path('product/<int:pk>/', views.product_pg, name='product_pg'),
	path('add_product/', views.add_product, name='add_product'),
	path('product_byuser/', views.product_byuser, name='product_byuser'),
	path('product_publish/<int:pk>', views.product_publish, name='product_publish'),
	path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
	path('product_del/<int:pk>/', views.product_del, name='product_del'),
	path('checkout/', views.checkout, name='checkout'),
	path('payment/', views.payment, name="payment"),
	path('add_to_wishlist/<int:pk>', views.add_to_wishlist, name='add_to_wishlist'),
	path('wishlist_view/', views.wishlist_view, name='wishlist_view'),
	path('remove_wish/<int:pk>', views.remove_wish, name='remove_wish'),
	path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
	path('cart_view/', views.cart_view, name='cart_view'),
	path('delete_cart/<int:pk>/', views.delete_cart, name='delete_cart'),
	path('decreaseCart/<int:pk>/', views.decreaseCart, name='decreaseCart'),
	path('filter/', views.filter, name='filter'),
	path('contact_us/', views.contact_us, name='contact_us'),
	path('about_us/', views.about_us, name='about_us'),
	path('pro_category/', views.pro_category, name='pro_category'),
	path('product_list_base/', views.product_list_base, name='product_list_base'),


	#path('signup/', views.signup, name='signup'),
	#path('login/', views.login, name='login'),
]