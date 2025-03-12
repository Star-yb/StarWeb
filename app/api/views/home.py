from fastapi import Request,APIRouter

from fastapi.responses import HTMLResponse
from app.core.events.templates import templates
from app.settings.config import APP_NAME, APP_DESCRIPTION

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
# 任意定义两个参数，非必传
async def home(request: Request):
    """
    主页视图
    """
    #     # 解析访问令牌
    # parser = TokenParser()
    # parser.analyze_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIsInN1YiI6ImFkbWluIiwic2NvcGVzIjpbXSwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTczODI1Nzc3NH0.yJJfRjLeXzQr_K_pAaiSQ_-qfEwTzPAOpvZPN5ep30I")

    # # 解析刷新令牌
    # parser.analyze_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIsInN1YiI6ImFkbWluIiwic2NvcGVzIjpbXSwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3Mzg4NjA3NzR9.UznSt8hCAYwzjSM7Hs3spb3M0bxxQeYOF5XQfY3JOwA")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": APP_NAME,
            "description": APP_DESCRIPTION
        }
    )



