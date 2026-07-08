import mysql.connector
import random

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="web_edukasi_islam"
)
cursor = conn.cursor()

# Ambil daftar artikel per kategori
artikel_by_cat = {1: [], 2: [], 3: []}
cursor.execute("SELECT id_artikel, id_kategori FROM artikel")
for id_art, id_cat in cursor.fetchall():
    if id_cat in artikel_by_cat:
        artikel_by_cat[id_cat].append(id_art)

print("=== Persiapan Data Dummy ===")
for cat, lst in artikel_by_cat.items():
    print(f"Kategori {cat} : {len(lst)} artikel tersedia")

# Buat 15 user dummy baru
for i in range(1, 16):
    nama = f"DummyUser{i}"
    email = f"dummy{i}@test.com"
    password = "dummy123"
    
    # Cek apakah email sudah ada
    cursor.execute("SELECT id_jemaah FROM jemaah WHERE email = %s", (email,))
    existing = cursor.fetchone()
    if existing:
        print(f"User {email} sudah ada, dilewati")
        continue
    
    # Insert user baru
    cursor.execute("INSERT INTO jemaah (nama_lengkap, email, password) VALUES (%s, %s, %s)",
                   (nama, email, password))
    user_id = cursor.lastrowid
    
    # Tentukan preferensi: 70% single kategori, 30% dua kategori
    if random.random() < 0.7:
        pref_cats = [random.choice([1, 2, 3])]
    else:
        pref_cats = random.sample([1, 2, 3], k=2)
    
    # Simpan preferensi awal
    for cat in pref_cats:
        cursor.execute("INSERT INTO preferensi_awal (id_jemaah, id_kategori) VALUES (%s, %s)", (user_id, cat))
    
    # Beri riwayat baca: ambil artikel dari kategori yang dipilih
    read_articles = set()
    for cat in pref_cats:
        available = artikel_by_cat.get(cat, [])
        if len(available) < 2:
            continue
        n = random.randint(2, 3)
        for art in random.sample(available, min(n, len(available))):
            read_articles.add(art)
    
    read_articles = list(read_articles)[:6]  # maksimal 6 artikel
    for art in read_articles:
        klik = random.randint(1, 12)
        cursor.execute("""
            INSERT INTO log_interaksi (id_jemaah, id_artikel, jumlah_klik, terakhir_dibaca)
            VALUES (%s, %s, %s, NOW())
        """, (user_id, art, klik))
    
    print(f"✓ {nama} (ID:{user_id}) | preferensi: {pref_cats} | baca: {len(read_articles)} artikel")

conn.commit()
cursor.close()
conn.close()
print("\nSelesai! Data dummy baru siap.")