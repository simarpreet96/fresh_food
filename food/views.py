from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
import requests 
from django.contrib import messages
from .models import User, Product, Category, Cart, Order, ContactUs, Wish, subcategory, BillingAddress
from django.utils import timezone
from .forms import loginForm, SignUpForm, CartForm, ProductForm, BillingForm, ContactUsForm
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from food.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from food.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
#from django.contrib.auth import login
#from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
User = get_user_model()

# def contact_us(request):
#     cus = ContactUs(name=request.GET['name'],
#                     email=request.POST['email'], 
#                     enquiry=request.POST['enquiry'])
#     cus.save()
#     return redirect('food/contact.html')

def contact_us(request):
    cus = ContactUs.objects.all()
    if request.method =='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ContactUsForm()
    return render(request, 'food/contact.html', {'form':form})

def pro_category(request):
    food=subcategory.objects.filter(Q(category__title='f'))
    veg=subcategory.objects.filter(Q(category__title='v'))
    ext=subcategory.objects.filter(Q(category__title='e'))

    return render(request, 'food/category.html', {'food': food, 'veg':veg, 'ext':ext})


def about_us(request):
    return render(request, 'food/about-us.html')

def privacy_policy(request):
    return render(request,'registration/privacy_policy.html')

def user_list(request):
    posts2 = User.objects.filter(first_name=request.user)
    return render(request,'food/user_profile.html',{'posts2': posts2})

def user_del(requet, pk):
    post = get_object_or_404(User, pk=pk)
    post.delete()
    return redirect('user_list')

def user_edit(request, pk):
    post = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = SignUpForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('user_list')
    else:
        form = SignUpForm(instance=post)
    return render(request, 'food/user_edit.html', {'form': form})

def search(request):
    query = request.GET['query']
    if len(query) > 50:
        allpost= Product.objects.none()
    else:
        allpost=Product.objects.filter(Q(name__icontains=query)|
                                        Q(category__name__icontains=query)|
                                        Q(detail_text__icontains=query))
    if allpost.count() == 0:
        messages.error(request,'can not found')
    return render(request,'food/search.html',{'allpost':allpost, 'query':query})


def product_pg(request, pk):
    prd= get_object_or_404(Product, pk=pk)
    return render(request,'food/product.html', {'prd':prd})

@login_required
def product_byuser(request):
    posts = Product.objects.filter(Q(author=request.user))
    #print(posts.query)
    return render(request, 'food/product_list.html',{'posts':posts})

def product_del(requet, pk):
    post = get_object_or_404(Product, pk=pk)
    post.delete()
    return redirect('product_list')

def product_edit(request, pk):
    post = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=post)
    return render(request, 'food/product_edit.html', {'form': form})

def product_list(request):
    Products = Product.objects.filter(published=True)
    return render(request,'food/index.html',{'Products': Products})

def product_list_base(request):
    fru_base = Product.objects.filter(Q(category__title__icontains="f")) & Product.objects.filter(published='True') 
    veg_base = Product.objects.filter(Q(category__title__icontains="v")) & Product.objects.filter(published='True') 
    ext_base = Product.objects.filter(Q(category__title__icontains="e")) & Product.objects.filter(published='True') 
    return render(request, 'food/index.html',{'fru_base':fru_base,'veg_base':veg_base,'ext_base':ext_base})

def product_publish(request,pk):
    post =Product.objects.get(pk=pk)
    if post.published== 0:
        post.published= 1
        post.save()
        messages.info(request,'product is published')
    elif post.published== 1:
        post.published= 0
        post.save()
        messages.info(request,'product is unpublished')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'food/add_product.html', {'form': form})

def fruit_list(request):
    fru = Product.objects.filter(Q(category__title__icontains="f")) & Product.objects.filter(published='True') 
    print(fru.query)
    return render(request,'food/fruit_index.html',{'fru': fru})

def veg_list(request):
    veg = Product.objects.filter(Q(category__title__contains="v")) & Product.objects.filter(published='True') 
    return render(request,'food/veg_index.html',{'veg': veg})

def ext_list(request):
    ext = Product.objects.filter(Q(category__title__contains="e")) & Product.objects.filter(published='True') 
    return render(request,'food/extra_index.html',{'ext': ext})

