"""Akvaplast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import Main_app.views as Main_app


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main_app.main_page),
    path('products/', Main_app.category),
    path('products/<int:offset>/', Main_app.category),
    path('products/group_<str:grp>/', Main_app.group),
    path('products/group_<str:grp>/<int:offset>/', Main_app.group),
    path('search_<str:text>/', Main_app.search_results),
    path('search_<str:text>/<int:offset>/', Main_app.search_results),
    path('promotion/', Main_app.promotion),
    path('promotion/<int:offset>/', Main_app.promotion),
    path('products/product-item_<int:name>/', Main_app.product_item),
    path('articles/', Main_app.articles_list),
    path('articles/<int:offset>/', Main_app.articles_list),
    path('articles/article-item_<int:name>/', Main_app.article_item),
    path('company/', Main_app.company),
    path('shipping_and_payment/', Main_app.ShippingPayment),
    path('contacts/', Main_app.contacts),
    path('reviews/', Main_app.reviews),
]



