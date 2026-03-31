from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import pandas as pd
from itertools import islice

downloader = YoutubeCommentDownloader()

video_url = 'https://www.youtube.com/watch?v=qPvtOvqjod8'

print(f"--- Memulai Scraping YouTube: {video_url} ---")

comments = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)

data_youtube = []

for comment in islice(comments, 1800):
    data_youtube.append({
        'Username': comment['author'],
        'Isi komentar': comment['text'].replace('\n',' '),
        'Jumlah like komentar': comment['votes'],
        'Waktu komentar': comment['time']
    })

df = pd.DataFrame(data_youtube)

nama_file = 'dataset_youtube_video2.csv'
df.to_csv(nama_file, index=False, encoding='utf-8')

print(f"Data tersimpan di {nama_file}")