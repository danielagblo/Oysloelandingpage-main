# DigitalOcean Django Deployment Guide

This guide will help you deploy your Django application to DigitalOcean using multiple deployment methods.

## 🚀 Deployment Options

### Option 1: Traditional Server Deployment (Recommended for beginners)

#### Prerequisites
- DigitalOcean Droplet (Ubuntu 20.04+ recommended)
- Domain name (optional but recommended)
- SSH access to your droplet

#### Step-by-Step Deployment

1. **Create a DigitalOcean Droplet**
   - Go to DigitalOcean Control Panel
   - Create a new droplet (Ubuntu 20.04, $6/month minimum)
   - Add your SSH key for secure access

2. **Connect to your server**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Create a non-root user**
   ```bash
   adduser django
   usermod -aG sudo django
   su - django
   ```

4. **Upload your project files**
   ```bash
   # From your local machine
   scp -r /Users/danielagblo/Downloads/testsite django@your-droplet-ip:/home/django/
   ```

5. **Run the deployment script**
   ```bash
   cd /home/django/testsite
   chmod +x deploy.sh
   ./deploy.sh
   ```

6. **Configure your domain (if you have one)**
   - Update DNS records to point to your droplet IP
   - Update `.env` file with your domain name
   - Configure SSL certificates

### Option 2: Docker Deployment

#### Prerequisites
- DigitalOcean Droplet with Docker installed
- Docker Compose

#### Deployment Steps

1. **Install Docker on your droplet**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

2. **Install Docker Compose**
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Deploy with Docker Compose**
   ```bash
   # Copy your project files to the server
   scp -r /Users/danielagblo/Downloads/testsite django@your-droplet-ip:/home/django/
   
   # On the server
   cd /home/django/testsite
   cp env.example .env
   # Edit .env with your configuration
   
   # Start the application
   docker-compose up -d
   ```

### Option 3: App Platform Deployment

#### Prerequisites
- DigitalOcean App Platform account
- GitHub repository (push your code to GitHub first)

#### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/testsite.git
   git push -u origin main
   ```

2. **Create App Platform App**
   - Go to DigitalOcean App Platform
   - Click "Create App"
   - Connect your GitHub repository
   - Select your repository and branch

3. **Configure the app**
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run Command: `gunicorn --config gunicorn.conf.py testsite.wsgi:application`
   - Environment Variables: Add all variables from your `.env` file

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Django settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# Database (use DigitalOcean Managed Database)
DATABASE_URL=postgresql://username:password@your-db-host:25060/dbname?sslmode=require

# Redis (use DigitalOcean Managed Redis)
REDIS_URL=redis://username:password@your-redis-host:25061/0

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Database Setup

#### Option 1: DigitalOcean Managed Database (Recommended)
1. Create a PostgreSQL database in DigitalOcean
2. Get the connection string
3. Update `DATABASE_URL` in your `.env` file

#### Option 2: Local PostgreSQL
```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb testsite
sudo -u postgres createuser django
sudo -u postgres psql -c "ALTER USER django PASSWORD 'your-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE testsite TO django;"
```

### SSL Certificate Setup

#### Using Let's Encrypt (Free)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### Using DigitalOcean SSL
1. Go to DigitalOcean Control Panel
2. Add your domain
3. Generate SSL certificate
4. Update nginx configuration with certificate paths

## 📊 Monitoring and Maintenance

### Log Monitoring
```bash
# Application logs
journalctl -u testsite -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Application logs
tail -f /home/django/testsite/logs/django.log
```

### Backup Strategy
```bash
# Run backup script
/home/django/testsite/backup.sh

# Database backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Updates
```bash
# Update application
/home/django/testsite/update.sh

# Restart services
sudo systemctl restart testsite
sudo systemctl reload nginx
```

## 🔒 Security Checklist

- [ ] Change default admin password
- [ ] Configure firewall (UFW)
- [ ] Enable SSL/HTTPS
- [ ] Set up regular backups
- [ ] Configure monitoring
- [ ] Update system packages regularly
- [ ] Use strong secret keys
- [ ] Configure proper file permissions

## 🚨 Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check if Gunicorn is running: `sudo systemctl status testsite`
   - Check logs: `journalctl -u testsite -f`

2. **Static files not loading**
   - Run: `python manage.py collectstatic --noinput`
   - Check nginx configuration

3. **Database connection errors**
   - Verify DATABASE_URL in .env file
   - Check database server status

4. **Permission denied errors**
   - Check file permissions: `ls -la /home/django/testsite`
   - Fix permissions: `sudo chown -R django:www-data /home/django/testsite`

### Performance Optimization

1. **Enable Gzip compression** (already configured in nginx.conf)
2. **Set up Redis caching** (configure REDIS_URL)
3. **Use CDN for static files** (Cloudflare, AWS CloudFront)
4. **Optimize database queries**
5. **Enable HTTP/2** (already configured)

## 📈 Scaling

### Horizontal Scaling
- Use DigitalOcean Load Balancer
- Deploy multiple app instances
- Use managed databases and Redis

### Vertical Scaling
- Upgrade droplet size
- Add more workers in gunicorn.conf.py
- Optimize database queries

## 💰 Cost Optimization

- Use DigitalOcean App Platform for automatic scaling
- Use managed databases and Redis
- Enable CDN for static files
- Monitor resource usage

## 📞 Support

- DigitalOcean Documentation: https://docs.digitalocean.com/
- Django Deployment Guide: https://docs.djangoproject.com/en/stable/howto/deployment/
- Community Forums: https://www.digitalocean.com/community

---

**Note**: This guide assumes you have basic knowledge of Linux, Django, and web deployment. For production deployments, always test in a staging environment first.
