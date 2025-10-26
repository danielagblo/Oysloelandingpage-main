#!/bin/bash

# DigitalOcean Django Deployment Script
# This script sets up a Django application on a DigitalOcean droplet

set -e  # Exit on any error

echo "🚀 Starting DigitalOcean Django Deployment Setup"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please do not run this script as root. Run as a regular user with sudo privileges."
    exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
print_status "Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql-client redis-tools git curl wget unzip

# Create application directory
APP_DIR="/home/$USER/testsite"
print_status "Creating application directory: $APP_DIR"
mkdir -p $APP_DIR
cd $APP_DIR

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media
mkdir -p backups

# Set up environment file
print_status "Setting up environment configuration..."
if [ ! -f .env ]; then
    cp env.example .env
    print_warning "Please edit .env file with your actual configuration values"
fi

# Run Django setup commands
print_status "Running Django setup commands..."
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser (optional)
print_status "Creating Django superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Set up systemd service for Gunicorn
print_status "Creating systemd service for Gunicorn..."
sudo tee /etc/systemd/system/testsite.service > /dev/null <<EOF
[Unit]
Description=Gunicorn instance to serve testsite
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --config gunicorn.conf.py testsite.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
print_status "Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/testsite
sudo ln -sf /etc/nginx/sites-available/testsite /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Set proper permissions
print_status "Setting proper file permissions..."
sudo chown -R $USER:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod -R 775 $APP_DIR/logs
sudo chmod -R 775 $APP_DIR/media

# Enable and start services
print_status "Enabling and starting services..."
sudo systemctl daemon-reload
sudo systemctl enable testsite
sudo systemctl start testsite
sudo systemctl enable nginx
sudo systemctl restart nginx

# Configure firewall
print_status "Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# Create backup script
print_status "Creating backup script..."
tee $APP_DIR/backup.sh > /dev/null <<EOF
#!/bin/bash
# Backup script for Django application

BACKUP_DIR="$APP_DIR/backups"
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_\$DATE.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p \$BACKUP_DIR

# Create backup
tar -czf \$BACKUP_DIR/\$BACKUP_FILE \\
    --exclude='venv' \\
    --exclude='logs' \\
    --exclude='staticfiles' \\
    --exclude='media' \\
    --exclude='backups' \\
    --exclude='.git' \\
    --exclude='__pycache__' \\
    --exclude='*.pyc' \\
    .

echo "Backup created: \$BACKUP_DIR/\$BACKUP_FILE"

# Keep only last 7 backups
cd \$BACKUP_DIR
ls -t backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Old backups cleaned up"
EOF

chmod +x $APP_DIR/backup.sh

# Create update script
print_status "Creating update script..."
tee $APP_DIR/update.sh > /dev/null <<EOF
#!/bin/bash
# Update script for Django application

echo "🔄 Updating Django application..."

# Activate virtual environment
source venv/bin/activate

# Pull latest changes (if using git)
# git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate

# Restart services
sudo systemctl restart testsite
sudo systemctl reload nginx

echo "✅ Application updated successfully!"
EOF

chmod +x $APP_DIR/update.sh

# Display final status
print_status "Deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "======================"
echo "Application Directory: $APP_DIR"
echo "Virtual Environment: $APP_DIR/venv"
echo "Static Files: $APP_DIR/staticfiles"
echo "Media Files: $APP_DIR/media"
echo "Logs: $APP_DIR/logs"
echo ""
echo "🔧 Service Management:"
echo "====================="
echo "Start service: sudo systemctl start testsite"
echo "Stop service: sudo systemctl stop testsite"
echo "Restart service: sudo systemctl restart testsite"
echo "Check status: sudo systemctl status testsite"
echo "View logs: journalctl -u testsite -f"
echo ""
echo "🌐 Web Server:"
echo "============="
echo "Nginx status: sudo systemctl status nginx"
echo "Nginx logs: sudo tail -f /var/log/nginx/error.log"
echo ""
echo "📁 Useful Commands:"
echo "==================="
echo "Backup: $APP_DIR/backup.sh"
echo "Update: $APP_DIR/update.sh"
echo "Django shell: cd $APP_DIR && source venv/bin/activate && python manage.py shell"
echo "Django admin: http://your-domain.com/admin/ (admin/admin123)"
echo ""
print_warning "Don't forget to:"
echo "1. Update .env file with your actual configuration"
echo "2. Configure SSL certificates for HTTPS"
echo "3. Set up domain DNS to point to your server"
echo "4. Configure database and Redis connections"
echo ""
echo "🎉 Your Django application is ready for production!"