@login_required
def remove_wish(request,pk):
    item=get_object_or_404(Product,pk=pk)
    remove_list=Wish.objects.filter(item=item.pk,user=request.user)
    remove_list.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def wishlist_view(request):
    user=request.user
    productw=Product.objects.filter(author=user, price=False)
    wishs=Wish.objects.filter(user=user)  
    if wishs.exists():
        if wishs.exists():
            wish=wishs[0]
            return render(request,'food/wishlist.html', {'productw':productw, 'wishs':wishs})
        else:
            messages.warning(request, "You do not have any item in your Cart")
            return redirect("product_list")
    else:
        messages.warning(request, "You do not have any item in your Cart")
        return redirect("product_list")

    return render(request, 'food/wishlist.html',{'wishs':wishs})

@login_required
def cart_view(request):
    user=request.user
    carts=Cart.objects.filter(user=user, price=False)
    orders=Order.objects.filter(user=user, ordered=False)
    if carts.exists():
        if orders.exists():
            order=orders[0]
            return render(request,'food/cart.html', {'carts':carts, 'order':order})
        else:
            messages.warning(request, "You do not have any item in your wishlist")
            return redirect("product_list")
    else:
        messages.warning(request, "You do not have any item in your wishlist")
        return redirect("product_list")

    return render(request, 'food/cart.html',{'carts':carts})


def add_to_wishlist(request,pk):
    user=request.user
    items = get_object_or_404(Product,pk=pk)
    wished_item,created = Wish.objects.get_or_create(item=items,
                                                    pk = items.pk,
                                                    user = user,)

    messages.info(request,'The item was added to your wishlist')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_to_cart(request, pk):
    item=get_object_or_404(Product, pk=pk)
    order_item, created=Cart.objects.get_or_create(item=item,user=request.user)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.orderitems.filter(item=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,f"{item.name} quantity has update.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            order.orderitems.add(order_item)
            messages.info(request, f"{item.name} has added to your cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
            order=Order.objects.create(user=request.user)
            order.orderitems.add(order_item)
            messages.info(request, f"{item.name} has added to your cart. ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_cart(request, pk):
    item=get_object_or_404(Product, pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is the order
        if order.orderitems.filter(item=item.pk).exists():
            order_item=Cart.objects.filter(item=item, user=request.user)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, f"{item.name} has removed from your cart.")
            messages.info(request, f"{item.name} quantity has updated.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, f"{item.name} Your item is not delete")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def decreaseCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.orderitems.filter(item=item.pk).exists():
            order_item=Cart.objects.filter(item=item, user=request.user)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} has removed frpm your cart.")
            messages.info(request, f"{item.name} quantity has updated.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, f"{item.name} quantity has updated.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checkout(request):
    
    form = BillingForm
    
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].all_total() 
    get_total = order_qs[0].get_totals() 
    get_perse = order_qs[0].get_percentage() 

    context = {"form": form, 
                "order_items": order_items,
                "order_total": order_total,
                "get_total":get_total,
                "get_perse":get_perse
                 }

    # Getting the saved saved_address
    saved_address = BillingAddress.objects.filter(user = request.user)
    if saved_address.exists():
        savedAddress = saved_address.first()
        context = {"form": form, 
                    "order_items": order_items,
                    "order_total": order_total, 
                    "savedAddress": savedAddress
                    }

    if request.method == "POST":
        saved_address = BillingAddress.objects.filter(user = request.user)
        if saved_address.exists():

            savedAddress = saved_address.first()
            form = BillingForm(request.POST, instance=savedAddress)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()
        else:
            form = BillingForm(request.POST)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()
                
    return render(request, 'food/checkout.html', context)

def payment(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    order_total = order_qs[0].all_total() 
    totalCents = float(order_total * 100);
    total = round(totalCents, 2)
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=total,
            currency='usd',
            description=order_qs,
            source=request.POST['stripeToken'])
        print(charge)
        
    return render(request, 'food/payment.html', {"key": key, "total": total})

def filter(request):
    #print(request.GET["filter_type"])
    if 'filter_type' in request.GET and request.GET["filter_type"] == "low":
        Products = Product.objects.filter().order_by('price')
    else:
        Products = Product.objects.filter().order_by('-price')
    #print(Products.query)
    return render(request, 'food/index.html',{'Products': Products})

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            dj_login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('product_list')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('product_list') 

#def signup(request):
#    posts = User.objects.all()
#    if request.method =='POST':
#        form = SignUpForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password')
#            #user = authenticate(username=username, password=raw_password)
#            login(request)
#            return redirect('product_list')
#    else:
#        form = SignUpForm()
#    return render(request, 'registration/register.html', {'form':form})


# def login(request):
#    if request.method =='POST':
#        form = loginForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_date.get('username')
#            raw_password = form.cleaned_date.get('password')
#            #user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            return redirect('post_list')
#    else:  
#        form = loginForm()
#    return render(request, 'templates/food/login.html', {'form':form})