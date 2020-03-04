from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views 
from django.conf.urls.static import static
from food.admin import event_admin_site


urlpatterns = [
    path('admin/', admin.site.urls),
    path('event-admin/', event_admin_site.urls),
    path('', include('food.urls')),
    path('blog/', include('blog.urls')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('django.contrib.auth.urls')),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
