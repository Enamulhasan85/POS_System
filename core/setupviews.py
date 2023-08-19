from sqlite3 import Timestamp
from unicodedata import category, name
from django.shortcuts import render, redirect
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from .models import *
from .forms import *
from .decorators import *
import datetime
import random
import string
import json



@allowed_users(allowed_roles=['admin', 'operator'])
def companylist(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Company.objects.all()
         
    return render(request, "company/index.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def createcompany(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("companylist")
        
         
    context['form']= form
         
    return render(request, "company/create.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def editcompany(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Company, id = id)
 
    # pass the object as instance in form
    form = CompanyForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to companylist
    if form.is_valid():
        form.save()
        return redirect("companylist")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "company/edit.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def deletecompany(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Company, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("companylist")
 

@allowed_users(allowed_roles=['admin', 'operator'])
def supplierlist(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Supplier.objects.all()
         
    return render(request, "supplier/index.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def createsupplier(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("supplierlist")
        
         
    context['form']= form
         
    return render(request, "supplier/create.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def editsupplier(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Supplier, id = id)
 
    # pass the object as instance in form
    form = SupplierForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to supplierlist
    if form.is_valid():
        form.save()
        return redirect("supplierlist")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "supplier/edit.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def deletesupplier(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Supplier, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("supplierlist")
 
 
 
@allowed_users(allowed_roles=['admin', 'operator'])
def customerlist(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Customer.objects.all()
         
    return render(request, "customer/index.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def createcustomer(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("customerlist")
        
         
    context['form']= form
         
    return render(request, "customer/create.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def editcustomer(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    
    # fetch the object related to passed id
    obj = get_object_or_404(Customer, id = id)
 
    # pass the object as instance in form
    form = CustomerForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to customerlist
    if form.is_valid():
        form.save()
        return redirect("customerlist")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "customer/edit.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def deletecustomer(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Customer, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("customerlist")
    
    
    

@allowed_users(allowed_roles=['admin', 'operator'])
def categorylist(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Category.objects.all()
         
    return render(request, "category/index.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def createcategory(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("categorylist")
        
         
    context['form']= form
         
    return render(request, "category/create.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def editcategory(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    
    # fetch the object related to passed id
    obj = get_object_or_404(Category, id = id)
 
    # pass the object as instance in form
    form = CategoryForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to categorylist
    if form.is_valid():
        form.save()
        return redirect("categorylist")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "category/edit.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def deletecategory(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Category, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("categorylist")
    
    
@allowed_users(allowed_roles=['admin', 'operator'])
def productlist(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    context["dataset"] = Product.objects.all()
         
    return render(request, "product/index.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def createproduct(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("productlist")
    else:
        form = ProductForm()
         
    context['form'] = form
         
    return render(request, "product/create.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def editproduct(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
 
    # pass the object as instance in form
    form = ProductForm(request.POST  or None, instance = obj)
    
    # save the data from the form and
    # redirect to productlist
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance = obj)
        if form.is_valid():
            form.save()
            return redirect("productlist")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "product/edit.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def deleteproduct(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Product, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("productlist")
    
    
@allowed_users(allowed_roles=['admin', 'operator'])
def getproduct(request):
    # dictionary for initial data with
    # field names as keys
    data = []
    products = Product.objects.all().order_by('title')

    companyid = request.GET.get('companyid')
    categoryid = request.GET.get('categoryid')
    
    if companyid != '':
        company = Company.objects.get(id=companyid)    
        products = products.filter(company=company)

        
    if categoryid != '':
        category = Category.objects.get(id=categoryid) 
        products = products.filter(category=category)
                    
    
    for product in products:
        str = product.title + " (" + product.productCode + ")"
        data.append({'id':product.id, 'title': str})
    
    return JsonResponse({'productlist': data}, status=200, content_type="application/json")
 
    
@allowed_users(allowed_roles=['admin', 'operator'])
def getproductinfo(request):
    # dictionary for initial data with
    # field names as keys
    productid = request.GET.get('productid')
    
    product = Product.objects.get(id=productid)
    
    if Stock.objects.filter(product=product).count():
        lateststock = Stock.objects.filter(product=product).order_by("-id")[:1].get()
        unitPrice = lateststock.salePrice
        discount = lateststock.discount    
        inStock = Stock.objects.filter(product=product).aggregate(inStock = Sum("quantity") - Sum("sold"))
        inStock = inStock["inStock"]
    else :
        unitPrice = 0
        discount = 0
        inStock = 0
    
    unit = product.get_unit_display()
    
    data = {'id': product.id, 'inStock': inStock, 'unitPrice': unitPrice, 'discount': discount, 'unit': unit}
    
    return JsonResponse({'productinfo': data}, status=200, content_type="application/json")
 