from datetime import datetime
import secrets
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import FileResponse
from path import *
import aiofiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ml import CLASSES, img_preprocess, explain_image, model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

templates = Jinja2Templates(directory="dist")
app.mount('/dist', StaticFiles(directory='dist'), name='dist')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

# return: "[Date][random str].png": str
def get_filename() -> str:
    cur_time = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = ''.join([cur_time, secrets.token_hex(16)]) + '.png'
    return filename

@app.post('/files/')
async def post_file(file: UploadFile) -> dict:
    filename = get_filename()
    filepath = os.path.join(ORIGIN_IMG_DIR, filename)

    async with aiofiles.open(filepath, 'wb+') as buffer:
        img = await file.read()
        await buffer.write(img)

    return {'filename': filename}

@app.get("/predict/{filename}")
async def predict(filename: str) -> dict:
    lime_file_path = os.path.join(LIME_IMG_DIR, filename)
    filename = os.path.join(ORIGIN_IMG_DIR, filename)
    img = img_preprocess(filename)
    pred = list(map(float, model.predict(img)[0]))
    pred = {label: prob for label, prob in zip(CLASSES, pred)}
    explain_image(img[0], lime_file_path)
    print("limefilepath=", lime_file_path)
    return {'pred': pred}

@app.get("/static/{filename}")
async def get_static_file(filename: str) -> FileResponse:
    return FileResponse(os.path.join(STATIC_DIR, filename))

@app.get("/static/originImg/{filename}")
async def get_origin_img(filename: str) -> FileResponse:
    return FileResponse(os.path.join(STATIC_DIR, 'originImg', filename))

@app.get("/static/limeImg/{filename}")
async def get_lime_img(filename: str) -> FileResponse:
    return FileResponse(os.path.join(STATIC_DIR, 'limeImg', filename))

@app.get("/{filename}")
async def get_dist(filename: str) -> FileResponse:
    return FileResponse(os.path.join(DIST_DIR, filename))

@app.get("/assets/{filename}")
async def get_dist_assets(filename: str) -> FileResponse:
    return FileResponse(os.path.join(DIST_DIR, "assets", filename))
