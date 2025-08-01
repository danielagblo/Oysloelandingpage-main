from django.contrib import admin
from .models import Seller, Analytics

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
