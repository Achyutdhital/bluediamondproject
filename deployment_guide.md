# cPanel Deployment Guide for Blue Diamond Project

## Files to Upload
Create a ZIP file containing ONLY these folders/files from your project:
- `core/` (entire folder)
- `passenger_wsgi.py`
- `.htaccess`
- `requirements.txt`

**DO NOT UPLOAD:**
- `env/` folder (virtual environment)
- `db.sqlite3` (you'll create new database on server)
- `.git/` folder
- `__pycache__/` folders

## Step-by-Step Deployment

### 1. Create Python App in cPanel
- Go to cPanel → Python App
- Click "Create Application"
- Python version: 3.11 (or latest available)
- Application root: `/home/camhsano/bluediamondservicecenter`
- Application URL: Leave blank for main domain or enter subdirectory
- Application startup file: `passenger_wsgi.py`
- Application Entry point: `application`

### 2. Upload Files
- Extract your ZIP file to `/home/camhsano/bluediamondservicecenter/`
- Make sure `passenger_wsgi.py` is in the root directory

### 3. Install Dependencies
In cPanel Python App terminal or SSH:
```bash
pip install -r requirements.txt
```

### 4. Update Configuration Files

#### Edit `passenger_wsgi.py`:
Replace `yourdomain.com` with your actual domain name

#### Edit `.htaccess`:
Already configured for: `/home/camhsano/bluediamondservicecenter`

### 5. Set Environment Variables
In cPanel Python App → Environment Variables:
- `DJANGO_DEBUG` = `False`
- `DJANGO_ALLOWED_HOSTS` = `yourdomain.com,www.yourdomain.com`
- `DJANGO_SECRET_KEY` = `your-secret-key-here`

### 6. Database Setup
Run these commands ONE BY ONE in terminal:
```bash
cd /home/camhsano/bluediamondservicecenter/core
python manage.py migrate
```
If migrate fails, try:
```bash
python manage.py makemigrations
python manage.py migrate
```
Then:
```bash
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 7. Media Files Setup
Create media directory and set permissions:
```bash
mkdir -p /home/camhsano/bluediamondservicecenter/core/media
chmod 755 /home/camhsano/bluediamondservicecenter/core/media
```

### 8. Restart Application
In cPanel Python App, click "Restart" button

## Troubleshooting

### Script Exit Code 2 Errors:
1. **Check current directory**: Make sure you're in `/home/camhsano/bluediamondservicecenter/core`
2. **Check Python path**: Use `which python` to verify correct Python version
3. **Run commands individually**: Don't run multiple commands at once
4. **Check file permissions**: Run `ls -la` to check if files are readable

### Common Issues:
- If 500 error: Check error logs in cPanel
- If static files not loading: Run `python manage.py collectstatic`
- If images not showing: Check media folder permissions
- If login fails: Create superuser again with `python manage.py createsuperuser`
- If migration fails: Delete `db.sqlite3` and run migrations again

## Important Notes
- Your site will be available at: `https://yourdomain.com`
- Admin dashboard: `https://yourdomain.com/dashboard/`
- Always backup your database before updates
- Use environment variables for sensitive settings