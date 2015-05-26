from project import create_app
import os

app = create_app(os.environ["APP_SETTINGS"])