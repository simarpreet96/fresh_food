from django.contrib import admin
from .models import User,Category,subcategory,Product,Cart,Order,Wish,ContactUs,BillingAddress
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.contrib.admin import AdminSite
from django.core.exceptions import PermissionDenied
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin

# @admin.register(User)
# class UserAdmin(AbstractUserAdmin):
#     def get_queryset(self, request):
#         qs = super(UserAdmin, self).get_queryset(request)
#         if not request.user.is_superuser:
#             return qs.filter(is_superuser=False)
#         return qs

# list_display = ['email', 'is_staff', 'is_active', 'is_superuser', 'seller']

class UserAdmin(admin.ModelAdmin):

    list_display = ['email', 'is_staff', 'is_active']

admin.site.register(User,UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    
    def make_published(self, request, queryset):
        queryset.update(published='True')
    make_published.short_description ="Mark selected stories as published"

    def image_post(self,obj):
        return format_html('<img src="/media/{}" width="100" height="100"/>'.format(obj.image))
    image_post.short_description='Image'

    list_display = ['author','name','price','category','image_post','published','published_date']


admin.site.register(Product,ProductAdmin)

class EventAdminSite(AdminSite):
    site_header = "staff Events Admin"
    site_title = "staff Events Admin Portal"
    index_title = "Welcome to staff Researcher Events Portal"

event_admin_site = EventAdminSite(name='event_admin')

event_admin_site.register(Category)

event_admin_site.register(subcategory)

event_admin_site.register(Cart)

event_admin_site.register(Order)

event_admin_site.register(ContactUs)

event_admin_site.register(BillingAddress)

event_admin_site.register(Group)





admin.site.register(Category)

admin.site.register(subcategory)

admin.site.register(Wish)

admin.site.register(BillingAddress)

admin.site.register(Cart)

admin.site.register(Order)

admin.site.register(ContactUs)

admin.site.unregister(Group)
