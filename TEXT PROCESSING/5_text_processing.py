import pandas as pd
import re
from collections import Counter

# <-- Memuat data -->
df_shopee = pd.read_csv('data_shopee.csv')
df_yt1 = pd.read_csv('dataset_yt_video1_final.csv')
df_yt2 = pd.read_csv('dataset_yt_video2_final.csv')
df_maps = pd.read_csv('data_maps_final.csv')

# <-- Standarisasi Kolom -->
df_shopee = df_shopee.rename(columns={'Isi ulasan': 'Teks', 'Username': 'User', 'Tanggal ulasan': 'Waktu'})
df_shopee['Sumber'] = 'Shopee'

df_yt1 = df_yt1.rename(columns={'Isi komentar': 'Teks', 'Username': 'User', 'Waktu komentar': 'Waktu'})
df_yt1['Sumber'] = 'YouTube (Podcast Deddy)'

df_yt2 = df_yt2.rename(columns={'Isi komentar': 'Teks', 'Username': 'User', 'Waktu komentar': 'Waktu'})
df_yt2['Sumber'] = 'YouTube (Nadhif)'

df_maps = df_maps.rename(columns={'Isi Ulasan': 'Teks', 'Username': 'User', 'Waktu Ulasan': 'Waktu'})
df_maps['Sumber'] = 'Google Maps (Tugu Jogja)'

# <-- Gabung Semua Data -->
cols = ['User', 'Teks', 'Waktu', 'Sumber']
df_all = pd.concat([df_shopee[cols], df_yt1[cols], df_yt2[cols], df_maps[cols]], ignore_index=True)
df_all = df_all.dropna(subset=['Teks'])

# <-- Daftar Kata yang dihapus -->
custom_stops = {
    'yang', 'di', 'ke', 'dan', 'ini', 'itu', 'nya', 'ada', 'buat', 'dari', 'kalau', 'kalo', 'udah', 'gak', 'ga',
    'bisa', 'aja', 'sama', 'juga', 'untuk', 'dengan', 'lebih', 'sih', 'lagi', 'tapi', 'aku', 'kamu', 'ya', 'saya',
    'dia', 'mereka', 'kita', 'kami', 'karena', 'karna', 'seperti', 'dalam', 'pada', 'atau', 'sangat', 'jadi',
    'tidak', 'banyak', 'sudah', 'akan', 'bagi', 'sampai', 'hanya', 'saat', 'jangan', 'apa', 'saja', 'terus'
}

# <-- Fungsi Text Processing  -->
def clean_text(text):
    text = str(text).lower() 
    text = re.sub(r'https?://\S+|www\.\S+', '', text) 
    text = re.sub(r'@\w+|#\w+', '', text) 
    text = re.sub(r'[^a-z\s]', ' ', text) 
    
    # <-- Tokenizing & Stopword Removal -->
    words = text.split()
    words = [w for w in words if w not in custom_stops and len(w) > 2]
    return ' '.join(words)

# <-- Mulai pembersihan -->
print("Memulai proses pembersihan teks...")
df_all['Teks_Bersih'] = df_all['Teks'].apply(clean_text)

# <-- Ekstrak Knowledge -->
results = {}
for source in df_all['Sumber'].unique():
    text_corpus = ' '.join(df_all[df_all['Sumber'] == source]['Teks_Bersih'].tolist())
    word_counts = Counter(text_corpus.split()).most_common(15)
    results[source] = word_counts

print("\n----- TOP KATA PER PLATFORM -----")
for k, v in results.items():
    print(f"{k}: {v}")

# <-- Simpan File Nya -->
df_all.to_csv('datafinal_FIX_processing.csv', index=False)