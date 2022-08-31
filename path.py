import os

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'whatisbreed-backend')
ORIGIN_IMG_DIR = os.path.join(BASE_DIR, 'static', 'originImg/')
LIME_IMG_DIR = os.path.join(BASE_DIR, 'static', 'limeImg/')
SERVER_IMG_DIR = os.path.join(
    'http://localhost:8000/', 'static/', 'originImg/')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DIST_DIR = os.path.join(BASE_DIR, 'dist')
