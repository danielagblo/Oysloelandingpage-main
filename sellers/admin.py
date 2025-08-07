from django.contrib import admin
from .models import Seller, Analytics, PricingPlan

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'monthly_price', 'yearly_price', 'cancelled_monthly_price', 'cancelled_yearly_price', 'yearly_discount_percentage', 'is_popular', 'is_active', 'updated_at']
    list_filter = ['is_popular', 'is_active', 'name']
    search_fields = ['display_name', 'description']
    list_editable = ['monthly_price', 'yearly_price', 'cancelled_monthly_price', 'cancelled_yearly_price', 'is_popular', 'is_active']
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('name', 'display_name', 'description')
        }),
        ('Pricing', {
            'fields': ('monthly_price', 'yearly_price'),
            'description': 'Set the monthly and yearly prices for this plan. Yearly price should be less than monthly price × 12 for discount.'
        }),
        ('Cancelled Prices (Optional)', {
            'fields': ('cancelled_monthly_price', 'cancelled_yearly_price'),
            'description': 'Set original prices to show as crossed out. Leave blank if no cancelled prices should be displayed.',
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_popular', 'is_active'),
            'description': 'Mark as popular to highlight this plan. Set active to show on the website.'
        })
    )
    
    readonly_fields = ['yearly_discount_percentage']
    
    def yearly_discount_percentage(self, obj):
        return f"{obj.yearly_discount_percentage}%"
    yearly_discount_percentage.short_description = 'Yearly Discount'

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'owner_name', 'status', 'assigned_admins_display', 'created_at']
    list_filter = ['status', 'business_type', 'experience_level', 'assigned_admins']
    search_fields = ['business_name', 'owner_name', 'email_address']
    filter_horizontal = ['assigned_admins']

    def assigned_admins_display(self, obj):
        return ", ".join([admin.get_full_name() or admin.username for admin in obj.assigned_admins.all()])
    assigned_admins_display.short_description = 'Assigned Admins'

    fieldsets = (
        ('Business Information', {
            'fields': ('business_name', 'business_type', 'business_description')
        }),
        ('Owner Information', {
            'fields': ('owner_name', 'email_address', 'phone_number', 'location')
        }),
        ('Business Details', {
            'fields': ('experience_level', 'inventory_size')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_admins')
        })
    )

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'page_views', 'form_submissions']
    list_filter = ['date']
    readonly_fields = ['date']
