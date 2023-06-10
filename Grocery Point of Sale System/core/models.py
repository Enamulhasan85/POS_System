from email.policy import default
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

STATUS = (
    ('RECEIVED', 'Received'),
    ('APPROVED', 'Approved'),
    ('PROCESSING', 'Processing'),
    ('SHIPPED', 'Shipped'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    fullName = models.CharField(max_length=400, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20, blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    entryDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.fullName


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    addressName = models.CharField(max_length=400, blank=True)
    streetAddress = models.CharField(max_length=100)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.streetAddress}, {self.area}, {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = 'Addresses'


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = PhoneNumberField(blank=True)
    # gender = models.CharField(choices=GENDER, max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = PhoneNumberField(blank=True)
    # gender = models.CharField(choices=GENDER, max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    # gender = models.CharField(choices=GENDER, max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    productCode = models.CharField(max_length=100)
    # price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    # quantity = models.IntegerField(default=0)
    # entrydate = models.DateField(null=True, blank=True)
    # sold = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("core:product", kwargs={
    #         'slug': self.productCode
    #     })


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    provider = models.CharField(max_length=100)
    totalPrice = models.FloatField()
    note = models.TextField(null=True, blank=True)
    entryDate = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} - {self.entryDate.strftime("%Y-%m-%d %H:%M:%S")}'


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    tradePrice = models.FloatField()
    totalPrice = models.FloatField()
    
    def __str__(self):
        return f"{self.product} - {self.quantity}"


class Stock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, blank=True, null=True)
    purchasedetail = models.ForeignKey(PurchaseDetail, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    tradePrice = models.FloatField()
    mrp = models.FloatField()
    discount = models.IntegerField(default=0)
    entryDate = models.DateTimeField(null=True, blank=True)
    manufacturingDate = models.DateField(null=True, blank=True)
    expirationDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.product.title}"

    def get_total_item_price(self):
        return self.quantity * self.tradePrice

    def get_total_discount_item_price(self):
        return self.quantity * self.tradePrice * (1 - (self.discount/100.00))

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.get_total_discount_item_price()


class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    saleStripeId = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField()
    totalPrice = models.FloatField()
    discount = models.FloatField()
    status = models.CharField(choices=STATUS, max_length=20)
    note = models.TextField()
    
    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return f'{self.customer.name} - {self.date.strftime("%Y-%m-%d %H:%M:%S")}'


class Refund(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    Amount = models.FloatField()
    date = models.DateTimeField()
    note = models.TextField()
    
    def __str__(self):
        return f'Refunded by {self.user} on {self.date.strftime("%Y-%m-%d %H:%M:%S")}'
    
    
class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    refund = models.ForeignKey(Refund, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    totalPrice = models.FloatField()
    quantity = models.IntegerField()
    unitPrice = models.FloatField()

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_item_price(self):
        return self.quantity * self.unitPrice

    def get_amount_saved(self):
        return self.get_total_item_price()

    def get_final_price(self):
        return self.get_total_item_price()
    

class Due(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dueAmount = models.FloatField()
    date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.sale} on {self.date}"


class DueCollection(models.Model):
    due = models.ForeignKey(Due, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    Amount = models.FloatField()
    date = models.DateTimeField()
    note = models.TextField()
    
    def __str__(self):
        return f"Collected by {self.user} on {self.date}"
