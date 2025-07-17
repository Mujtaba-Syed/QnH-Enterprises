# QnH Enterprises - Docker Setup

This document explains how to run the QnH Enterprises Django application using Docker with environment-based configuration.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### Environment Configuration

The project supports two environments:

1. **Development** - Uses SQLite database
2. **Production** - Uses PostgreSQL database

## 📁 File Structure

```
QnH-Enterprises/
├── Dockerfile                 # Main Docker image definition
├── docker-compose.yml         # Main compose file
├── .env                       # Environment variables (dev & prod)
├── scripts/
│   ├── start-dev.sh          # Development startup script
│   └── start.sh              # Production startup script
├── nginx.conf                # Nginx configuration for production
├── .dockerignore             # Files to exclude from Docker build
└── core/                     # Django project
```

## 🛠️ Development Setup

### 1. Clone and Navigate
```bash
cd QnH-Enterprises
```

### 2. Run Development Environment
```bash
# Development (default)
docker-compose up --build

# Or explicitly set environment
ENVIRONMENT=development STARTUP_SCRIPT=./scripts/start-dev.sh docker-compose up --build
```

### 3. Access the Application
- **Web Application**: https://www.qhenterprises.com
- **Admin Interface**: https://www.qhenterprises.com/admin

### 4. Development Features
- **Hot Reload**: Code changes are automatically reflected
- **SQLite Database**: No external database required
- **Console Email**: Email output goes to console
- **Debug Mode**: Enabled for development

## 🚀 Production Setup

### 1. Configure Production Environment
Edit `env.production` file with your production settings:
```bash
# Update these values in env.production
SECRET_KEY=your-super-secret-production-key
POSTGRES_DB=your_production_db_name
POSTGRES_USER=your_production_user
POSTGRES_PASSWORD=your_secure_password
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
BASE_URL=https://your-domain.com
```

### 2. Run Production Environment
```bash
# Production
ENVIRONMENT=production STARTUP_SCRIPT=./scripts/start.sh docker-compose up --build --profile production
```

### 3. Production Features
- **PostgreSQL Database**: Robust production database
- **Redis Caching**: For improved performance
- **Nginx Reverse Proxy**: For static files and load balancing
- **Gunicorn**: Production WSGI server
- **Security Headers**: Enhanced security configuration

## 🔧 Docker Commands

### Build Images
```bash
# Build image
docker-compose build
```

### Run Services
```bash
# Start development environment (default)
docker-compose up

# Start production environment
ENVIRONMENT=production STARTUP_SCRIPT=./scripts/start.sh docker-compose up --profile production

# Run in background
docker-compose up -d
```

### Stop Services
```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### View Logs
```bash
# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs web

# Follow logs in real-time
docker-compose logs -f
```

### Execute Commands
```bash
# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Access Django shell
docker-compose exec web python manage.py shell

# Access database shell (production)
docker-compose exec db psql -U qnh_production_user -d qnh_production_db
```

## 🔒 Security Considerations

### Development
- Uses SQLite (file-based database)
- Debug mode enabled
- Console email backend
- No SSL/TLS

### Production
- PostgreSQL with secure credentials
- Debug mode disabled
- SMTP email configuration
- Nginx with security headers
- SSL/TLS ready (configure certificates)

## 📊 Monitoring and Logs

### Application Logs
```bash
# View Django application logs
docker-compose logs web

# View Nginx logs (production)
docker-compose logs nginx

# View database logs
docker-compose logs db
```

### Database Monitoring
```bash
# Connect to PostgreSQL (production)
docker-compose exec db psql -U qnh_production_user -d qnh_production_db

# View Redis info (production)
docker-compose exec redis redis-cli info
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Kill the process or change port in docker-compose.yml
   ```

2. **Database Connection Issues**
   ```bash
   # Check if database is running
   docker-compose ps
   
   # Restart database service
   docker-compose restart db
   ```

3. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

4. **Build Failures**
   ```bash
   # Clean build cache
   docker-compose build --no-cache
   
   # Remove all containers and images
   docker system prune -a
   ```

### Reset Everything
```bash
# Stop all containers
docker-compose down

# Remove all volumes
docker-compose down -v

# Remove all images
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

## 🔄 Environment Variables

### Development (`env.development`)
- `DEBUG=True`
- `PRODUCTION=False`
- Uses SQLite database
- Console email backend

### Production (`env.production`)
- `DEBUG=False`
- `PRODUCTION=True`
- PostgreSQL database configuration
- SMTP email configuration
- Security settings

## 📝 Additional Notes

- **Media Files**: Stored in Docker volumes for persistence
- **Static Files**: Collected during build process
- **Database**: SQLite for dev, PostgreSQL for production
- **Caching**: Redis available in production
- **Reverse Proxy**: Nginx handles static files and load balancing in production

## 🤝 Contributing

When contributing to this project:

1. Use the development environment for testing
2. Update environment files if adding new variables
3. Test both development and production configurations
4. Update this README if changing Docker setup

## 📞 Support

For issues related to Docker setup:
1. Check the troubleshooting section
2. Review Docker and Docker Compose logs
3. Ensure all prerequisites are installed
4. Verify environment variable configuration 