from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
page_router = APIRouter()


@page_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
