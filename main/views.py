from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime

def home(request):
    """Render the main one-page website"""
    context = {
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'page_title': 'Modern One-Page Website'
    }
    return render(request, 'main/index.html', context)

def api_data(request):
    """API endpoint to return dynamic data"""
    data = {
        'message': 'Hello from Django backend!',
        'timestamp': datetime.now().isoformat(),
        'status': 'success',
        'data': {
            'users_count': 42,
            'features': ['Responsive Design', 'Modern UI', 'Django Backend', 'JavaScript Interactivity'],
            'technologies': ['HTML5', 'CSS3', 'JavaScript', 'Django', 'Python']
        }
    }
    return JsonResponse(data)
