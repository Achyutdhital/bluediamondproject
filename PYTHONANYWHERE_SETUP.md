# PythonAnywhere Deployment Guide

## Complete Setup Instructions for Blue Diamond Service Center

### Step 1: Pull Latest Code
```bash
cd ~/bluediamond
git pull origin main
```

### Step 2: Activate Virtual Environment
```bash
cd ~/bluediamond
source env/bin/activate  # or: workon your-virtualenv-name
```

### Step 3: Install/Update Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Collect Static Files (CRITICAL!)
```bash
cd core
python manage.py collectstatic --noinput
```

### Step 5: Run Migrations
```bash
python manage.py migrate
```

### Step 6: Configure WSGI File

Open your WSGI configuration file at:
`/var/www/your-username_pythonanywhere_com_wsgi.py`

Replace its contents with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/your-username/bluediamond/core'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where settings are
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# Activate your virtual env
activate_this = '/home/your-username/bluediamond/env/bin/activate_this.py'
# For Python 3.6+, use:
exec(open(activate_this).read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `your-username` with your actual PythonAnywhere username!**

### Step 7: Configure Static Files Mapping

In PythonAnywhere Web tab, add these static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/your-username/bluediamond/core/staticfiles/` |
| `/media/` | `/home/your-username/bluediamond/core/media/` |

**IMPORTANT**: Replace `your-username` with your actual username!

### Step 8: Update Django Settings

Edit `core/settings.py` on PythonAnywhere:

```python
# At the top, add:
import os

# Update these settings:
DEBUG = False  # IMPORTANT: Set to False in production!

ALLOWED_HOSTS = ['your-username.pythonanywhere.com', 'www.yourdomain.com']

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add this for better security:
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

### Step 9: Set Correct Permissions
```bash
chmod -R 755 ~/bluediamond/core/staticfiles
chmod -R 755 ~/bluediamond/core/media
```

### Step 10: Reload Web App

1. Go to PythonAnywhere Web tab
2. Click the green **"Reload your-username.pythonanywhere.com"** button
3. Wait 30-60 seconds for reload to complete

### Step 11: Clear Browser Cache

After reload, **clear your browser cache** or open in incognito/private mode to see the changes.

---

## Troubleshooting

### Static Files Not Loading

1. **Verify collectstatic ran successfully:**
   ```bash
   cd ~/bluediamond/core
   python manage.py collectstatic --noinput
   ls staticfiles/  # Should show dashboard/, app/, admin/ folders
   ```

2. **Check static file mappings in Web tab:**
   - URL: `/static/`
   - Directory: `/home/your-username/bluediamond/core/staticfiles/`
   - Must match exactly!

3. **Check file permissions:**
   ```bash
   chmod -R 755 ~/bluediamond/core/staticfiles
   ```

4. **Check WSGI configuration:**
   - Ensure DJANGO_SETTINGS_MODULE points to `core.settings`
   - Ensure path includes `/home/your-username/bluediamond/core`

### CSS/JS Not Working but Loading

If files load but CSS doesn't apply:

1. **Check MIME types** - PythonAnywhere should handle this automatically
2. **Hard refresh browser** - Press Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
3. **Check for mixed content** - Ensure all URLs use https:// if site is https://

### Mobile Menu Not Showing

This is usually a JavaScript issue:

1. **Check browser console for errors:**
   - Right-click → Inspect → Console tab
   - Look for 404 errors on .js files

2. **Verify Bootstrap JS is loading:**
   ```bash
   ls ~/bluediamond/core/staticfiles/app/vendors/js/bootstrap.bundle.min.js
   ```

3. **Check jQuery is loaded before Bootstrap:**
   - In base.html, jQuery must come before Bootstrap JS

### Images Not Showing

1. **Check media file mapping:**
   - URL: `/media/`
   - Directory: `/home/your-username/bluediamond/core/media/`

2. **Check permissions:**
   ```bash
   chmod -R 755 ~/bluediamond/core/media
   ```

3. **Re-upload images through admin** if they were uploaded locally

---

## Quick Deployment Checklist

Every time you push changes:

- [ ] Git pull on PythonAnywhere
- [ ] Activate virtual environment
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Run `python manage.py migrate` (if models changed)
- [ ] Reload web app from Web tab
- [ ] Clear browser cache
- [ ] Test on mobile device

---

## Common Commands Reference

```bash
# Navigate to project
cd ~/bluediamond

# Activate environment
source env/bin/activate

# Pull latest changes
git pull origin main

# Collect static files
cd core
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Check for errors
python manage.py check

# View error log
tail -n 50 /var/log/your-username.pythonanywhere.com.error.log
```

---

## Important Notes

1. **NEVER commit `db.sqlite3`** to GitHub - it's in .gitignore
2. **Create new superuser** on PythonAnywhere after first deployment
3. **Upload media files** through admin panel on production
4. **Always run collectstatic** after pulling code changes
5. **Set DEBUG = False** in production for security
6. **Use environment variables** for sensitive data (SECRET_KEY, etc.)

---

## Support

If issues persist after following this guide:

1. Check PythonAnywhere error logs
2. Check browser console for JavaScript errors
3. Verify all file paths use absolute paths
4. Contact PythonAnywhere support with specific error messages
