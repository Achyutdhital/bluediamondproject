"""
Django core package initialization
"""
import os

# Use PyMySQL as a replacement for mysqlclient when USE_MYSQL is enabled
if os.environ.get('USE_MYSQL', 'False') == 'True':
    try:
        import pymysql  # type: ignore
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
