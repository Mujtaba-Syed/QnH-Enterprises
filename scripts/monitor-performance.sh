#!/bin/bash

echo "📊 Production Performance Monitor"
echo "=================================="

# Check container status
echo "🐳 Container Status:"
docker-compose ps

echo ""

# Check memory usage
echo "💾 Memory Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

echo ""

# Check nginx access logs for response times
echo "⏱️  Nginx Response Times (last 50 requests):"
docker-compose logs nginx --tail=100 | grep -E "GET|POST" | tail -50 | awk '{print $4, $6, $7, $8}' | head -20

echo ""

# Check Django logs for slow queries
echo "🐌 Django Slow Queries (last 100 lines):"
docker-compose logs web --tail=100 | grep -E "slow|timeout|error" | tail -20

echo ""

# Check Redis memory usage
echo "🔴 Redis Memory Usage:"
docker-compose exec redis redis-cli info memory | grep -E "used_memory|used_memory_peak|used_memory_rss"

echo ""

# Check database connections
echo "🗄️  Database Connections:"
docker-compose exec db psql -U postgres -d qhenterprises -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';"

echo ""

# Check cache hit rate
echo "🎯 Cache Statistics:"
docker-compose exec redis redis-cli info stats | grep -E "keyspace_hits|keyspace_misses"

echo ""
echo "📈 Performance Tips:"
echo "- Monitor response times above 2 seconds"
echo "- Check for memory leaks in containers"
echo "- Optimize database queries if slow queries detected"
echo "- Monitor cache hit rates (should be >80%)"
