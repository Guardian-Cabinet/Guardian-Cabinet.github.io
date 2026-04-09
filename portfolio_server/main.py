from fastapi import FastAPI, Form, Request, File, UploadFile, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import shutil
import uuid
from datetime import datetime

app = FastAPI(title="Portfolio CMS")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Moves UPLOADS and STATIC one level up to the root c:\anti\homepage\
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_FILE = os.path.join(BASE_DIR, "data.json")
VISITS_FILE = os.path.join(BASE_DIR, "visits.json")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOADS_DIR = os.path.join(ROOT_DIR, "static", "uploads")

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "static")), name="static")


# ──────────────── Data helpers ────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "content" in data:
                c = data["content"]
                if "careers" in c: c["careers"] = sorted(c["careers"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
                if "educations" in c: c["educations"] = sorted(c["educations"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
                if "trainings" in c: c["trainings"] = sorted(c["trainings"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
                if "activities" in c: c["activities"] = sorted(c["activities"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
                if "awards" in c: c["awards"] = sorted(c["awards"], key=lambda x: str(x.get("date", "")).replace(" ", ""), reverse=True)
            return data
    return {}

def load_secrets():
    secrets_file = os.path.join(BASE_DIR, "secrets.json")
    if os.path.exists(secrets_file):
        with open(secrets_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"admin_id": "admin", "pin": "1234"}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_visits():
    if os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_visits(visits):
    with open(VISITS_FILE, "w", encoding="utf-8") as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)


# ──────────────── Visitor Tracking helpers ────────────────
def get_client_ip(request: Request) -> str:
    """Get real client IP, considering proxy headers."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    return request.client.host if request.client else "unknown"


# ──────────────── Public Routes ────────────────
@app.get("/", response_class=HTMLResponse)
async def read_portfolio(request: Request):
    data = load_data()
    settings = data.get("settings", {})
    start_date_str = settings.get("valid_start", "2000-01-01")
    end_date_str = settings.get("valid_end", "2099-12-31")
    
    today = datetime.now().date()
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        start_date = today
        end_date = today

    if not (start_date <= today <= end_date):
        return templates.TemplateResponse(
            request=request,
            name="expired.html", 
            context={"request": request, "start": start_date_str, "end": end_date_str}
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={"request": request, "data": data}
    )


# ──────────────── Tracking API ────────────────
@app.post("/api/track/enter")
async def track_enter(request: Request):
    """방문자가 사이트에 처음 진입했을 때 호출"""
    body = await request.json()
    ip = get_client_ip(request)
    ua = request.headers.get("user-agent", "unknown")
    
    session_id = str(uuid.uuid4())[:8]
    visit = {
        "session_id": session_id,
        "ip": ip,
        "user_agent": ua,
        "entered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "left_at": None,
        "duration_seconds": 0,
        "pages_viewed": ["01 PROFILE"],
        "referrer": body.get("referrer", "direct")
    }
    
    visits = load_visits()
    visits.append(visit)
    # 최대 500건 유지 (오래된 것 삭제)
    if len(visits) > 500:
        visits = visits[-500:]
    save_visits(visits)
    
    return {"session_id": session_id}


@app.post("/api/track/page")
async def track_page(request: Request):
    """방문자가 특정 폴더(탭)를 열었을 때 호출"""
    body = await request.json()
    session_id = body.get("session_id")
    page = body.get("page", "")
    
    if not session_id:
        return {"ok": False}
    
    visits = load_visits()
    for v in reversed(visits):
        if v["session_id"] == session_id:
            if page not in v["pages_viewed"]:
                v["pages_viewed"].append(page)
            break
    save_visits(visits)
    return {"ok": True}


@app.post("/api/track/leave")
async def track_leave(request: Request):
    """방문자가 사이트를 떠날 때 체류 시간 기록"""
    body = await request.json()
    session_id = body.get("session_id")
    duration = body.get("duration", 0)
    
    if not session_id:
        return {"ok": False}
    
    visits = load_visits()
    for v in reversed(visits):
        if v["session_id"] == session_id:
            v["left_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            v["duration_seconds"] = duration
            break
    save_visits(visits)
    return {"ok": True}


# ──────────────── Authentication ────────────────
def is_authenticated(request: Request):
    """Check if the user is authenticated via cookie."""
    return request.cookies.get("admin_session") == "authenticated"

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@app.post("/login")
async def post_login(admin_id: str = Form(...), pin: str = Form(...)):
    secrets = load_secrets()
    stored_id = secrets.get("admin_id", "admin")
    stored_pin = secrets.get("pin", "1234")
    if admin_id == stored_id and pin == stored_pin:
        response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="admin_session", value="authenticated", httponly=True)
        return response
    return HTMLResponse("<h1>아이디 또는 비밀번호가 틀렸습니다.</h1><br><a href='/login'>다시 시도</a>", status_code=401)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("admin_session")
    return response


def generate_insight(visits):
    if not visits: return "현재 방문자 데이터가 부족하여 분석할 수 없습니다. 홍보를 통해 트래픽을 늘려주세요."
    
    valid_durations = [v.get("duration_seconds", 0) for v in visits if v.get("duration_seconds", 0) > 0]
    avg_duration = sum(valid_durations) / len(valid_durations) if valid_durations else 0
    
    tab_dropoffs = {}
    for v in visits:
        pages = v.get("pages_viewed", [])
        if pages:
            last_page = pages[-1]
            tab_dropoffs[last_page] = tab_dropoffs.get(last_page, 0) + 1
            
    worst_tab = max(tab_dropoffs, key=tab_dropoffs.get) if tab_dropoffs else "알 수 없음"
    
    insight = "💡 [AI 인사이트] "
    if avg_duration < 15:
        insight += f"방문자의 평균 체류 시간이 짧습니다({int(avg_duration)}초). 첫 화면인 PROFILE의 글을 좀 더 핵심만 보이게 요약해보세요. "
    else:
        insight += f"방문자들이 평균 {int(avg_duration)}초로 꽤 오래 머뭅니다. 포트폴리오의 실물 자료를 더 늘려도 좋습니다. "
        
    if worst_tab and worst_tab != "알 수 없음":
        insight += f"특히 '{worst_tab}' 탭에서 나가는(이탈) 비율이 가장 높습니다. 이 탭의 내용을 좀 더 매력적으로 수정해보세요."
        
    return insight

@app.get("/admin", response_class=HTMLResponse)
async def get_admin(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")
    data = load_data()
    visits = load_visits()
    insight_text = generate_insight(visits)
    return templates.TemplateResponse(
        request=request,
        name="admin.html", 
        context={"request": request, "data": data, "insight": insight_text}
    )

@app.get("/admin/visits", response_class=HTMLResponse)
async def get_visits(request: Request):
    """방문자 추적 대시보드"""
    if not is_authenticated(request):
        return RedirectResponse(url="/login")
    visits = load_visits()
    visits_sorted = sorted(visits, key=lambda x: x.get("entered_at", ""), reverse=True)
    return templates.TemplateResponse(
        request=request,
        name="visits_panel.html",
        context={"request": request, "visits": visits_sorted, "now": datetime.now()}
    )

@app.post("/admin/upload")
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        return {"error": "이미지 파일만 업로드 가능합니다."}
    
    filename = f"upload_{int(datetime.now().timestamp())}{ext}"
    filepath = os.path.join(UPLOADS_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"url": f"/static/uploads/{filename}"}

@app.post("/admin/save")
def save_admin(
    request: Request,
    pin: str = Form(...),
    json_data: str = Form(...)
):
    secrets = load_secrets()
    stored_pin = secrets.get("pin", "1234")
    
    if pin != stored_pin:
        return HTMLResponse("<h1>비밀번호(PIN)가 틀렸습니다.</h1><br><a href='/admin'>돌아가기</a>", status_code=403)
    
    try:
        new_data = json.loads(json_data)
        data = load_data()
        if "settings" not in new_data:
            new_data["settings"] = data.get("settings", {})
        
        # PIN과 admin_id가 data.json에 남지 않도록 제거 (보안)
        new_data["settings"].pop("pin", None)
        new_data["settings"].pop("admin_id", None)
             
        save_data(new_data)
        
        # AUTO-RENDER STATIC index.html AFTER SAVING
        try:
            import subprocess
            import sys
            subprocess.run([sys.executable, os.path.join(BASE_DIR, "..", "render_portfolio.py")], check=True)
            msg = "성공적으로 저장 및 정적 사이트가 갱신되었습니다!"
            
            # Github Auto commit and push
            try:
                root = os.path.join(BASE_DIR, "..")
                if os.path.exists(os.path.join(root, ".git")):
                    subprocess.run(["git", "add", "."], cwd=root, check=True)
                    subprocess.run(["git", "commit", "-m", "Auto-update from Admin CMS"], cwd=root, check=True)
                    # Try origin first, then fallback to upstream if needed
                    try:
                        subprocess.run(["git", "push", "origin", "main"], cwd=root, check=True)
                    except Exception:
                        subprocess.run(["git", "push", "upstream", "main"], cwd=root, check=True)
                    msg += " GitHub 동기화 완료!"
                else:
                    msg += " (Git 저장소가 초기화되지 않아 동기화를 건너뜁니다.)"
            except Exception as git_e:
                msg += " (GitHub 동기화 실패: " + str(git_e).replace("'", " ") + ")"
                
        except Exception as e:
            msg = "데이터는 저장되었으나 정적 갱신에 실패했습니다: " + str(e).replace("'", " ")

        return HTMLResponse(f"<script>alert('{msg}'); window.location.href='/admin';</script>")
    except Exception as e:
        return HTMLResponse(f"<h1>데이터 저장 오류</h1><p>{str(e)}</p><a href='/admin'>돌아가기</a>", status_code=400)


if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8081)
    except KeyboardInterrupt:
        pass
