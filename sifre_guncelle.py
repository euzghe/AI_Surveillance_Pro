import psycopg2

try:
    # Şifresiz veya eski yöntemle bağlanmayı dene
    conn = psycopg2.connect(dbname="postgres", user="ozge", host="")
    conn.autocommit = True
    cur = conn.cursor()
    
    # Şifreni 'euzghe_77' olarak ayarla
    cur.execute("ALTER USER ozge WITH PASSWORD 'euzghe_77';")
    
    print("🚀 ŞİFRE BAŞARIYLA GÜNCELLENDİ: euzghe_77")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Hata oluştu: {e}")