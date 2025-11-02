import os
import sys
import traceback
from datetime import datetime

# Resolve absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure the app root and the outer "core" folder (which contains manage.py and the inner package) are on PYTHONPATH
if BASE_DIR not in sys.path:
	sys.path.insert(0, BASE_DIR)

PROJECT_DIR = os.path.join(BASE_DIR, 'core')
if PROJECT_DIR not in sys.path:
	sys.path.insert(0, PROJECT_DIR)

# Set environment variables for production (can be overridden via cPanel UI)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('DJANGO_DEBUG', 'False')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', 'bluediamondservicecenter.com,www.bluediamondservicecenter.com')

# Initialize the WSGI application with basic startup error logging to Passenger stderr
try:
	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()
except Exception:  # Log the traceback to help diagnose 503s
	sys.stderr.write("\n[Passenger][WSGI] Application failed to start. Traceback follows:\n")
	trace = ''.join(traceback.format_exc())
	sys.stderr.write(trace)
	sys.stderr.write("\n")
	# Fallback: also write to a file in the application root so it can be viewed via File Manager
	try:
		log_path = os.path.join(BASE_DIR, 'passenger_startup_error.log')
		with open(log_path, 'a', encoding='utf-8') as f:
			f.write("\n=== {} UTC ===\n".format(datetime.utcnow().isoformat()))
			f.write(trace)
			f.write("\n")
	except Exception:
		pass
	raise