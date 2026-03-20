import os
from dotenv import load_dotenv

load_dotenv() # .env dosyasındaki verileri yükler
db_pass = os.getenv("DB_PASSWORD")
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import cv2

app = FastAPI()

# 1. GÜVENLİK AYARI (CORS): Tarayıcının API'ye erişebilmesi için şart
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. STATİK DOSYALAR: 'ihlaller' klasöründeki fotoğrafları dışarı açıyoruz
app.mount("/ihlaller", StaticFiles(directory="ihlaller"), name="ihlaller")

# 3. VERİTABANI BAĞLANTISI
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres", 
        user="ozge", 
        password="db_pass", 
        host="127.0.0.1", 
        port="5432"
    )

# 4. CANLI YAYIN MOTORU (Video Streaming)
def generate_frames():
    # 0 genellikle dahili kameradır, dış kamera varsa 1 denenebilir
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Görüntüyü JPEG formatına sıkıştırıyoruz
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # HTTP üzerinden parça parça (Multipart) gönderiyoruz
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# --- ENDPOINT'LER ---

@app.get("/")
def home():
    return {"mesaj": "Özge AI Güvenlik Sistemi API Aktif! 🚀"}

@app.get("/veriler")
def get_violations():
    """Veritabanındaki tüm ihlalleri listeler"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM violations ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        return {"hata": str(e)}

@app.get("/video_feed")
def video_feed():
    """Canlı kamera görüntüsünü tarayıcıya akıtır"""
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")