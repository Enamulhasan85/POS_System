from django import forms
from django.forms import ModelChoiceField
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
import datetime


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
 
      
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", 'password']
        widgets = {
            "username": forms.TextInput(attrs={}),
            "password": forms.TextInput(attrs={'type': 'password'}),
        }
        
        
class UserGroupForm(UserCreationForm):
        id = forms.IntegerField()
        username = forms.CharField(max_length=150)
        first_name = forms.CharField(max_length=150)
        last_name = forms.CharField(max_length=150)
        email = forms.EmailField()
        is_active = models.BooleanField(default=True)
        user = User()
        group = Group()
        

class CompanyForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Company
 
        # specify fields to be used
        fields = [
            "name",
            "address",
            "contact",
        ]
        
        
class SupplierForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = Supplier

        # specify fields to be used
        fields = [
            "name",
            "address",
            "contact",
        ]
        
        
class CustomerForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Customer
 
        # specify fields to be used
        fields = [
            "name",
            "address",
            "contact",
        ]
        
        
class CategoryForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Category
 
        # specify fields to be used
        fields = [
            "title",
            "code",
        ]
        

class ProductForm(forms.ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Product
 
        # specify fields to be used
        fields = [
            "title",
            "company",
            "productCode",
            "category",
            "unit",
            "lowStockLimit",
            "image",
            "description",
        ]
        

class PurchaseForm(forms.ModelForm):
        
    # create meta class
    class Meta:
        # specify model to be used
        model = Purchase
        
        # specify fields to be used
        fields = [
            "company",
            "supplier",
            "invoice",
            "totalPrice",
            "note",
        ]
        widgets = {
            "company": forms.Select(attrs={'required': 'true', }),
            "totalPrice": forms.NumberInput(attrs={'id': 'totalPurchasePrice', 'min': '0', 'value': '0'}),
        }
        
        
class PurchaseDetailForm(forms.ModelForm):
    manufacturingDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm'},))
    expirationDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm'},))
    mrp = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0'},))
    salePrice = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0'},))

    # create meta class
    class Meta:
        # specify model to be used
        model = PurchaseDetail
        
        # specify fields to be used
        fields = [
            "product",
            "tradePrice",
            "quantity",
            "totalPrice",
        ]
        widgets = {
            "product": forms.Select(attrs={"class": 'form-select-sm'}),
            "tradePrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "quantity": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "totalPrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
        }

        
class StockForm(forms.ModelForm):
        
    # create meta class
    class Meta:
        # specify model to be used
        model = Stock
        
        # specify fields to be used
        fields = [
            "user",
            "product",
            "quantity",
            "tradePrice",
            "salePrice",
            "mrp",
            "discount",
            "entryDate",
            "manufacturingDate",
            "expirationDate",
        ]
        widgets = {
            "user": forms.Select(attrs={"class": 'form-select-sm', "disabled": "true"}),
            "product": forms.Select(attrs={"class": 'form-select-sm', "disabled": "true"}),
            "quantity": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0', "disabled": "true"}),
            "tradePrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "salePrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "mrp": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "discount": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "entryDate": forms.DateTimeInput(attrs={"class": 'form-control-sm', 'type':'datetime-local', "disabled": "true"}),
            "manufacturingDate": forms.TextInput(attrs={"class": 'form-control-sm', 'type':'date', "disabled": "true"}),
            "expirationDate": forms.TextInput(attrs={"class": 'form-control-sm', 'type':'date'}),
        }    
        labels = {
            "discount": "ProductDiscount(%)",
        }
        
        
class SaleForm(forms.ModelForm):
    payable = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0', 'value': '0', "disabled": "true"},))
    due = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0', 'value': '0', "disabled": "true"},))

    # create meta class
    class Meta:
        # specify model to be used
        model = Sale
        
        # specify fields to be used
        fields = [
            "customer",
            "saleStripeId",
            "date",
            "totalPrice",
            "discountAmount",
            "paidAmount",
            "changeAmount",
            "status",
            "note",
        ]
        widgets = {
            "customer": forms.Select(attrs={"class": 'form-select-sm'}),
            "saleStripeId": forms.TextInput(attrs={"class": 'form-select-sm', 'required': "true"}),
            "totalPrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0', 'value': '0', "disabled": "true"}),
            "discountAmount": forms.NumberInput(attrs={"class": 'form-control-sm', 'id': 'id_discount',  'min': '0', 'value': '0'}),
            "paidAmount": forms.NumberInput(attrs={"class": 'form-control-sm', 'id': 'id_paid', 'min': '0', 'value': '0'}),
            "changeAmount": forms.NumberInput(attrs={"class": 'form-control-sm', 'id': 'id_change', 'min': '0', 'value': '0', "disabled": "true"}),
            "status": forms.Select(attrs={"class": 'form-select-sm'}),
            "date": forms.TextInput(attrs={"class": 'form-control-sm', 'type':'date'}),
        }
        labels = {
            "discountAmount": "Discount",
            "paidAmount": "Paid",
            "changeAmount": "Change",
        }
        
          
class SaleDetailForm(forms.ModelForm):
    company = ModelChoiceField(queryset=Company.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    category = ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    inStock = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0', 'disabled': 'true'},))
    
    # create meta class
    class Meta:
        # specify model to be used
        model = SaleDetail
        
        # specify fields to be used
        fields = [
            "product",
            "quantity",
            "unitPrice",
            "discount",
            "totalPrice",
        ]
        widgets = {
            "product": forms.Select(attrs={"class": 'form-select-sm'}),
            "quantity": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "unitPrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0', 'disabled': 'true'}),
            "discount": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0', "id": 'ProductDiscount', 'disabled': 'true'}),
            "totalPrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0', "id": 'totalProductPrice', "disabled": "true"}),
        }
        labels = {
            "discount": "ProductDiscount(%)",
            "totalPrice": "TotalProductPrice",
        }
        
        
     
class RefundForm(forms.ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', 'disabled': 'true'},))
    inStock = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0', 'disabled': 'true'},))
    due = forms.FloatField(label="Due refund", widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0', 'value': '0', 'id': 'dueRefund' },))

    # create meta class
    class Meta:
        # specify model to be used
        model = Refund
        
        # specify fields to be used
        fields = [
            "quantity",
            "unitPrice",
            "totalRefund",
            "note",
        ]
        widgets = {
            "quantity": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0', 'value': '0'}),
            "unitPrice": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "totalRefund": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0', 'id': 'totalRefund',}),
        }
        labels = {
            "totalRefund": "Total Refund",
        }        
     
     
class DueCollectionForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = DueCollection
        
        # specify fields to be used
        fields = [
            "amount",
            "note",
        ]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": 'form-control-sm', 'min': '0'}),
            "note": forms.Textarea(attrs={"class": 'form-control form-control-sm',}),
        }
        labels = {
            "amount": "Due Collected",
            "note": "Note",
        }  
        
        
class PurchaseSummaryForm(forms.Form):
    FromDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    ToDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    company = ModelChoiceField(queryset=Company.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))
    supplier = ModelChoiceField(queryset=Supplier.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))


        
class ProductInStockForm(forms.Form):
    FromDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    ToDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    company = ModelChoiceField(queryset=Company.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))
    category = ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))
    product = ModelChoiceField(queryset=Product.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))
    productCode = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control-sm', },))

       
       
class SalesSummaryForm(forms.Form):
    FromDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    ToDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    user = ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))
    customer = ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))
   
        
       
class SalesByCustomerForm(forms.Form):
    FromDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    ToDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    customer = ModelChoiceField(queryset=Customer.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm', },))
   
        
      