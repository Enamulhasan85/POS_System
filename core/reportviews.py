from sqlite3 import Timestamp
from unicodedata import category, name
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.db.models import F
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
def purchaseSummary(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # pass the object as instance in form
    form = PurchaseSummaryForm(request.POST or None)
    
    if request.method == "POST":
        # add the dictionary during initialization
        ToDate = datetime.datetime.strptime(request.POST.get("ToDate"), "%Y-%m-%d") + datetime.timedelta(days=1)
        FromDate = datetime.datetime.strptime(request.POST.get("FromDate"), "%Y-%m-%d")
        
        purchaseSummary = Purchase.objects.filter(entryDate__gte=FromDate, 
                                                  entryDate__lt=ToDate)
                                           
        if request.POST.get("supplier") != "":
            print(request.POST.get("supplier")) 
            purchaseSummary = purchaseSummary.filter(supplier=request.POST.get("supplier"))
        
        if request.POST.get("company") != "":
            print(request.POST.get("company")) 
            purchaseSummary = purchaseSummary.filter(company=request.POST.get("company"))
        
        
        purchaseSummary = purchaseSummary.values("supplier").annotate(
                                        totalPrice=Sum("totalPrice"), 
                                        supplierName=F('supplier__name'), 
                                        supplierAddress=F('supplier__address'), 
                                        supplierContact=F('supplier__contact')
                                        ).order_by("supplierName")

        
        context["dataset"] = purchaseSummary
    
    context['purchaseSummaryForm'] = form
         
    return render(request, "report/purchaseSummary.html", context) 



@allowed_users(allowed_roles=['admin', 'operator'])
def productInStock(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # pass the object as instance in form
    form = ProductInStockForm(request.POST or None)
    
    if request.method == "POST":
        # add the dictionary during initialization
        ToDate = datetime.datetime.strptime(request.POST.get("ToDate"), "%Y-%m-%d") + datetime.timedelta(days=1)
        FromDate = datetime.datetime.strptime(request.POST.get("FromDate"), "%Y-%m-%d")
        
        productInStock = Stock.objects.filter(entryDate__gte=FromDate, 
                                                  entryDate__lt=ToDate, )
        
        if request.POST.get("product") != "":
            print(request.POST.get("product")) 
            productInStock = productInStock.filter(product=request.POST.get("product"))
            
        if request.POST.get("productCode") != "":
            print(request.POST.get("productCode")) 
            productInStock = productInStock.filter(product__productCode=request.POST.get("productCode"))
            
        if request.POST.get("category") != "":
            print(request.POST.get("category")) 
            productInStock = productInStock.filter(product__category=request.POST.get("category"))
        
        if request.POST.get("company") != "":
            print(request.POST.get("company")) 
            productInStock = productInStock.filter(product__company=request.POST.get("company"))
        
        # print(productInStock)
        
        productInStock = productInStock.values("product").annotate(
                                        productQuantity=Sum("quantity"), 
                                        productSold=Sum("sold"), 
                                        inStock=Sum("quantity")-Sum("sold"), 
                                        productCompanyId=F('product__company'), 
                                        productCategoryId=F('product__category'),
                                        productTitle=F('product__title'), 
                                        productCode=F('product__productCode')
                                        ).order_by("productTitle")
        
        for productStock in productInStock:
            print(productStock['productCompanyId'])
            productStock['productCompany'] = Company.objects.get(id=productStock['productCompanyId']).name
            productStock['productCategory'] = Category.objects.get(id=productStock['productCategoryId']).title
            productStock['unitPrice'] = Stock.objects.filter(product=productStock['product']).order_by("-id")[0].salePrice
            productStock['stockValue'] = productStock['inStock'] * productStock['unitPrice']
        
        context["dataset"] = productInStock
    
    context['productInStockForm'] = form
         
    return render(request, "report/productInStock.html", context) 



@allowed_users(allowed_roles=['admin', 'operator'])
def salesSummary(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # pass the object as instance in form
    form = SalesSummaryForm(request.POST or None)
    
    if request.method == "POST":
        # add the dictionary during initialization
        ToDate = datetime.datetime.strptime(request.POST.get("ToDate"), "%Y-%m-%d") + datetime.timedelta(days=1)
        FromDate = datetime.datetime.strptime(request.POST.get("FromDate"), "%Y-%m-%d")
        
        reportItems = Sale.objects.filter(date__gte=FromDate, date__lt=ToDate, )
        
        if request.POST.get("user") != "":
            print(request.POST.get("user")) 
            reportItems = reportItems.filter(user=request.POST.get("user"))
            
        if request.POST.get("customer") != "":
            print(request.POST.get("customer")) 
            reportItems = reportItems.filter(customer=request.POST.get("customer"))
           
        print(reportItems)
        
        reportItems = reportItems.values("user").annotate(
                                        salesTotal=Sum("totalPrice"), 
                                        discountGiven=Sum("discountAmount"), 
                                        collectedAmount=Sum("paidAmount")-Sum("changeAmount"), 
                                        dueGiven=Sum("totalPrice")-Sum("discountAmount")-Sum("paidAmount")+Sum("changeAmount"), 
                                        userName=F('user__username'), 
                                        first_name=F('user__first_name'), 
                                        last_name=F('user__last_name'), 
                                        )
        
        for reportItem in reportItems:
            print(reportItem)
            
            dueCollection = DueCollection.objects.filter(user=reportItem['user'], 
                                                date__gte=FromDate, date__lt=ToDate,).values("user").annotate(
                                                dueCollection=Sum("amount"),
                                                )[0]
            
            reportItem['dueCollection'] = dueCollection['dueCollection']
            
            
            refunds = Refund.objects.filter(user=reportItem['user'], 
                                date__gte=FromDate, date__lt=ToDate,).values("user").annotate(
                                refundedAmount=Sum("totalRefund"),
                                dueRefundedAmount=Sum("dueRefund"),
                                )[0]
                
            reportItem['refundedAmount'] = refunds["refundedAmount"]
                           
            reportItem['dueRefundedAmount'] = refunds["dueRefundedAmount"]
        
        context["dataset"] = reportItems
    
    context['reportform'] = form
         
    return render(request, "report/salesSummary.html", context) 



@allowed_users(allowed_roles=['admin', 'operator'])
def salesByCustomer(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # pass the object as instance in form
    form = SalesByCustomerForm(request.POST or None)
    
    if request.method == "POST":
        # add the dictionary during initialization
        ToDate = datetime.datetime.strptime(request.POST.get("ToDate"), "%Y-%m-%d") + datetime.timedelta(days=1)
        FromDate = datetime.datetime.strptime(request.POST.get("FromDate"), "%Y-%m-%d")
        
        reportItems = Sale.objects.filter(date__gte=FromDate, date__lt=ToDate, )
        
        if request.POST.get("customer") != "":
            print(request.POST.get("customer")) 
            reportItems = reportItems.filter(customer=request.POST.get("customer"))
           
        print(reportItems)
        
        reportItems = reportItems.values("customer").annotate(
                                        total=Sum("totalPrice"), 
                                        discount=Sum("discountAmount"), 
                                        paid=Sum("paidAmount")-Sum("changeAmount"), 
                                        due=Sum("totalPrice")-Sum("discountAmount")-Sum("paidAmount")+Sum("changeAmount"), 
                                        customerName=F('customer__name'), 
                                        )
        
        for reportItem in reportItems:
            print(reportItem)
            
            dueGiven = DueCollection.objects.filter(due__customer_id=reportItem['customer'], 
                                                date__gte=FromDate, date__lt=ToDate,).values("due__customer_id").annotate(
                                                dueGiven=Sum("amount"),
                                                )[0]
            
            reportItem['dueGiven'] = dueGiven['dueGiven']
            
            
            refunds = Refund.objects.filter(sale__customer_id=reportItem['customer'], 
                                date__gte=FromDate, date__lt=ToDate,).values("sale__customer_id").annotate(
                                refundedAmount=Sum("totalRefund"),
                                dueRefundedAmount=Sum("dueRefund"),
                                )[0]
                
            reportItem['refundedAmount'] = refunds["refundedAmount"]
                           
            reportItem['dueRefundedAmount'] = refunds["dueRefundedAmount"]
            
            reportItem['dueReceivable'] = reportItem['due'] - reportItem['dueGiven'] - reportItem['dueRefundedAmount']
        
        context["dataset"] = reportItems
    
    context['reportform'] = form
         
    return render(request, "report/salesByCustomer.html", context) 
