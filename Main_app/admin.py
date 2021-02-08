from django.contrib import admin
from Main_app.models import Сategory, ProductGroups, Products, Articles
# Register your models here.

class СategoryAdmin(admin.ModelAdmin): # предназначен описания вида представления инфы строк таблицы в админке
    list_display = ('category',)  # описывает какие данные будут отображаться, и сортировка по ним
    #search_fields = ('district','region__region') # добавляем панель поиска #, 'region__region__region'

class ProductGroupsAdmin(admin.ModelAdmin): 
    list_display = ('group', 'category')  
    search_fields = ('group','category__category') 

class ProductsAdmin(admin.ModelAdmin): 
    list_display = ('name','group',"mod","prise","availability","promotion") 
    search_fields = ('name','group__group',"availability","promotion") 

class ArticlesAdmin(admin.ModelAdmin): 
    list_display = ('name',) 
    search_fields = ('name','description')    


admin.site.register(Сategory,СategoryAdmin)
admin.site.register(ProductGroups,ProductGroupsAdmin)
admin.site.register(Products,ProductsAdmin)
admin.site.register(Articles,ArticlesAdmin)

 
