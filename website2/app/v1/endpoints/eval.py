import os
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/uploadfile", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    # Process results here, place in results var
    # Should use async if at all possible, following
    # https://fastapi.tiangolo.com/async/
    f = open("images/image.png", "wb+")
    f.write(file.file.read())
    result = os.popen("python3 run_model.py images/image.png")
    print("file recieved: ", file.filename)
    results = {"filename": file.filename, "type": file.content_type, "result": result.read()}
    return templates.TemplateResponse("results.html", {"request":request, "results": results})
