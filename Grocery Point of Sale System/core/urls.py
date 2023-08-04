from django.urls import path
from core import views, setupviews, purchaseviews, stockviews, saleviews
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    path('accounts/index/', views.userlist, name='userlist'),
    # path('accounts/logout/', views.logout, name='logout'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.registerpage, name='register'),
    path('accounts/login/', views.loginpage, name='login'),
    path('accounts/edit/<int:userid>', views.edituser, name='edituser'),
    path('accounts/delete/', views.deleteuser, name='deleteuser'),
    
    path('company/index/', setupviews.companylist, name='companylist'),
    path('company/create/', setupviews.createcompany, name='createcompany'),
    path('company/edit/<int:id>', setupviews.editcompany, name='editcompany'),
    path('company/delete/', setupviews.deletecompany, name='deletecompany'),
    
    path('supplier/index/', setupviews.supplierlist, name='supplierlist'),
    path('supplier/create/', setupviews.createsupplier, name='createsupplier'),
    path('supplier/edit/<int:id>', setupviews.editsupplier, name='editsupplier'),
    path('supplier/delete/', setupviews.deletesupplier, name='deletesupplier'),
    
    path('customer/index/', setupviews.customerlist, name='customerlist'),
    path('customer/create/', setupviews.createcustomer, name='createcustomer'),
    path('customer/edit/<int:id>', setupviews.editcustomer, name='editcustomer'),
    path('customer/delete/', setupviews.deletecustomer, name='deletecustomer'),
    
    path('category/index/', setupviews.categorylist, name='categorylist'),
    path('category/create/', setupviews.createcategory, name='createcategory'),
    path('category/edit/<int:id>', setupviews.editcategory, name='editcategory'),
    path('category/delete/', setupviews.deletecategory, name='deletecategory'),
    
    path('product/index/', setupviews.productlist, name='productlist'),
    path('product/create/', setupviews.createproduct, name='createproduct'),
    path('product/edit/<int:id>', setupviews.editproduct, name='editproduct'),
    path('product/delete/', setupviews.deleteproduct, name='deleteproduct'),
    path('product/get/', setupviews.getproduct, name='getproduct'),
    path('product/getinfo/', setupviews.getproductinfo, name='getproductinfo'),
    
    path('purchase/index/', purchaseviews.purchaselist, name='purchaselist'),
    path('purchase/create/', purchaseviews.createpurchase, name='createpurchase'),
    path('purchase/edit/<int:id>', purchaseviews.editpurchase, name='editpurchase'),
    path('purchase/delete/', purchaseviews.deletepurchase, name='deletepurchase'),
    
    path('stock/index/', stockviews.stocklist, name='stocklist'),
    path('stock/edit/<int:id>', stockviews.editstock, name='editstock'),
    
    path('sale/index/', saleviews.salelist, name='salelist'),
    path('sale/create/', saleviews.createsale, name='createsale'),
    path('sale/refund/<int:id>', saleviews.refundsale, name='refundsale'),
    path('sale/delete/', saleviews.deletesale, name='deletesale'),
    
    path('due/index/', saleviews.duelist, name='duelist'),
    path('due/collection/<int:id>', saleviews.duecollection, name='duecollection'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/createaddress/', views.createaddressprofile, name='createaddressprofile'),
    path('profile/deleteaddress/<int:id>', views.deleteaddressprofile, name='address_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)