import base64
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import run_model_lite

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/uploadfile", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    # Process results here, place in results var
    # Should use async if at all possible, following
    # https://fastapi.tiangolo.com/async/
    # filename = file.filename
    # await file.close()
    # f.close()
    print("file recieved: ", file.filename)
    print("content type: ", file.content_type)
    bytes = await file.read()
    if len(bytes) > 500000:
        bytes = base64.decode(bytes)
    print("File length: ", len(bytes))
    result = run_model_lite.predict_image(bytes)
    results = {"filename": file.filename, "result": result}
    await file.close()
    return templates.TemplateResponse("results.html", {"request":request, "results": results})
