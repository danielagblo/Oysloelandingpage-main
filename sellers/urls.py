from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sellers', views.SellerViewSet)
router.register(r'analytics', views.AnalyticsViewSet)

urlpatterns = [
    # Public endpoints (no authentication required) - MUST come before router
    path('submit-seller/', views.submit_seller_form, name='submit-seller'),
    path('track-pageview/', views.track_pageview, name='track-pageview'),
    # path('public/submit-contact/', views.submit_contact_form, name='submit-contact'),
    
    # API endpoints (for authenticated users)
    path('', include(router.urls)),
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
] 