from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from v1.routers import router

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(router, prefix="/v1")


@app.get("/")
async def main():
    with open("index.html", "r") as f:
        content = f.read()
        print("get recieved")
        return HTMLResponse(content=content)


# https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9
handler = Mangum(app=app)

# curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@image.png" https://kx0v87byqj.execute-api.us-east-1.amazonaws.com/dev/v1/uploadfile
