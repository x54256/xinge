from app import app
from .toutiao import toutiao

app.register_blueprint(toutiao, url_prefix='/toutiao')