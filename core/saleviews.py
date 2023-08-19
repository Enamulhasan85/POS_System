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
def salelist(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    context["dataset"] = Sale.objects.all()
         
    return render(request, "sale/index.html", context) 


@allowed_users(allowed_roles=['admin', 'operator'])
def createsale(request):
     # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method == "POST":
        data = request.POST.getlist("saleProducts[]")
        print(data)
        # data = json.loads(request.POST.getlist("purchaseProducts[]")[1])
        # print(data)
        
        sale = Sale()
        sale.user = request.user
        if request.POST.get("customer") != '':
            sale.customer = Customer.objects.get(id=request.POST.get("customer"))
        sale.saleStripeId = request.POST.get("saleStripeId")
        sale.date = datetime.datetime.now()
        sale.totalPrice = request.POST.get("totalPrice")
        sale.discountAmount = request.POST.get("discount")
        sale.paidAmount = request.POST.get("paid")
        sale.changeAmount = request.POST.get("change")
        if request.POST.get("due") != '0':
            sale.status = 'due'
        else :
            sale.status = 'paid'
        sale.note = request.POST.get("note")
        sale.save()
        
        if sale.status != 'paid':
            due = Due()
            due.sale = sale
            due.customer = sale.customer
            due.dueAmount = request.POST.get("due")
            due.date = datetime.datetime.now()
            due.save()
                    
        for product in request.POST.getlist("saleProducts[]"):
            product = json.loads(product)
            # print(product)
            sale_detail = SaleDetail(quantity=product["quantity"], unitPrice=product["unitPrice"], discount=product["ProductDiscount"], totalPrice=product["totalPrice"],)
            sale_detail.product = Product.objects.get(id=product["product"])
            sale_detail.sale = sale
            sale_detail.save()
            
            stocklist = Stock.objects.filter(product=sale_detail.product).filter(sold__lt=F("quantity")).order_by('id')
            for stock in stocklist:
                instock = stock.quantity - stock.sold
                if instock >= int(sale_detail.quantity):
                    stock.sold += int(sale_detail.quantity)
                    sale_detail.quantity = 0
                else:
                    sale_detail.quantity = int(sale_detail.quantity) - instock
                    stock.sold = stock.quantity
                
                stock.save()
                
                if sale_detail.quantity == 0:
                    break

            # send to client side.
        
        return JsonResponse({"res": "complete"}, status=200)
    else:
        form = SaleForm()
        
    form = SaleForm()
    form.fields["note"].widget.attrs['rows'] = '3'
    
    # form.company = Company.objects.all()    
    # form.category = Category.objects.all()    
         
    context['saleform'] = form
    context['saledetailform'] = SaleDetailForm()
         
    return render(request, "sale/create.html", context)



@allowed_users(allowed_roles=['admin', 'operator'])
def refundsale(request, id):
     # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method == "POST":
        refund = Refund()
        refund.user = request.user
        refund.sale = Sale.objects.get(id=request.POST.get("sale"))
        refund.saleDetail = SaleDetail.objects.get(id=request.POST.get("saleDetailId"))
        refund.quantity = request.POST.get("quantity")
        refund.unitPrice = request.POST.get("unitPrice")
        refund.totalRefund = request.POST.get("totalRefund")
        refund.dueRefund = request.POST.get("due")
        refund.date = datetime.datetime.now()
        refund.note = request.POST.get("note")
        refund.save()
        
        product = Product.objects.get(id = request.POST.get("productid"))
        stocks = Stock.objects.filter(product = product)
        
        refundquantity = int(refund.quantity)
        for stock in stocks:
            productrefunded = min(stock.sold, refundquantity)
            stock.sold -= productrefunded
            stock.save()
            refundquantity -= productrefunded
            
            if refundquantity == 0:
                break
        
        sale = Sale.objects.get(id=request.POST.get("sale"))
        salestatus = sale.status
        sale.status = 'refund'
        sale.customer = Customer.objects.get(id=request.POST.get("customer"))
        saleDetails = SaleDetail.objects.filter(sale = sale)
        for saleDetail in saleDetails:
            refunds = Refund.objects.filter(saleDetail = saleDetail).aggregate(quantity = Sum("quantity"))["quantity"]
            
            if refunds != saleDetail.quantity:
                sale.status = salestatus
                break
        
        sale.save()
       
    
    sale = Sale.objects.get(id=id)
    
    form = SaleForm(instance = sale)
    form.fields["saleStripeId"].widget.attrs['disabled'] = 'true'
    form.fields["date"].widget.attrs['disabled'] = 'true'
    form.fields["totalPrice"].widget.attrs['disabled'] = 'true'
    form.fields["discountAmount"].widget.attrs['disabled'] = 'true'
    form.fields["paidAmount"].widget.attrs['disabled'] = 'true'
    form.fields["note"].widget.attrs['disabled'] = 'true'
    form.fields["note"].widget.attrs['rows'] = '2'
    
    context['sale'] = sale
    context['saleform'] = form
    
    salerefunds = Refund.objects.filter(sale=sale)

    if salerefunds.count() == 0:
        totalrefund = 0
        dueRefund = 0
    else:
        totalrefund = salerefunds.aggregate(totalrefund = Sum("totalRefund"))["totalrefund"]
        dueRefund = salerefunds.aggregate(dueRefund = Sum("dueRefund"))["dueRefund"]
        
    try:
        due = Due.objects.get(sale=sale)
    except Due.DoesNotExist:
        due = None
        
    duecollections = DueCollection.objects.filter(due=due)
    context["duecollections"] = duecollections
    
    if duecollections.count() == 0:
        duecollect = 0
    else:
        duecollect = duecollections.aggregate(duecollection = Sum("amount"))["duecollection"]
    
    refundform = RefundForm()
    refundform.fields["totalRefund"].widget.attrs['max'] = sale.paidAmount - totalrefund + duecollect
    refundform.fields["due"].widget.attrs['max'] = sale.get_dueAmount() - dueRefund - duecollect
    refundform.fields["note"].widget.attrs['rows'] = '2'
    
    context['refundform'] = refundform
    
    saledetails = SaleDetail.objects.filter(sale=sale)
    for saledetail in saledetails:
        refunds = Refund.objects.filter(saleDetail=saledetail)
        if refunds.count() == 0:
            saledetail.refunded = 0
        else:
            refunded = refunds.aggregate(refunded = Sum("quantity"))
            saledetail.refunded = refunded["refunded"]
    
    context['saledetails'] = saledetails
    context['salerefunds'] = salerefunds
    context['totalRefund'] = totalrefund
    context['totalDueRefund'] = dueRefund
    context['totalDueCollected'] = duecollect
         
    return render(request, "sale/refund.html", context)


@allowed_users(allowed_roles=['admin'])
def deletesale(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Sale, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("salelist") 
    
    
@allowed_users(allowed_roles=['admin', 'operator'])
def duelist(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    dues = Due.objects.all()
    
    for due in dues:
        if DueCollection.objects.filter(due = due).count() == 0:
            due.collectedAmount = 0
        else:
            due.collectedAmount = DueCollection.objects.filter(due = due).aggregate(duecollection = Sum("amount"))["duecollection"]
             
        if Refund.objects.filter(sale = due.sale).count() == 0:
            due.refundedAmount = 0
        else:
            due.refundedAmount = Refund.objects.filter(sale = due.sale).aggregate(dueRefund = Sum("dueRefund"))["dueRefund"]
               
    context["dataset"] = dues
    
    return render(request, "due/index.html", context) 


    
@allowed_users(allowed_roles=['admin', 'operator'])
def duecollection(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    due = Due.objects.get(id=id)
    
    if request.method == "POST":
        duecollection = DueCollection()
        duecollection.due = due
        duecollection.user = request.user
        duecollection.amount = request.POST.get("amount")
        duecollection.date = datetime.datetime.now()
        duecollection.note = request.POST.get("note")
        duecollection.save()
        
    
    if DueCollection.objects.filter(due = due).count() == 0:
        due.collectedAmount = 0
    else:
        due.collectedAmount = DueCollection.objects.filter(due = due).aggregate(duecollection = Sum("amount"))["duecollection"]
            
    if Refund.objects.filter(sale = due.sale).count() == 0:
        due.refundedAmount = 0
    else:
        due.refundedAmount = Refund.objects.filter(sale = due.sale).aggregate(dueRefund = Sum("dueRefund"))["dueRefund"]
               
    context["due"] = due
    context["duecollections"] = DueCollection.objects.filter(due=due)
    context["collectedAmount"] = due.collectedAmount
    context["refundedAmount"] = due.refundedAmount
    
    sale = due.sale
    
    form = SaleForm(instance = sale)
    form.fields["customer"].widget.attrs['disabled'] = 'true'
    form.fields["saleStripeId"].widget.attrs['disabled'] = 'true'
    form.fields["date"].widget.attrs['disabled'] = 'true'
    form.fields["totalPrice"].widget.attrs['disabled'] = 'true'
    form.fields["discountAmount"].widget.attrs['disabled'] = 'true'
    form.fields["paidAmount"].widget.attrs['disabled'] = 'true'
    form.fields["note"].widget.attrs['disabled'] = 'true'
    form.fields["note"].widget.attrs['rows'] = '2'
    
    context['sale'] = sale
    context['saleform'] = form
    
    duecollectionform = DueCollectionForm()
    duecollectionform.fields["amount"].widget.attrs['max'] = sale.get_dueAmount() - due.collectedAmount - due.refundedAmount
    duecollectionform.fields["note"].widget.attrs['rows'] = '1'
    
    context['duecollectionform'] = duecollectionform
    
    salerefunds = Refund.objects.filter(sale=sale)
    
    saledetails = SaleDetail.objects.filter(sale=sale)
    for saledetail in saledetails:
        refunds = Refund.objects.filter(saleDetail=saledetail)
        if refunds.count() == 0:
            saledetail.refunded = 0
        else:
            refunded = refunds.aggregate(refunded = Sum("quantity"))
            saledetail.refunded = refunded["refunded"]
    
    context['saledetails'] = saledetails
    context['salerefunds'] = salerefunds
    context['totalRefund'] = salerefunds.aggregate(totalRefund = Sum("totalRefund"))["totalRefund"]
    context['totalDueRefund'] = due.refundedAmount
    
    return render(request, "due/duecollection.html", context) 