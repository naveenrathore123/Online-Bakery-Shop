from django.urls import path
from . import views

app_name = 'store' # Because of namespace

urlpatterns = [
    path('', views.base_home, name='base_home'),
    path('product_all', views.product_all, name='store_home'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>', views.category_list, name="category_list"),
] 
