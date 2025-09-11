from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_action(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret":
        response = RedirectResponse("/", status_code=303)
        response.set_cookie("user", username)
        return response
    return RedirectResponse("/login", status_code=303)