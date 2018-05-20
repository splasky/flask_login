import sys
import logging
 
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/apache-flask/flask_login")
 
from src.app import app as application 
# application.secret_key = ''
