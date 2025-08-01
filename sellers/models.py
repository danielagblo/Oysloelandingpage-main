from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Seller(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    INVENTORY_CHOICES = [
        ('small', 'Small (1-50 items)'),
        ('medium', 'Medium (51-200 items)'),
        ('large', 'Large (201-500 items)'),
        ('enterprise', 'Enterprise (500+ items)'),
    ]
    
    BUSINESS_TYPE_CHOICES = [
        ('individual', 'Individual Seller'),
        ('business', 'Business/Company'),
        ('retailer', 'Retailer'),
        ('wholesaler', 'Wholesaler'),
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
    ]
    
    # Business Information
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES, default='individual')
    business_description = models.TextField()
    
    # Owner Information
    owner_name = models.CharField(max_length=200)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    
    # Business Details
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    inventory_size = models.CharField(max_length=20, choices=INVENTORY_CHOICES)
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Admin Assignment
    assigned_admins = models.ManyToManyField(User, related_name='assigned_sellers', blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'
    
    def __str__(self):
        return f"{self.business_name} - {self.owner_name}"
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'

class Analytics(models.Model):
    date = models.DateField(unique=True)
    page_views = models.IntegerField(default=0)
    form_submissions = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'
    
    def __str__(self):
        return f"Analytics for {self.date}"


