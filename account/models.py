import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail
from django.db import models

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, name, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, name, password, **other_fields)
     
    def create_user(self, email, name, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        verbose_name= "Accounts"
        verbose_name_plural = "Accounts"
        
    def email_user(self, subject, message):
        send_mail(subject, message, 'rathorenav123@gmail.com', [self.email], fail_silently=False)
        
    def __str__(self):
        return self.email
    
class Address(models.Model):
    """Address table"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   # this is auto increment id, create a multiple address
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=100)
    phone = models.CharField(_("Phone Number"), max_length=15)
    postcode = models.CharField(_("Postcode"), max_length=15)
    address_line = models.CharField(_("Address line 1"), max_length=250)
    address_line2 = models.CharField(_("Address line 2"), max_length=250)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=150)
    created = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)
    
    class Meta:
        verbose_name= "Address"
        verbose_name_plural = "Addresses"
        
    def __str__(self):
        return "Address"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    