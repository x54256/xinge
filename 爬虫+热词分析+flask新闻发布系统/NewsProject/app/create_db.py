import sys
sys.path.append("..")

from app import db

db.create_all()
