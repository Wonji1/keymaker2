import sys

print(sys.path)

sys.path.append('/home/keona/keymaker/flask')
sys.path.append('/home/keona/keymaker/flask/lib/python3.7/site-packages')

print(sys.path)

from app import app as application
