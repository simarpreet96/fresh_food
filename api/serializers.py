from rest_framework import serializers
from food.models import User, Product, Category, Cart
from blog.models import Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'country', 'is_staff',)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user','item','quantity','created','price',)

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('title',)

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Product
        fields = ('author','name','price','detail_text','published_date', 'category',)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'status', 'published_date', 'text',)


