#!/bin/bash

echo "🚀 Starting Production Performance Optimization..."

# Navigate to project directory
cd /app

# Collect static files with optimization
echo "📦 Collecting and optimizing static files..."
python manage.py collectstatic --noinput --clear

# Optimize images (if ImageMagick is available)
if command -v convert &> /dev/null; then
    echo "🖼️  Optimizing images..."
    find staticfiles/ -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | head -100 | xargs -I {} convert {} -strip -quality 85 {}
    find core/media/ -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | head -100 | xargs -I {} convert {} -strip -quality 85 {}
fi

# Database optimization
echo "🗄️  Optimizing database..."
python manage.py dbshell << EOF
VACUUM ANALYZE;
REINDEX DATABASE qhenterprises;
EOF

# Clear cache
echo "🧹 Clearing cache..."
python manage.py clearcache

# Restart services
echo "🔄 Restarting services..."
docker-compose restart web nginx

echo "✅ Production optimization completed!"
echo "📊 Monitor performance with: docker-compose logs -f web"
