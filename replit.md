# Cascade System Inspection App

## Overview

This is a Flask-based web application for managing cascade boiler and water heater inspections. The system provides role-based access control with three user types: input users (can enter data), download users (can enter and download data), and admin users (full access). The application uses PostgreSQL for data storage and implements user authentication with Flask-Login.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for session management
- **Password Security**: Werkzeug for password hashing
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Tailwind CSS (loaded via CDN)
- **Icons**: Feather Icons
- **JavaScript**: Vanilla JavaScript for form validation and UI interactions
- **Responsive Design**: Mobile-first approach with Tailwind's responsive utilities

### Database Design
- **Primary Database**: PostgreSQL
- **ORM Pattern**: SQLAlchemy with declarative base
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

## Key Components

### User Management System
- **User Model**: Stores user credentials, profile information, and role-based permissions
- **Role System**: Three-tier permission system (input/download/admin)
- **Authentication Flow**: Login/logout with session management
- **Registration System**: New user account creation (incomplete in current implementation)

### Permission System
- **Input Permission**: Basic data entry capabilities
- **Download Permission**: Data entry + data download capabilities  
- **Admin Permission**: Full system access including user management

### Security Features
- **Password Hashing**: Werkzeug's secure password hashing
- **Session Management**: Flask sessions with configurable secret key
- **Input Validation**: Frontend and backend form validation
- **Access Control**: Route-level permission checking

## Data Flow

### User Authentication Flow
1. User submits login credentials via POST to `/login`
2. System validates credentials against User model
3. On success, Flask-Login creates user session
4. User redirected to dashboard based on their role permissions
5. Protected routes check authentication status via `@login_required` decorator

### Permission Checking Flow
1. User attempts to access protected functionality
2. System checks `current_user.has_permission()` method
3. Permission granted/denied based on user's role hierarchy
4. UI elements conditionally rendered based on permissions

## External Dependencies

### Production Dependencies
- **Flask**: Web framework core
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Werkzeug**: WSGI utilities and security functions
- **PostgreSQL**: Production database (configured via DATABASE_URL environment variable)

### Frontend Dependencies (CDN)
- **Tailwind CSS**: Utility-first CSS framework
- **Feather Icons**: Icon library for UI elements

### Development Dependencies
- **SQLite**: Fallback database for local development
- **Flask Debug Mode**: Development server with auto-reload

## Deployment Strategy

### Environment Configuration
- **Database URL**: Configurable via `DATABASE_URL` environment variable
- **Session Secret**: Configurable via `SESSION_SECRET` environment variable
- **Default Fallbacks**: Local development values for missing environment variables

### Database Initialization
- **Auto-migration**: `db.create_all()` runs on application startup
- **Default Admin**: Creates admin user if none exists (username: admin, password: admin123)
- **Connection Pooling**: Configured for production reliability with 300-second recycle time

### Production Readiness
- **Proxy Support**: ProxyFix middleware configured for reverse proxy deployment
- **Connection Management**: Pool pre-ping and recycling for database reliability
- **Logging**: Debug-level logging configured for troubleshooting

### Current Limitations
- **Incomplete Registration**: Registration form exists but POST handler not implemented
- **Missing Features**: Dashboard shows UI for inspection data entry but backend logic not implemented
- **Static Admin Creation**: Admin user created with hardcoded credentials on startup
- **Development Configuration**: Some settings still optimized for development rather than production

The application follows a traditional MVC pattern with Flask blueprints ready for scaling, though currently all routes are in a single file. The role-based permission system is well-architected for expansion to additional user types and permissions as needed.