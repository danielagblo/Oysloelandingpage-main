# OYSLOE Marketplace - Admin Panel & API

A comprehensive admin panel and API system for the OYSLOE marketplace, featuring seller management, analytics, and form processing.

## 🚀 Features

### Admin Panel
- **Dashboard** - Overview of key metrics and recent activity
- **Seller Management** - View, approve, reject, and manage seller applications
- **Analytics** - Track page views, form submissions, and business metrics
- **Settings** - Admin account management and system configuration
- **Responsive Design** - Works on desktop, tablet, and mobile devices

### API Backend
- **RESTful API** - Complete CRUD operations for sellers
- **Authentication** - JWT-based admin authentication
- **Database** - SQLite database with automatic table creation
- **Security** - Rate limiting, CORS, and input validation
- **Analytics** - Automatic tracking of page views and form submissions

### Frontend Integration
- **Form Processing** - Connected seller application form
- **Real-time Validation** - Client-side form validation
- **Success/Error Handling** - User-friendly notifications
- **Page Analytics** - Automatic page view tracking

## 📋 Prerequisites

- Node.js (v14 or higher)
- npm or yarn package manager

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the server**
   ```bash
   npm start
   ```
   
   For development with auto-restart:
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### Default Admin Account
The system automatically creates a default admin account:
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@oysloe.com`

⚠️ **Important:** Change the default password after first login for security.

### Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
PORT=3000
JWT_SECRET=your-secret-key-here
```

## 🌐 Access Points

### Main Website
- **URL:** `http://localhost:8000` (your existing static server)
- **Description:** OYSLOE marketplace homepage with seller form

### Admin Panel
- **URL:** `http://localhost:3000/admin`
- **Description:** Admin dashboard for managing sellers and viewing analytics

### API Endpoints
- **Base URL:** `http://localhost:3000/api`
- **Documentation:** See API endpoints below

## 📊 API Endpoints

### Public Endpoints
```
POST /api/sellers              - Submit seller application
POST /api/analytics/pageview   - Track page view
```

### Admin Endpoints (Require Authentication)
```
POST /api/admin/login          - Admin login
GET  /api/admin/sellers        - Get all sellers (with pagination/filtering)
PATCH /api/admin/sellers/:id/status - Update seller status
GET  /api/admin/analytics      - Get analytics data
```

## 🎯 Usage Guide

### 1. Starting the System
1. Start your static website server: `python -m http.server 8000`
2. Start the admin API: `npm start`
3. Access the admin panel at `http://localhost:3000/admin`

### 2. Admin Panel Features

#### Dashboard
- View total sellers, pending applications, page views, and form submissions
- See recent seller applications
- Quick access to common actions

#### Seller Management
- View all seller applications in a paginated table
- Search sellers by name, business, or email
- Filter by status (pending, approved, rejected)
- Approve or reject applications
- View detailed seller information

#### Analytics
- Track page views and form submissions
- View data for different time periods (7, 30, 90 days)
- Visual charts and statistics

#### Settings
- Update admin account information
- Change password
- View system information

### 3. Form Integration
The seller form on your homepage (`http://localhost:8000`) is now connected to the API:
- Real-time validation
- Automatic submission to database
- Success/error notifications
- Page view tracking

## 🗄️ Database Schema

### Sellers Table
```sql
CREATE TABLE sellers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email_address TEXT NOT NULL,
    location TEXT NOT NULL,
    business_name TEXT NOT NULL,
    business_type TEXT NOT NULL,
    experience_level TEXT NOT NULL,
    inventory_size TEXT NOT NULL,
    business_description TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Admins Table
```sql
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Analytics Table
```sql
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_views INTEGER DEFAULT 0,
    form_submissions INTEGER DEFAULT 0,
    date DATE DEFAULT CURRENT_DATE
);
```

## 🔒 Security Features

- **JWT Authentication** - Secure admin login
- **Password Hashing** - bcrypt for password security
- **Rate Limiting** - Prevents API abuse
- **Input Validation** - Server-side validation
- **CORS Protection** - Cross-origin request security
- **Helmet Security** - Additional security headers

## 🎨 Customization

### Styling
- Admin panel styles: `public/admin/styles.css`
- Main website styles: `styles.css`

### Functionality
- Admin panel logic: `public/admin/script.js`
- Main website logic: `script.js`
- API server: `server.js`

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the PORT in `.env` file or `server.js`
   - Kill existing processes using the port

2. **Database errors**
   - Delete `database.sqlite` file to reset
   - Check file permissions

3. **CORS errors**
   - Ensure both servers are running
   - Check browser console for specific errors

4. **Form not submitting**
   - Verify API server is running on port 3000
   - Check browser network tab for errors

### Logs
Check the console output for:
- Server startup messages
- Database connection status
- API request logs
- Error messages

## 📈 Future Enhancements

- Email notifications for new applications
- Advanced analytics and reporting
- Bulk operations for sellers
- Export functionality
- Multi-admin support
- Audit logging
- Backup and restore functionality

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Verify all services are running
4. Check database file permissions

## 📄 License

This project is part of the OYSLOE marketplace system.

---

**OYSLOE Admin Panel** - Your complete marketplace management solution! 🚀 