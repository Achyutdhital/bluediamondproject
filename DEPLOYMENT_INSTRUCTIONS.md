# cPanel Deployment Instructions - Media Files Fix

## The Problem
Images not loading because media files need special configuration on cPanel/Passenger.

## The Solution
Updated `.htaccess` and `urls.py` to properly serve media files in production.

---

## Quick Deployment Steps

### 1. Push Changes to GitHub
```powershell
cd "d:\Prabin bro freelance\bluediamond"
git add .
git commit -m "Fix: Configure media file serving for cPanel production"
git push
```

### 2. On cPanel - Pull and Setup

**Option A: Via cPanel Terminal**
```bash
cd /home/camhsano/bluediamondservicecenter
git pull origin main
cd core
python manage.py collectstatic --noinput
cd ..
touch tmp/restart.txt
```

**Option B: If uploading ZIP instead**
1. Create ZIP with: `core/`, `passenger_wsgi.py`, `.htaccess`, `requirements.txt`
2. Upload to `/home/camhsano/bluediamondservicecenter/`
3. Extract (overwrite existing files)
4. Run commands below

### 3. Verify Media Directory Structure
```bash
cd /home/camhsano/bluediamondservicecenter/core
ls -la media/
```

You should see folders like:
- `media/blog/`
- `media/brands/`
- `media/gallery/`
- `media/Services/`
- `media/training_courses/`
- `media/media/` (nested folder from admin uploads)

### 4. Set Permissions (Important!)
```bash
cd /home/camhsano/bluediamondservicecenter/core
chmod -R 755 media/
find media/ -type f -exec chmod 644 {} \;
```

### 5. Test Media Access
Try accessing a media file directly in browser:
```
https://bluediamondservicecenter.com/media/media/companydetails/logos/Bluediamond_Trades.jpg
```

If you get 404, check:
1. File actually exists on server
2. Permissions are correct (755 for dirs, 644 for files)
3. Path in `.htaccess` matches actual server path

---

## What Changed

### 1. `.htaccess` (Root directory)
- Added RewriteRules to serve `/media/` files directly
- Added `/static/` file serving
- Configured proper MIME types
- Added caching headers
- Added HTTPS redirect

### 2. `core/core/urls.py`
- Updated media serving to work in both DEBUG and production modes

---

## Troubleshooting

### Images Still Not Loading?

**Check 1: Verify file paths on server**
```bash
cd /home/camhsano/bluediamondservicecenter/core/media
ls -R
```

**Check 2: Check .htaccess is in the right place**
```bash
cd /home/camhsano/bluediamondservicecenter
ls -la .htaccess
```

**Check 3: Verify paths in .htaccess match your server**
The paths should be:
- `/home/camhsano/bluediamondservicecenter/core/staticfiles/`
- `/home/camhsano/bluediamondservicecenter/core/media/`

**Check 4: Check Python App settings in cPanel**
- Application root: `/home/camhsano/bluediamondservicecenter`
- Python version: 3.11
- Application startup file: `passenger_wsgi.py`

**Check 5: Restart the app**
```bash
touch /home/camhsano/bluediamondservicecenter/tmp/restart.txt
```

Or in cPanel → Python App → Click "Restart"

### If Using Database with Media Paths

If your database has full paths like `/home/user/...`, you need to:
1. Export database
2. Find/Replace old paths with new ones
3. Re-import

Or use Django shell:
```bash
cd /home/camhsano/bluediamondservicecenter/core
python manage.py shell
```

Then update paths programmatically if needed.

---

## Alternative: Create Symbolic Link

If images are uploaded to a different location, create a symlink:
```bash
cd /home/camhsano/public_html
ln -s /home/camhsano/bluediamondservicecenter/core/media media
ln -s /home/camhsano/bluediamondservicecenter/core/staticfiles static
```

Then update `.htaccess` accordingly.

---

## Files Changed in This Update
- `.htaccess` - Complete rewrite with media/static serving
- `core/core/urls.py` - Updated media serving configuration
- This guide - Instructions for deployment

## Commands Summary
```bash
# Quick deployment
cd /home/camhsano/bluediamondservicecenter
git pull origin main
chmod -R 755 core/media/
find core/media/ -type f -exec chmod 644 {} \;
cd core
python manage.py collectstatic --noinput
cd ..
touch tmp/restart.txt
```
