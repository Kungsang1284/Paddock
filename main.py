from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import duckdb

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# DuckDBファイル接続（永続化したければファイル名指定）
con = duckdb.connect(database='comments.duckdb')

# テーブル作成（最初だけ）
con.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

@app.get("/", response_class=HTMLResponse)
async def get_comments(request: Request):
    rows = con.execute("SELECT message, created_at FROM comments ORDER BY created_at DESC").fetchall()
    return templates.TemplateResponse("chat.html", {"request": request, "comments": rows})

@app.post("/comment", response_class=HTMLResponse)
async def post_comment(request: Request, message: str = Form(...)):
    con.execute("INSERT INTO comments (message) VALUES (?)", [message])
    rows = con.execute("SELECT message, created_at FROM comments ORDER BY created_at DESC").fetchall()
    return templates.TemplateResponse("chat.html", {"request": request, "comments": rows})
