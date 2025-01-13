from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 

from . import views
urlpatterns = [
    
    path('', views.home, name='home'),
    path('product_lists/<int:pk>/', views.product_list, name='product_list'),
    path('login/', views.login_page, name='login_page'),
    path('signup/',views.signup, name='signup'),
    path('logout_view/',views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('product_details/<int:pk>/', views.product_details, name='product_details'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('category/<int:pk>/',views.category,name="category"),
    path('buy/',views.buy,name='checkout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)