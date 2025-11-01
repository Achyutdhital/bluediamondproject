## 🚀 Quick Fix for PythonAnywhere Static Files

### The Problem
CSS, JavaScript, carousel buttons, and mobile menu not working on PythonAnywhere but work locally.

### The Solution (5 Steps)

#### 1. SSH into PythonAnywhere and navigate to project:
```bash
cd ~/bluediamond
git pull origin main
source env/bin/activate
```

#### 2. Collect static files (MOST IMPORTANT):
```bash
cd core
python manage.py collectstatic --noinput
```

#### 3. Configure Static Files in PythonAnywhere Web Tab:

Click on **"Web"** tab → Scroll to **"Static files"** section → Add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR-USERNAME/bluediamond/core/staticfiles/` |
| `/media/` | `/home/YOUR-USERNAME/bluediamond/core/media/` |

Replace `YOUR-USERNAME` with your actual PythonAnywhere username!

#### 4. Verify WSGI Configuration:

Open WSGI file from Web tab, ensure it has:

```python
path = '/home/YOUR-USERNAME/bluediamond/core'
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
```

#### 5. Reload Web App:

Click the big green **"Reload"** button in Web tab.

---

### After Every Git Push

```bash
cd ~/bluediamond
git pull origin main
source env/bin/activate
cd core
python manage.py collectstatic --noinput
# Click Reload button in Web tab
```

---

### Still Not Working?

1. **Check Error Log**: Web tab → Log files → error.log
2. **Clear Browser Cache**: Ctrl+Shift+R or open incognito
3. **Check Browser Console**: Right-click → Inspect → Console (look for 404 errors)
4. **Verify permissions**:
   ```bash
   chmod -R 755 ~/bluediamond/core/staticfiles
   chmod -R 755 ~/bluediamond/core/media
   ```

See **PYTHONANYWHERE_SETUP.md** for complete guide.
