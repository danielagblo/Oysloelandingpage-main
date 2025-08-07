from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.middleware.csrf import get_token
from datetime import datetime, timedelta
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Seller, Analytics, PricingPlan
from .serializers import (
    SellerSerializer, SellerCreateSerializer, SellerStatusUpdateSerializer,
    AnalyticsSerializer, DashboardStatsSerializer
)

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SellerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SellerStatusUpdateSerializer
        return SellerSerializer
    
    def get_queryset(self):
        queryset = Seller.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(business_name__icontains=search) |
                Q(owner_name__icontains=search) |
                Q(email_address__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_update(self, serializer):
        seller = serializer.save()
        seller.reviewed_by = self.request.user
        seller.reviewed_at = timezone.now()
        seller.save()
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        seller = self.get_object()
        serializer = SellerStatusUpdateSerializer(seller, data=request.data, partial=True)
        
        if serializer.is_valid():
            seller = serializer.save()
            seller.reviewed_by = request.user
            seller.reviewed_at = timezone.now()
            seller.save()
            
            return Response({
                'message': f'Seller status updated to {seller.get_status_display()}',
                'seller': SellerSerializer(seller).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        seller_ids = request.data.get('sellerIds', [])
        
        if not seller_ids:
            return Response(
                {'error': 'No seller IDs provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count = Seller.objects.filter(id__in=seller_ids).delete()[0]
        
        return Response({
            'message': f'{deleted_count} seller(s) deleted successfully',
            'deleted_count': deleted_count
        })

class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def track_pageview(self, request):
        """Track a page view"""
        today = timezone.now().date()
        analytics, created = Analytics.objects.get_or_create(
            date=today,
            defaults={'page_views': 1, 'form_submissions': 0}
        )
        
        if not created:
            analytics.page_views += 1
            analytics.save()
        
        return Response({
            'message': 'Page view tracked successfully',
            'date': today,
            'page_views': analytics.page_views
        })
    
    @action(detail=False, methods=['post'])
    def track_submission(self, request):
        """Track a form submission"""
        today = timezone.now().date()
        analytics, created = Analytics.objects.get_or_create(
            date=today,
            defaults={'page_views': 0, 'form_submissions': 1}
        )
        
        if not created:
            analytics.form_submissions += 1
            analytics.save()
        
        return Response({
            'message': 'Form submission tracked successfully',
            'date': today,
            'form_submissions': analytics.form_submissions
        })
    
    @action(detail=False, methods=['get'])
    def get_stats(self, request):
        """Get analytics statistics for different periods"""
        period = request.query_params.get('period', '7days')
        
        # Calculate date range
        today = timezone.now().date()
        if period == 'today':
            start_date = today
        elif period == '7days':
            start_date = today - timedelta(days=7)
        elif period == '30days':
            start_date = today - timedelta(days=30)
        elif period == '90days':
            start_date = today - timedelta(days=90)
        else:
            start_date = today - timedelta(days=7)
        
        # Get analytics data
        analytics_data = Analytics.objects.filter(
            date__gte=start_date
        ).aggregate(
            total_views=Sum('page_views'),
            total_submissions=Sum('form_submissions'),
            total_days=Count('date'),
            avg_views_per_day=Sum('page_views') / Count('date'),
            avg_submissions_per_day=Sum('form_submissions') / Count('date')
        )
        
        # Get daily breakdown for charts
        daily_data = Analytics.objects.filter(
            date__gte=start_date
        ).order_by('date').values('date', 'page_views', 'form_submissions')
        
        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': today,
            'total_views': analytics_data['total_views'] or 0,
            'total_submissions': analytics_data['total_submissions'] or 0,
            'total_days': analytics_data['total_days'] or 0,
            'avg_views_per_day': round(analytics_data['avg_views_per_day'] or 0, 2),
            'avg_submissions_per_day': round(analytics_data['avg_submissions_per_day'] or 0, 2),
            'conversion_rate': round(
                (analytics_data['total_submissions'] or 0) / (analytics_data['total_views'] or 1) * 100, 2
            ),
            'daily_data': list(daily_data)
        })

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        period = request.query_params.get('period', '7days')
        
        # Calculate date range
        today = timezone.now().date()
        if period == '7days':
            start_date = today - timedelta(days=7)
        elif period == '30days':
            start_date = today - timedelta(days=30)
        elif period == '90days':
            start_date = today - timedelta(days=90)
        else:
            start_date = today - timedelta(days=7)
        
        # Get analytics data
        analytics_data = Analytics.objects.filter(
            date__gte=start_date
        ).aggregate(
            total_views=Sum('page_views'),
            total_submissions=Sum('form_submissions'),
            total_days=Count('date')
        )
        
        # Get seller statistics
        seller_stats = Seller.objects.aggregate(
            total_sellers=Count('id'),
            pending_sellers=Count('id', filter=Q(status='pending')),
            approved_sellers=Count('id', filter=Q(status='approved')),
            rejected_sellers=Count('id', filter=Q(status='rejected'))
        )
        
        # Combine data
        stats = {
            'total_sellers': seller_stats['total_sellers'] or 0,
            'pending_sellers': seller_stats['pending_sellers'] or 0,
            'approved_sellers': seller_stats['approved_sellers'] or 0,
            'rejected_sellers': seller_stats['rejected_sellers'] or 0,
            'total_views': analytics_data['total_views'] or 0,
            'total_submissions': analytics_data['total_submissions'] or 0,
            'total_days': analytics_data['total_days'] or 0
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

@csrf_exempt
def submit_seller_form(request):
    """Public endpoint for submitting seller applications"""
    if request.method == 'POST':
        import json
        
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
        
        serializer = SellerCreateSerializer(data=data)
        
        if serializer.is_valid():
            seller = serializer.save()
            
            # Track form submission
            today = timezone.now().date()
            analytics, created = Analytics.objects.get_or_create(
                date=today,
                defaults={'page_views': 0, 'form_submissions': 1}
            )
            
            if not created:
                analytics.form_submissions += 1
                analytics.save()
            
            return JsonResponse({
                'message': 'Application submitted successfully!',
                'seller_id': seller.id
            })
        else:
            return JsonResponse({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=400)
    
    return JsonResponse({
        'error': 'Method not allowed'
    }, status=405)

@csrf_exempt
def track_pageview(request):
    """Public endpoint for tracking page views"""
    if request.method == 'POST':
        today = timezone.now().date()
        analytics, created = Analytics.objects.get_or_create(
            date=today,
            defaults={'page_views': 1, 'form_submissions': 0}
        )
        
        if not created:
            analytics.page_views += 1
            analytics.save()
        
        return JsonResponse({
            'message': 'Page view tracked successfully',
            'date': today.isoformat(),
            'page_views': analytics.page_views
        })
    
    return JsonResponse({
        'error': 'Method not allowed'
    }, status=405)

@require_http_methods(["GET"])
def pricing_api(request):
    """API endpoint to get pricing plans"""
    try:
        pricing_plans = PricingPlan.objects.filter(is_active=True).order_by('monthly_price')
        
        plans_data = []
        for plan in pricing_plans:
            plans_data.append({
                'name': plan.name,
                'display_name': plan.display_name,
                'description': plan.description,
                'monthly_price': float(plan.monthly_price),
                'yearly_price': float(plan.yearly_price),
                'cancelled_monthly_price': float(plan.cancelled_monthly_price) if plan.cancelled_monthly_price else None,
                'cancelled_yearly_price': float(plan.cancelled_yearly_price) if plan.cancelled_yearly_price else None,
                'is_popular': plan.is_popular,
                'yearly_discount': plan.yearly_discount_percentage,
                'has_cancelled_prices': plan.has_cancelled_prices
            })
        
        return JsonResponse({
            'success': True,
            'plans': plans_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    # Get today's analytics
    today = timezone.now().date()
    today_analytics = Analytics.objects.filter(date=today).first()
    
    # Get recent analytics (last 7 days)
    recent_analytics = Analytics.objects.filter(
        date__gte=today - timedelta(days=7)
    ).order_by('-date')
    
    # Get seller statistics
    seller_stats = {
        'total': Seller.objects.count(),
        'pending': Seller.objects.filter(status='pending').count(),
        'approved': Seller.objects.filter(status='approved').count(),
        'rejected': Seller.objects.filter(status='rejected').count(),
    }
    
    context = {
        'today_analytics': today_analytics,
        'recent_analytics': recent_analytics,
        'seller_stats': seller_stats,
    }
    
    return render(request, 'admin/dashboard.html', context)
