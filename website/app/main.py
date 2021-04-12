from typing import Optional
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

tasks = {1:{"task_name": "do stuff", "status":False}}
ntasks = 1

@app.get("/")
async def main():
    with open("index.html", "r") as f:
        content = f.read()
        return HTMLResponse(content=content)

@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    # Process results here, place in results var
    # Should use async if at all possible, following
    # https://fastapi.tiangolo.com/async/
    results = {"test": "Hello, world!"}
    return templates.TemplateResponse("results.html", {"request":request, "results": results})
