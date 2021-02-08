# pylint: disable=E1101

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from Main_app.forms import Search_form
from Akvaplast.settings import security_data
from .models import Products, Сategory, ProductGroups, Articles
import random

api_key = security_data["yandex-map-api-key"]

# Использование or и and в одном запросе при фильтрации
""" Table.objects.filter(Q(field1=1) | Q(field2=2))
Table.objects.filter(
    (Q(field1=1) | Q(field2=2)) &
    (Q(field1=3) | Q(field2=4))
) """

@csrf_exempt
def main_page(request):

    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    rez = Products.objects.filter(promotion=True)
    #print(len(rez))
    #print(len(random.sample(rez,2)))
    lst = random.sample(range(len(rez)),2)
    recomend = rez[lst[0]]
    new = rez[lst[1]]

    rez = Articles.objects.all()
    lst = random.sample(range(len(rez)),2)
    articles = {"article1":rez[lst[0]], "article2":rez[lst[1]]}

    load_css = ["main_temp.css","header.css","home_page.css","bottom_part.css"]
    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = 'Купить трубы в Минске, цена на трубопроводные системы оптом - Продажа труб в Беларуси'
    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": True, "slider":True, "api_key":api_key,"after_page_parts":after_page_parts,
        "recomend":recomend,"new":new, "articles":articles} 
    #'form':form, 'sp':sp, "Teg_a_sp":Teg_a_sp 
    return render_to_response('home_page.html',Tabs)

# Create your views here.

def ccs_load_convector(lst):
    new_lst = []
    for s in lst:
        new_lst.append('css/%s' % s)

    return new_lst


@csrf_exempt
def category(request, offset=1):

    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    len_sp = Сategory.objects.count()
    max_categories = 20

    # Тестируем переключалки страниц
    #len_sp = 300

    cat = Сategory.objects.filter()[(offset-1)*max_categories:offset*max_categories]
    # Тестируем переключалки страниц
    #tttt = random.choice(Сategory.objects.filter())
    #cat = [tttt for i in range(max_categories)]

    a = len_sp // max_categories +1 if len_sp % max_categories > 0 else len_sp // max_categories
    if offset > a: raise Http404

    Teg_a_sp = {"temp":"pagestr.html","lst":NumberPage(a, offset,"products")}

    #cat = Сategory.objects.filter()
    
    groups = []
    #print(cat)
    for tp in cat:
        pg = ProductGroups.objects.filter(category=tp)
        groups.append({"name":tp.category,
            "img":tp.imgPath,
            "group":[{"name_group":item.group} for item in pg]})

    load_css = ["main_temp.css","header.css","products_category.css","bottom_part.css","pagestr.css"]
    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = 'Товары'
    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,
        "categories":groups, "Teg_a_sp":Teg_a_sp } 
    
    return render_to_response('products_category.html',Tabs)


@csrf_exempt
def group(request, grp, offset=1):

    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    max_categories = 20

    # Тестируем переключалки страниц
    #len_sp = 300

    grp_link = ProductGroups.objects.get(group=grp)

    cat = Products.objects.filter(group=grp_link)
    len_sp = cat.count()
    
    current_cat = cat[(offset-1)*max_categories:offset*max_categories]

    # Тестируем переключалки страниц
    #tttt = random.choice(Сategory.objects.filter())
    #cat = [tttt for i in range(max_categories)]

    a = len_sp // max_categories +1 if len_sp % max_categories > 0 else len_sp // max_categories
    if len_sp != 0:
        if offset > a: raise Http404

    Teg_a_sp = {"temp":"pagestr.html","lst":NumberPage(a, offset,"products/group_%s" % grp_link.group)}

    #cat = Сategory.objects.filter()


    load_css = ["main_temp.css","header.css","products_list.css","bottom_part.css","pagestr.css"]
    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = grp_link.group

    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,
        "products":current_cat, "Teg_a_sp":Teg_a_sp, "notempty": len_sp != 0,
        "add_page_content":[]} 
    
    return render_to_response('products_list.html',Tabs)


@csrf_exempt
def search_results(request, text, offset=1):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    max_categories = 20
    

    cat = Products.objects.filter(Q(name__icontains=text) | Q(mod__icontains=text))
    len_sp = cat.count()
    
    current_cat = cat[(offset-1)*max_categories:offset*max_categories]

    a = len_sp // max_categories +1 if len_sp % max_categories > 0 else len_sp // max_categories
    if len_sp != 0:
        if offset > a: raise Http404
    
    Teg_a_sp = {"temp":"pagestr.html","lst":NumberPage(a, offset,"search_%s" % text)}

    load_css = ["main_temp.css","header.css","products_list.css","bottom_part.css","pagestr.css"]
    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = "Результаты поиска"
    
    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,
        "products":current_cat, "Teg_a_sp":Teg_a_sp, "notempty": len_sp != 0,
        "add_page_content":[]} 
    
    return render_to_response('products_list.html',Tabs)


@csrf_exempt
def promotion(request, offset=1):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    max_categories = 20
    

    cat = Products.objects.filter(promotion=True)
    len_sp = cat.count()
    
    current_cat = cat[(offset-1)*max_categories:offset*max_categories]

    a = len_sp // max_categories +1 if len_sp % max_categories > 0 else len_sp // max_categories
    if len_sp != 0:
        if offset > a: raise Http404
    
    Teg_a_sp = {"temp":"pagestr.html","lst":NumberPage(a, offset,"promotion")}

    load_css = ["main_temp.css","header.css","products_list.css",
        "bottom_part.css","pagestr.css","promotion.css"]

    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    add_page_content = ["promotion.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = "Акции"
    
    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,
        "products":current_cat, "Teg_a_sp":Teg_a_sp, "notempty": len_sp != 0,
        "add_page_content":add_page_content} 
    
    return render_to_response('products_list.html',Tabs)

