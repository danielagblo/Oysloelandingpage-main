# Modern One-Page Website with Django Backend

A beautiful, responsive one-page website built with Django backend, HTML5, CSS3, and JavaScript.

## Features

- **Modern Design**: Clean, professional design with smooth animations
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Django Backend**: Robust Python backend with API endpoints
- **Interactive Elements**: Dynamic content loading, smooth scrolling, and form validation
- **Performance Optimized**: Efficient code with modern best practices

## Technologies Used

- **Backend**: Django 4.2+ (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## Project Structure

```
testsite/
├── manage.py                 # Django management script
├── requirements.txt         # Python dependencies
├── testsite/                # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── main/                    # Main Django app
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── tests.py            # Unit tests
│   ├── urls.py             # App URL patterns
│   └── views.py            # View functions
├── templates/              # HTML templates
│   └── main/
│       └── index.html      # Main template
└── static/                 # Static files
    ├── css/
    │   └── style.css       # Main stylesheet
    └── js/
        └── script.js       # JavaScript functionality
```

## Installation & Setup

1. **Clone or download the project**
   ```bash
   cd /Users/danielagblo/Downloads/testsite
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser and visit**
   ```
   http://127.0.0.1:8000/
   ```

## Features Overview

### Frontend Features
- **Responsive Navigation**: Mobile-friendly hamburger menu
- **Hero Section**: Eye-catching landing area with call-to-action buttons
- **About Section**: Feature cards with icons and descriptions
- **Services Section**: Service offerings with hover effects
- **Dynamic Data Section**: Real-time data from Django API
- **Contact Form**: Interactive form with validation
- **Smooth Scrolling**: Seamless navigation between sections
- **Animations**: Fade-in effects and smooth transitions

### Backend Features
- **Django Views**: Clean separation of concerns
- **API Endpoints**: RESTful API for dynamic content
- **Admin Interface**: Easy content management
- **Database Models**: Structured data storage
- **Static File Handling**: Optimized asset delivery

### JavaScript Functionality
- **Mobile Menu Toggle**: Responsive navigation
- **Smooth Scrolling**: Enhanced user experience
- **Form Validation**: Client-side validation with notifications
- **API Integration**: Dynamic content loading
- **Scroll Effects**: Parallax and animation triggers
- **Performance Optimization**: Debounced scroll handlers

## API Endpoints

- `GET /` - Main website page
- `GET /api/data/` - JSON API endpoint for dynamic data

## Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Color scheme can be changed by updating CSS variables
- Responsive breakpoints can be adjusted in media queries

### Content
- Update `templates/main/index.html` for content changes
- Modify `main/views.py` for backend logic
- Add new sections by extending the HTML template

### JavaScript
- Enhance `static/js/script.js` for additional functionality
- Add new interactive features as needed

## Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Development

### Running Tests
```bash
python manage.py test
```

### Collecting Static Files (for production)
```bash
python manage.py collectstatic
```

### Database Management
```bash
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use environment variables for sensitive settings
2. **Static Files**: Configure proper static file serving
3. **Database**: Use PostgreSQL or MySQL for production
4. **Security**: Update SECRET_KEY and disable DEBUG
5. **HTTPS**: Enable SSL/TLS certificates
6. **Caching**: Implement Redis or Memcached
7. **CDN**: Use a CDN for static assets

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please check the Django documentation or create an issue in the project repository.
