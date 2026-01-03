# 🔧 FIX EMAIL CONFIGURATION - Step by Step

Your email is still using console backend. Follow these steps:

## Step 1: Check Your .env File

Make sure your `.env` file (in the project root) has these lines:

```env
EMAIL_USE_SMTP=True
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@qhenterprises.com
EMAIL_HOST_PASSWORD=your-actual-password
DEFAULT_FROM_EMAIL=your-email@qhenterprises.com
```

**Important**: 
- Replace `your-email@qhenterprises.com` with your actual Hostinger email
- Replace `your-actual-password` with your actual email password
- Make sure `EMAIL_USE_SMTP=True` (not `False` or commented out)

## Step 2: Verify .env File Location

The `.env` file must be in the **project root** (same directory as `docker-compose.yml`):

```
QnH-Enterprises/
├── .env              ← Must be here!
├── docker-compose.yml
├── Dockerfile
└── core/
```

## Step 3: Check Current Configuration

Run this command to see what Docker is reading:

```bash
docker-compose exec web python check_email_config.py
```

This will show you:
- What environment variables are set
- Whether `.env` file is being read
- What email backend will be used

## Step 4: Restart Docker Container

After adding/updating `.env` file, you MUST restart:

```bash
# Stop containers
docker-compose down

# Start again (this reloads .env file)
docker-compose up --build
```

Or if containers are running:

```bash
# Restart web service
docker-compose restart web
```

## Step 5: Verify It's Working

After restart, check the terminal output. You should see:

```
Email Backend: SMTP
Email Host: smtp.hostinger.com:587
Email User: your-email@qhenterprises.com
From Email: your-email@qhenterprises.com
```

**NOT**:
```
Email Backend: Console (emails will be printed to terminal)
```

## Common Issues

### Issue 1: Still seeing "Console" after restart

**Solution**: 
1. Check `.env` file has `EMAIL_USE_SMTP=True` (no spaces, no quotes)
2. Make sure `.env` is in project root
3. Try: `docker-compose down` then `docker-compose up --build`

### Issue 2: .env file not found

**Solution**:
- Make sure file is named exactly `.env` (not `.env.txt` or `env`)
- Check it's in the same directory as `docker-compose.yml`
- On Windows, make sure it's not hidden

### Issue 3: Environment variable not being read

**Solution**:
- Check for typos: `EMAIL_USE_SMTP` (not `EMAIL_USE_STMP` or `EMAIL_USE_SMTP`)
- Make sure there are no spaces: `EMAIL_USE_SMTP=True` (not `EMAIL_USE_SMTP = True`)
- Don't use quotes: `EMAIL_USE_SMTP=True` (not `EMAIL_USE_SMTP="True"`)

### Issue 4: Docker not picking up changes

**Solution**:
- Always restart containers after changing `.env`
- Use `docker-compose down` then `docker-compose up --build` for a clean restart
- Check if you're editing the right `.env` file (there might be multiple)

## Quick Test

After fixing, test the email:

```bash
# Using curl
curl -X POST http://localhost:8000/api/orders/test-email/ \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@gmail.com"}'
```

Then check your email inbox (and spam folder)!

## Still Not Working?

1. Run diagnostic: `docker-compose exec web python check_email_config.py`
2. Check Docker logs: `docker-compose logs web | grep -i email`
3. Verify `.env` file format (no BOM, Unix line endings)
4. Make sure you're editing the `.env` file in the project root, not inside `core/` directory

