import os
from dotenv import load_dotenv

load_dotenv() # .env dosyasındaki verileri yükler
db_pass = os.getenv("DB_PASSWORD")

from ultralytics import YOLO
import cv2
import torch
import os
import psycopg2
from datetime import datetime
import numpy as np

# 1. KLASÖR VE VERİTABANI HAZIRLIĞI
if not os.path.exists('ihlaller'):
    os.makedirs('ihlaller')

def save_to_db(object_id, object_type, image_path):
    try:
        conn = psycopg2.connect(
            dbname="postgres", user="ozge", password="db_pass", 
            host="127.0.0.1", port="5432"
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS violations (
                id SERIAL PRIMARY KEY,
                object_id INTEGER,
                object_type TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("INSERT INTO violations (object_id, object_type, image_path) VALUES (%s, %s, %s)",
                    (object_id, object_type, image_path))
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ DB Kaydı Başarılı: {object_type}")
    except Exception as e:
        print(f"❌ DB Hatası: {e}")

# 2. SEGMENTASYON MODELİ VE AYARLAR
device = 'mps' if torch.backends.mps.is_available() else 'cpu'
# 'yolov8n-seg.pt' modelini kullanarak nesneleri maskeliyoruz
model = YOLO('yolov8n-seg.pt') 
cap = cv2.VideoCapture(0)
line_x = 640  # Dikey çizgi konumu
already_saved = set()

print("🚀 Havalimanı Modu Aktif: Segmentation & Dikey Analiz Başladı!")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # Nesne Takibi ve Maskeleme
    results = model.track(frame, persist=True, device=device, verbose=False)

    # Eğer maskeler veya kutular varsa görselleştirme yap
    if results[0].boxes is not None:
        # results[0].plot() otomatik olarak hem kutuları hem maskeleri çizer
        frame = results[0].plot()

    # --- GÖRSEL KATMANLAR (Havalimanı Teması) ---
    cv2.line(frame, (line_x, 0), (line_x, 720), (56, 189, 248), 3) # Cam göbeği çizgi
    cv2.putText(frame, "HAVALIMANI GUVENLIK SINIRI", (line_x + 10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (56, 189, 248), 2)

    # --- ANALİZ VE KAYIT MANTIĞI ---
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy()
        cls = results[0].boxes.cls.cpu().numpy()

        for box, id, c in zip(boxes, ids, cls):
            x1, y1, x2, y2 = box
            cx = int((x1 + x2) / 2) # Nesne merkezi
            obj_name = model.names[int(c)]

            # KRİTİK KONTROL: SADECE ÇİZGİYİ GEÇTİYSE
            if cx > line_x:
                cv2.putText(frame, f"ALARM: {obj_name.upper()}", (int(x1), int(y1) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
                # DAHA ÖNCE KAYDEDİLMEDİYSE KAYDET
                if id not in already_saved:
                    timestamp = datetime.now().strftime("%H%M%S")
                    img_name = f"ihlaller/{obj_name}_id{int(id)}_{timestamp}.jpg"
                    
                    cv2.imwrite(img_name, frame)
                    save_to_db(int(id), obj_name, img_name)
                    
                    already_saved.add(id)
                    print(f"⚠️ {obj_name} yakalandı! Fotoğraf: {img_name}")

    # Tespit Sayısını Yazdır
    cv2.putText(frame, f"Aktif Analiz: {len(results[0].boxes)} Nesne", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Ozge AI - Airport Surveillance Pro", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()