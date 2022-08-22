from datetime import datetime
import secrets
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse
import os
import aiofiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ml import CLASSES, img_preprocess, explain_image, model

app = FastAPI()

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
ORIGIN_IMG_DIR = os.path.join(BASE_DIR, 'static', 'originImg/')
LIME_IMG_DIR = os.path.join(BASE_DIR, 'static', 'limeImg/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','originImg/')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


templates = Jinja2Templates(directory='static')
app.mount('/static', StaticFiles(directory='static'), name='static')

app = FastAPI()

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

# return: "[Date][random str].png"
def get_filename() -> str:
    cur_time = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = ''.join([cur_time, secrets.token_hex(16)]) + '.png'
    return filename

@app.post('/files/')
async def upload_file(file: UploadFile):
    filename = get_filename()
    origin_file_path = os.path.join(ORIGIN_IMG_DIR, filename)
    lime_file_path = os.path.join(LIME_IMG_DIR, filename)

    async with aiofiles.open(origin_file_path, 'wb+') as buffer:
        img = await file.read()
        await buffer.write(img)
    
    img = img_preprocess(origin_file_path)
    pred = list(map(float, model.predict(img)[0]))
    pred = {label: prob for label, prob in zip(CLASSES, pred)}
    explain_image(img[0], lime_file_path)

    return {
        'origin_file_path': os.path.join('/static/originImg', filename), 
        'lime_file_path': os.path.join('/static/limeImg', filename),
        'predict': pred}


@app.get("/static/{file_name}")
async def main(file_name: str):
    return FileResponse(os.path.join(STATIC_DIR, file_name))

@app.get("/static/originImg/{file_name}")
async def main(file_name: str):
    return FileResponse(os.path.join(STATIC_DIR, 'originImg', file_name))

@app.get("/static/limeImg/{file_name}")
async def main(file_name: str):
    return FileResponse(os.path.join(STATIC_DIR, 'limeImg', file_name))
