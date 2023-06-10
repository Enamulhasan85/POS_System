from django.contrib import admin
from .models import UserProfile, Address, Company, Customer, Category, Product, Stock, Purchase, PurchaseDetail, Sale, Refund, SaleDetail, Due, DueCollection

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullName', 'phone')
    
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
       
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', )

class StockAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'tradePrice', 'mrp', 'entryDate', 'expirationDate')
   
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'entryDate' )
     
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'tradePrice')
     
class SaleAdmin(admin.ModelAdmin):
    list_display = ('user', 'totalPrice', 'date', 'status')
       
class RefundAdmin(admin.ModelAdmin):
    list_display = ('sale', 'user', 'Amount',)
      
class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity')

class DueAdmin(admin.ModelAdmin):
    list_display = ('sale', 'customer', 'dueAmount', 'date')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'streetAddress', 'city', )
    
class DueCollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'due', 'Amount',  'date')

admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseDetail, PurchaseDetailAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Refund, RefundAdmin)
admin.site.register(SaleDetail, SaleDetailAdmin)
admin.site.register(Due, DueAdmin)
admin.site.register(DueCollection, DueCollectionAdmin)