import pandas as pd
import re
from collections import Counter

# 1. <-- Memuat Data -->
df_shopee = pd.read_csv('data_shopee.csv')
df_yt1 = pd.read_csv('dataset_yt_video1_final.csv')
df_yt2 = pd.read_csv('dataset_yt_video2_final.csv') 
df_maps = pd.read_csv('data_maps_final.csv')

# 2. <-- Standarisasi Kolom -->
df_shopee = df_shopee.rename(columns={'Isi ulasan': 'Teks', 'Username': 'User', 'Tanggal ulasan': 'Waktu'})
df_shopee['Sumber'] = 'Shopee'

df_yt1 = df_yt1.rename(columns={'Isi komentar': 'Teks', 'Username': 'User', 'Waktu komentar': 'Waktu'})
df_yt1['Sumber'] = 'YouTube (Epstein Part 1)'

df_yt2 = df_yt2.rename(columns={'Isi komentar': 'Teks', 'Username': 'User', 'Waktu komentar': 'Waktu'})
df_yt2['Sumber'] = 'YouTube (Epstein Part 2)'

df_maps = df_maps.rename(columns={'Isi Ulasan': 'Teks', 'Username': 'User', 'Waktu Ulasan': 'Waktu'})
df_maps['Sumber'] = 'Google Maps (Tugu Jogja)'

# 3. <-- Gabung Semua Data -->
cols = ['User', 'Teks', 'Waktu', 'Sumber']
df_all = pd.concat([df_shopee[cols], df_yt1[cols], df_yt2[cols], df_maps[cols]], ignore_index=True)
df_all = df_all.dropna(subset=['Teks'])

# 4. <-- Daftar Stopwords -->
custom_stops = {
    'yang', 'di', 'ke', 'dan', 'ini', 'itu', 'nya', 'ada', 'buat', 'dari', 'kalau', 'kalo', 'udah', 'gak', 'ga',
    'bisa', 'aja', 'sama', 'juga', 'untuk', 'dengan', 'lebih', 'sih', 'lagi', 'tapi', 'aku', 'kamu', 'ya', 'saya',
    'dia', 'mereka', 'kita', 'kami', 'karena', 'karna', 'seperti', 'dalam', 'pada', 'atau', 'sangat', 'jadi',
    'tidak', 'banyak', 'sudah', 'akan', 'bagi', 'sampai', 'hanya', 'saat', 'jangan', 'apa', 'saja', 'terus',
    'banget', 'kok', 'deh', 'nih', 'tuh', 'dah', 'kan'
}

# 5. <-- FUNGSI STEP-BY-STEP -->

def step1_case_folding(text):
    if not isinstance(text, str): return ""
    return text.lower()

def step2_filtering(text):
    # Hapus URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Hapus Mention/Hashtag
    text = re.sub(r'@\w+|#\w+', '', text)
    # Hapus SELAIN huruf a-z dan spasi (Hapus koma, titik, emoji)
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Rapikan spasi ganda
    return ' '.join(text.split())

def step3_stopword_removal(text):
    words = text.split()
    words = [w for w in words if w not in custom_stops and len(w) > 2]
    return ' '.join(words)

# 6. <-- Pembersihan Secara Bertahap -->
print("Memulai proses pembersihan bertahap...")

# Eksekusi Tahap 1
df_all['Tahap1_CaseFolding'] = df_all['Teks'].apply(step1_case_folding)

# Eksekusi Tahap 2 (Ambil dari hasil Tahap 1)
df_all['Tahap2_Filtered'] = df_all['Tahap1_CaseFolding'].apply(step2_filtering)

# Eksekusi Tahap 3 Final (Ambil dari hasil Tahap 2)
df_all['Tahap3_FinalBersih'] = df_all['Tahap2_Filtered'].apply(step3_stopword_removal)

# 7. <-- Ekstrak Knowledge  -->
results = {}
for source in df_all['Sumber'].unique():
    text_corpus = ' '.join(df_all[df_all['Sumber'] == source]['Tahap3_FinalBersih'].tolist())
    word_counts = Counter(text_corpus.split()).most_common(15)
    results[source] = word_counts

print("\n" + "="*30)
print("HASIL TOP KATA PER PLATFORM")
print("="*30)
for k, v in results.items():
    print(f"{k}:")
    print(f"   {v}")

# 8. <-- Simpan File Final -->
df_all.to_csv('datafinal_FIX.csv', index=False)
print("\nSelesai! File 'datafinal_FIX.csv' siap dikumpulkan.")