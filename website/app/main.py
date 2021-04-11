from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

tasks = {1:{"task_name": "do stuff", "status":False}}
ntasks = 1

@app.get("/")
async def main():
    with open("index.html", "r") as f:
        content = f.read()
        return HTMLResponse(content=content)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
