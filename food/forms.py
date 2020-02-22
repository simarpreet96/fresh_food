from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Cart, Product, ContactUs, BillingAddress

class loginForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='enter valid email')
	class Meta:
		model=User
		fields=('email','password')

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email','username','address1','address2',
            'country','city','postal_code', 'image','password1', 'password2','subscribe')

class ProductForm(forms.ModelForm):
	class Meta:
		model=Product
		fields=('name','price','image','detail_text','category','published',
			'published_date')

class CartForm(forms.ModelForm):
	class Meta:
		model=Cart
		fields="__all__" 

class BillingForm(forms.ModelForm):

    class Meta:
        model = BillingAddress
        fields = ['address', 'zipcode', 'city', 'landmark']

class ContactUsForm(forms.ModelForm):
	class Meta:
		model=ContactUs
		fields=('name','email','enquiry')