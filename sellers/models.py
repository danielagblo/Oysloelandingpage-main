from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PricingPlan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic 3x'),
        ('business', 'Business 4x'),
        ('platinum', 'Platinum 10x'),
    ]
    
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2)
    cancelled_monthly_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price to show as crossed out (optional)")
    cancelled_yearly_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original yearly price to show as crossed out (optional)")
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['monthly_price']
        verbose_name = 'Pricing Plan'
        verbose_name_plural = 'Pricing Plans'
    
    def __str__(self):
        return f"{self.get_name_display()} - ¢{self.monthly_price}"
    
    @property
    def yearly_discount_percentage(self):
        """Calculate the discount percentage for yearly billing"""
        if self.monthly_price > 0:
            yearly_total = self.monthly_price * 12
            discount = ((yearly_total - self.yearly_price) / yearly_total) * 100
            return round(discount, 1)
        return 0
    
    @property
    def has_cancelled_prices(self):
        """Check if this plan has cancelled prices to show"""
        return self.cancelled_monthly_price is not None or self.cancelled_yearly_price is not None

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


