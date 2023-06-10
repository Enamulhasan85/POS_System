from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
 
      
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", 'password']
        
        
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
            "description",
            "image",
        ]
        
        

class PurchaseForm(forms.ModelForm):
        
    # create meta class
    class Meta:
        # specify model to be used
        model = Purchase
        
        # specify fields to be used
        fields = [
            "company",
            "provider",
            "note",
            "totalPrice",
        ]
        widgets = {
            "company": forms.Select(attrs={'required': 'true', }),
            "totalPrice": forms.NumberInput(attrs={'id': 'totalPurchasePrice', 'min': '0', 'value': '0'}),
        }
        
        
class PurchaseDetailForm(forms.ModelForm):
    manufacturingDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm'},))
    expirationDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm'},))
    mrp = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control-sm', 'min': '0'},))

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
            "purchase",
            "quantity",
            "tradePrice",
            "mrp",
            "discount",
            "entryDate",
            "manufacturingDate",
            "expirationDate",
        ]
        widgets = {
        }