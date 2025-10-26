#!/bin/bash

# Quick start script for local development
echo "🚀 Starting Django Development Server"
echo "===================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp env.example .env
    echo "📝 Please edit .env file with your configuration"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Start development server
echo "🌐 Starting development server..."
echo "📍 Your website will be available at: http://127.0.0.1:8000/"
echo "🛑 Press Ctrl+C to stop the server"
echo "===================================="

python manage.py runserver
