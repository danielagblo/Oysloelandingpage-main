#!/bin/bash

# Modern One-Page Website Startup Script
echo "🚀 Starting Modern One-Page Website with Django Backend"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please check your Python environment."
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  requirements.txt not found. Skipping dependency installation."
fi

# Run Django migrations
echo "🗄️  Running database migrations..."
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Failed to run migrations. Please check your Django setup."
    exit 1
fi
echo "✅ Database migrations completed"

# Start the Django development server
echo "🌐 Starting Django development server..."
echo "📍 Your website will be available at: http://127.0.0.1:8000/"
echo "🛑 Press Ctrl+C to stop the server"
echo "=================================================="

python3 manage.py runserver