@csrf_exempt
def product_item(request, name):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    try:
        prd = Products.objects.get(id=name)
    except Products.DoesNotExist:
        raise Http404
    except Products.MultipleObjectsReturned:
        prd = Products.objects.filter(id=name)[0]
    

    load_css = ["main_temp.css","header.css","product_item.css",
        "bottom_part.css"]

    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = prd.name
    
    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,
        "productinfo":prd, "productdescribe":prd.description.split("\n")} 
    
    return render_to_response('product_item.html',Tabs)

@csrf_exempt
def articles_list(request, offset=1):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    max_categories = 8
    

    cat = Articles.objects.all()
    len_sp = cat.count()
    
    current_cat = cat[(offset-1)*max_categories:offset*max_categories]

    a = len_sp // max_categories +1 if len_sp % max_categories > 0 else len_sp // max_categories
    if len_sp != 0:
        if offset > a: raise Http404
    
    Teg_a_sp = {"temp":"pagestr.html","lst":NumberPage(a, offset,"articles")}

    load_css = ["main_temp.css","header.css","articles_list.css","bottom_part.css","pagestr.css"]
    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = "Статьи"
    
    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,
        "articles":current_cat, "Teg_a_sp":Teg_a_sp,
        } 
    
    return render_to_response('articles_list.html',Tabs)

@csrf_exempt
def article_item(request, name):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    try:
        prd = Articles.objects.get(id=name)
    except Products.DoesNotExist:
        raise Http404
    except Articles.MultipleObjectsReturned:
        prd = Products.objects.filter(id=name)[0]
    

    load_css = ["main_temp.css","header.css","article_item.css",
        "bottom_part.css"]

    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = prd.name

    lst = prd.description.split("\n")
    new_lst = []
    for i in lst:
        if i[:10]=="<imgPath>:":
            new_lst.append({"is_path":True,"value":i.lstrip("<imgPath>:").strip("\n").strip("\r")})
        else:
            new_lst.append({"is_path":False,"value":i})


    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,
        "articledescribe":new_lst} 
    
    return render_to_response('article_item.html',Tabs)

@csrf_exempt
def company(request):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]

    load_css = ["main_temp.css","header.css","company.css",
        "bottom_part.css"]

    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = "О компании"

    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,} 
    
    return render_to_response('company.html',Tabs)

@csrf_exempt
def ShippingPayment(request):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]
    #shipping_and_payment
    load_css = ["main_temp.css","header.css","shipping_and_payment.css",
        "bottom_part.css"]

    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = "Доставка и оплата"

    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False, "after_page_parts":after_page_parts,} 
    
    return render_to_response('shipping_and_payment.html',Tabs)

@csrf_exempt
def contacts(request):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]
    
    load_css = ["main_temp.css","header.css","contacts.css",
        "bottom_part.css"]

    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = "Контактные данные"

    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": True, "slider":False, "api_key":api_key, "after_page_parts":after_page_parts,} 
    
    return render_to_response('contacts.html',Tabs)

@csrf_exempt
def reviews(request):
    
    s_pan = search_panel(request)
    if s_pan["type"] == "redirect":
        return s_pan["value"]
    elif s_pan["type"] == "form":
        form = s_pan["value"]
    
    load_css = ["main_temp.css","header.css","reviews.css",
        "bottom_part.css"]

    load_css = ccs_load_convector(load_css)
    before_page_parts = ["header.html"]
    after_page_parts = ["bottom_part.html"]
    title_name = "Отзывы"

    Tabs = {'template':'main_temp.html','title':title_name,
        "load_css":load_css, "before_page_parts": before_page_parts,
        'form':form, "map": False, "slider":False,  "after_page_parts":after_page_parts,
        "imgviewer":True} 
    
    return render_to_response('reviews.html',Tabs)

def search_panel(request):
    if request.method == 'POST':
        form = Search_form(request.POST)
        if  form.is_valid():
            cd = form.cleaned_data
            #print(cd['search'])
            return {"type":"redirect","value": HttpResponseRedirect('/search_%s/' % cd['search'])}
    
    else:
        form = Search_form(initial={'search':''})

    return {"type":"form","value": form}



def NumberPage(len_sp, offset, link):
    # Составляет список ссылок для организации многостраничной структуры
    Teg_a_sp = []
    if len_sp == 1:
        return Teg_a_sp

    if 1 < len_sp and offset != 1:
        Teg_a_sp.append(["/%s/%s/" % (link,str(offset-1)), "", "previous"])
    
    if 1 < len_sp <= 12:
        for i in range(len_sp):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])

    elif offset < 6 :
        for i in range(offset+2):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])
        Teg_a_sp.append(["..."])
        for i in range(len_sp-2,len_sp):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])

    elif len_sp-offset <6:
        for i in range(2):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])
        Teg_a_sp.append(["..."])
        for i in range(offset-3,len_sp):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])

    elif offset >= 6 and len_sp-offset >=6:
        for i in range(2):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])
        Teg_a_sp.append(["..."])
        for i in range(offset-3,offset+2):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])
        Teg_a_sp.append(["..."])
        for i in range(len_sp-2,len_sp):
            Teg_a_sp.append(["/%s/%s/" % (link,str(i+1)), str(i+1), "pagenow" if offset == i+1 else "page"])

    if 1 < len_sp and offset != len_sp:
        Teg_a_sp.append(["/%s/%s/" % (link,str(offset+1)), "", "next"])

    #print(Teg_a_sp)
    
    return Teg_a_sp



