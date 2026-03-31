from google_play_scraper import Sort, reviews
import pandas as pd

# Menggunakan shopee karena ulasan nya banyak
app_id = 'com.shopee.id' 

print(f" Memulai Scraping Google Play Store untuk: {app_id} ")

# Proses pengambilan data
result, _ = reviews(
    app_id,
    lang='id',      
    country='id',  
    sort=Sort.NEWEST, 
    count=1800
)

data_final = []
for r in result:
    data_final.append({
        'Username': r['userName'],
        'Rating': r['score'],
        'Isi ulasan': r['content'],
        'Tanggal ulasan': r['at']
    })

# Simpan ke CSV
df = pd.DataFrame(data_final)
nama_file = 'dataset_playstore_shopee.csv'
df.to_csv(nama_file, index=False, encoding='utf-8')

print("-" * 30)
print(f"BERHASIL! Terkumpul {len(df)} ulasan.")
print(f"File tersimpan dengan nama: {nama_file}")
print("-" * 30)