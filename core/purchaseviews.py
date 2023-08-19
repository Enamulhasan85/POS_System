from sqlite3 import Timestamp
from unicodedata import category, name
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.contrib import messages
from django.http import HttpResponseRedirect
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
import json
 
 
@allowed_users(allowed_roles=['admin', 'operator'])
def purchaselist(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    context["dataset"] = Purchase.objects.all()
         
    return render(request, "purchase/index.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def createpurchase(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method == "POST":
        purchase = Purchase()
        
        data = request.POST.getlist("purchaseProducts[]")
        # print(data)
        # data = json.loads(request.POST.getlist("purchaseProducts[]")[1])
        # print(data)
        
        purchase.user = request.user
        purchase.company = Company.objects.get(id=request.POST.get("company"))
        purchase.supplier = Supplier.objects.get(id=request.POST.get("supplier"))
        purchase.invoice = request.POST.get("invoice")
        purchase.totalPrice = request.POST.get("totalPurchasePrice")
        purchase.note = request.POST.get("note")
        purchase.entryDate = datetime.datetime.now()
        purchase.save()
        
        for product in request.POST.getlist("purchaseProducts[]"):
            product = json.loads(product)
            # print(product)
            purchase_detail = PurchaseDetail(quantity=product["quantity"], tradePrice=product["tradePrice"], totalPrice=product["totalPrice"],)
            purchase_detail.product = Product.objects.get(id=product["product"])
            purchase_detail.purchase = purchase
            purchase_detail.save()
            
            stock = Stock()
            stock.user = request.user
            stock.product = purchase_detail.product
            stock.purchase = purchase
            stock.purchasedetail = purchase_detail
            stock.quantity = purchase_detail.quantity
            stock.tradePrice = purchase_detail.tradePrice
            stock.salePrice = product["salePrice"]
            stock.mrp = product["mrp"]
            stock.entryDate = datetime.datetime.now()
            stock.manufacturingDate = product["manufacturingDate"]
            stock.expirationDate = product["expirationDate"]
            stock.save()

            # send to client side.
        
        return JsonResponse({"res": "complete"}, status=200)
    else:
        form = PurchaseForm()
        
    form = PurchaseForm()
    form.fields["note"].widget.attrs['rows'] = '3'
         
    context['purchaseform'] = form
    context['purchasedetailform'] = PurchaseDetailForm()
         
    return render(request, "purchase/create.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def editpurchase(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method == "POST":
        purchase = Purchase.objects.get(id=id)
        
        data = request.POST.getlist("purchaseProducts[]")
        # print(data)
        
        purchase.company = Company.objects.get(id=request.POST.get("company"))
        purchase.supplier = Supplier.objects.get(id=request.POST.get("supplier"))
        purchase.invoice = request.POST.get("invoice")
        purchase.totalPrice = request.POST.get("totalPurchasePrice")
        purchase.note = request.POST.get("note")
        purchase.save()
        
        PurchaseDetail.objects.filter(purchase=purchase).delete()
        Stock.objects.filter(purchase=purchase).delete()
        
        for product in request.POST.getlist("purchaseProducts[]"):
            product = json.loads(product)
            # print(product)
            purchase_detail = PurchaseDetail(quantity=product["quantity"], tradePrice=product["tradePrice"], totalPrice=product["totalPrice"],)
            purchase_detail.product = Product.objects.get(id=product["product"])
            purchase_detail.purchase = purchase
            purchase_detail.save()
            
            stock = Stock()
            stock.user = request.user
            stock.product = purchase_detail.product
            stock.purchase = purchase
            stock.purchasedetail = purchase_detail
            stock.quantity = purchase_detail.quantity
            stock.tradePrice = purchase_detail.tradePrice
            stock.salePrice = product["salePrice"]
            stock.mrp = product["mrp"]
            stock.entryDate = purchase.entryDate
            stock.manufacturingDate = product["manufacturingDate"]
            stock.expirationDate = product["expirationDate"]
            stock.save()

            # send to client side.
        
        return JsonResponse({"res": "complete"}, status=200)
        
    
    purchase = Purchase.objects.get(id=id)
    form = PurchaseForm(instance = purchase)
    form.fields["note"].widget.attrs['rows'] = '3'
         
    context['purchaseform'] = form
    context['purchasedetailform'] = PurchaseDetailForm()
    
    context['purchase'] = purchase
    
    purchasedetails = PurchaseDetail.objects.filter(purchase=purchase)
    for purchasedetail in purchasedetails:
        stock = Stock.objects.filter(purchasedetail=purchasedetail).first()
        stock.manufacturingDate = stock.manufacturingDate.strftime('%Y-%m-%d')
        stock.expirationDate = stock.expirationDate.strftime('%Y-%m-%d')
        purchasedetail.stock = stock
    
    context['purchasedetails'] = purchasedetails
         
    return render(request, "purchase/edit.html", context)


@allowed_users(allowed_roles=['admin'])
def deletepurchase(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Purchase, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("purchaselist")
 