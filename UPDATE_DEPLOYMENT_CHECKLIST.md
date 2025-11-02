# cPanel Update Deployment Checklist
**Date:** November 2, 2025  
**Purpose:** Update live site with recent SEO system changes

---

## 🔴 CRITICAL: What Changed Since Last Deployment

### Database Changes
- ✅ **Migration 0018**: SEO fields (meta_title, meta_description) now optional (blank=True)
- ⚠️ **Must run**: `python manage.py migrate` on server

### Code Changes
1. **app/models.py** - SEO model fields updated
2. **app/views.py** - All 13 views now inject SEO data
3. **app/templates/app/seo_meta.html** - Fixed field names (meta_title, meta_description, etc.)
4. **dashboard/views.py** - SEO validation logic updated (optional save)
5. **dashboard/templates/** - SEO management templates updated

---

## 📦 Pre-Deployment Steps (On Local Machine)

### Step 1: Test Everything Locally
```powershell
# Make sure dev server is running
cd "d:\Prabin bro freelance\bluediamond\core"
python manage.py runserver

# Test these pages in browser:
# - http://localhost:8000/ (home)
# - http://localhost:8000/blog/ (blog list)
# - http://localhost:8000/services/ (services)
# - http://localhost:8000/dashboard/ (login & check SEO management)
```

### Step 2: Create Deployment Package
```powershell
# Navigate to project root
cd "d:\Prabin bro freelance\bluediamond"

# Create a ZIP file containing:
# - core/ folder (entire folder)
# - passenger_wsgi.py
# - requirements.txt
# - .htaccess (if exists)

# EXCLUDE these:
# - env/ folder
# - db.sqlite3 (server has its own database)
# - .git/ folder
# - __pycache__/ folders
# - *.pyc files
```

**Quick PowerShell command to create ZIP (excluding unwanted files):**
```powershell
Compress-Archive -Path "core\*" -DestinationPath "bluediamond-update.zip" -Force
```

---

## 🚀 Deployment Steps (On cPanel)

### Step 1: Backup Current Site
⚠️ **DO THIS FIRST - Critical!**

1. **Backup Database:**
   ```bash
   cd /home/camhsano/bluediamondservicecenter/core
   cp db.sqlite3 db.sqlite3.backup_nov2_2025
   ```

2. **Backup Media Files:**
   ```bash
   cd /home/camhsano/bluediamondservicecenter/core
   tar -czf media_backup_nov2.tar.gz media/
   ```

3. **Download backups to your local machine via cPanel File Manager**

### Step 2: Upload Updated Files

1. **Go to cPanel File Manager**
2. **Navigate to:** `/home/camhsano/bluediamondservicecenter/`
3. **Upload:** `bluediamond-update.zip`
4. **Extract:** Right-click ZIP → Extract
5. **Replace files when prompted** ✅

### Step 3: Update Dependencies (If Changed)

In **cPanel Python App Terminal** or **SSH**:
```bash
cd /home/camhsano/bluediamondservicecenter
source /home/camhsano/virtualenv/bluediamondservicecenter/3.11/bin/activate
pip install -r requirements.txt --upgrade
```

### Step 4: Run Database Migration 🔴 CRITICAL

```bash
cd /home/camhsano/bluediamondservicecenter/core
python manage.py migrate
```

**Expected output:**
```
Running migrations:
  Applying app.0018_alter_seo_meta_description_alter_seo_meta_title... OK
```

### Step 5: Collect Static Files

```bash
cd /home/camhsano/bluediamondservicecenter/core
python manage.py collectstatic --noinput
```

### Step 6: Clear Python Cache

```bash
cd /home/camhsano/bluediamondservicecenter
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
```

### Step 7: Restart Application

1. **Go to cPanel → Python App**
2. **Find your application**
3. **Click "RESTART"** button
4. **Wait 30 seconds**

---

## ✅ Post-Deployment Testing

### Test 1: Site Loading
- Visit: `https://yourdomain.com`
- Check: Homepage loads without errors
- Check: No 500 errors in browser console

### Test 2: SEO Meta Tags
1. Visit any page (e.g., homepage, blog post, service)
2. **Right-click → View Page Source**
3. **Search for:** `<meta name="description"`
4. **Verify:** Description appears correctly
5. **Search for:** `<meta property="og:title"`
6. **Verify:** Open Graph tags present

### Test 3: Dashboard SEO Management
1. Login: `https://yourdomain.com/dashboard/`
2. Go to: **SEO Management → Global SEO Settings**
3. **Verify:** All fields visible (site name, default title, meta description, etc.)
4. Go to: **SEO Management → SEO Metadata**
5. **Verify:** List shows meta titles and schema types
6. **Test:** Edit a service → SEO accordion → Leave empty → Save
7. **Expected:** Saves successfully (no errors)

### Test 4: Content Pages
- ✅ Blog list page loads
- ✅ Individual blog post shows correct title in browser tab
- ✅ Services page loads
- ✅ Individual service shows correct meta description
- ✅ Training courses page works
- ✅ About, Contact, Gallery pages load

---

## 🔧 Troubleshooting

### Issue: "No migrations to apply" but expecting 0018
**Solution:**
```bash
python manage.py showmigrations app
# Check if [X] 0018_alter_seo_meta_description_alter_seo_meta_title appears
# If it's already [X], migration is applied (good!)
```

### Issue: 500 Internal Server Error
**Solution:**
1. Check error logs in cPanel
2. Verify `passenger_wsgi.py` has correct paths
3. Check `settings.py` has correct `ALLOWED_HOSTS`
4. Restart Python app again

### Issue: SEO fields still required in dashboard
**Solution:**
1. Verify migration 0018 applied: `python manage.py showmigrations app`
2. If not applied, run: `python manage.py migrate`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Restart Python app

### Issue: Static files not loading (CSS/JS broken)
**Solution:**
```bash
cd /home/camhsano/bluediamondservicecenter/core
python manage.py collectstatic --noinput --clear
```
Then restart Python app

### Issue: Database errors about missing columns
**Solution:**
```bash
# Check current migration state
python manage.py showmigrations

# If migrations out of sync, try:
python manage.py migrate --fake-initial
```

---

## 📝 Quick Reference Commands

### Navigate to project:
```bash
cd /home/camhsano/bluediamondservicecenter/core
```

### Activate virtual environment:
```bash
source /home/camhsano/virtualenv/bluediamondservicecenter/3.11/bin/activate
```

### Check migration status:
```bash
python manage.py showmigrations app
```

### Apply migrations:
```bash
python manage.py migrate
```

### Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Check Python/Django version:
```bash
python --version
python -c "import django; print(django.get_version())"
```

---

## 🎯 Summary of Changes

### What's New:
1. ✅ SEO fields are now truly optional in dashboard forms
2. ✅ All public pages now have proper SEO meta tags
3. ✅ Schema markup (structured data) outputs on blog/service/course pages
4. ✅ Global SEO Settings page now shows all fields
5. ✅ SEO Management list shows meta titles and schema types
6. ✅ Open Graph and Twitter Card tags are dynamic per page

### What Users Will Notice:
- **Dashboard users:** Can save services/blogs without filling SEO fields
- **Visitors:** Better search engine results with proper meta descriptions
- **Social sharing:** Improved previews on Facebook/Twitter
- **Developers:** Cleaner admin interface, better structured data

---

## ⏱️ Estimated Time
- **Backup:** 5 minutes
- **Upload & Extract:** 5 minutes
- **Migration & Static Files:** 3 minutes
- **Restart & Test:** 5 minutes
- **Total:** ~20 minutes

---

## 🆘 Emergency Rollback

If something goes wrong:

1. **Restore database backup:**
   ```bash
   cd /home/camhsano/bluediamondservicecenter/core
   cp db.sqlite3.backup_nov2_2025 db.sqlite3
   ```

2. **Keep the old code backup** (don't delete until everything works)

3. **Contact support if migrations are corrupted**

---

**Last Updated:** November 2, 2025  
**Tested On:** Local development environment  
**Ready for Production:** ✅ Yes
