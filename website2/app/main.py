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


# docker build -t fastapi:latest .
# docker run -p 9372:9372 fastapi:latest
# https://medium.com/@meetakoti.kirankumar/deploying-fastapi-web-application-in-aws-a1995675087d
handler = Mangum(app=app)

# curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@package.sh" https://kx0v87byqj.execute-api.us-east-1.amazonaws.com/dev/v1/uploadfile
