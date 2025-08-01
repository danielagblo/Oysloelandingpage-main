from rest_framework import serializers
from .models import Seller, Analytics
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class SellerSerializer(serializers.ModelSerializer):
    reviewed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Seller
        fields = [
            'id', 'business_name', 'business_type', 'business_description',
            'owner_name', 'email_address', 'phone_number', 'location',
            'experience_level', 'inventory_size', 'status', 'created_at',
            'updated_at', 'reviewed_by', 'reviewed_at', 'review_notes'
        ]
        read_only_fields = ['created_at', 'updated_at', 'reviewed_by', 'reviewed_at']

class SellerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            'business_name', 'business_type', 'business_description',
            'owner_name', 'email_address', 'phone_number', 'location',
            'experience_level', 'inventory_size'
        ]

class SellerStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['status', 'review_notes']

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = ['id', 'date', 'page_views', 'form_submissions']

class DashboardStatsSerializer(serializers.Serializer):
    total_sellers = serializers.IntegerField()
    pending_sellers = serializers.IntegerField()
    approved_sellers = serializers.IntegerField()
    rejected_sellers = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_submissions = serializers.IntegerField()
    total_days = serializers.IntegerField() 