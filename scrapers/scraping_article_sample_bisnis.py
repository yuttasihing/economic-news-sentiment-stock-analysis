import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Reading .csv file
file_source = 'Master_Link_Bisnis_Q1_2026_(28-31).csv'
print(f'reading {file_source}')
df_link = pd.read_csv(file_source)

# sample = just take 5 news samples
#df_link = df_link.head(5)

# storage articles
data_article = []

# disguise chrome browser 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f'Starting text extraction trial for {len(df_link)} Bisnis.com articles...')
print("-" * 50)

for index, row in df_link.iterrows():
    url_target = row['url_article']
    date = row['date_publication']

    try: 
        # Takes the HTML of the referring URL and organizes it into a dom tree.
        response = requests.get(url_target, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # title extraction
        title_tag = soup.find('h1')
        clean_title = title_tag.text.strip() if title_tag else 'Judul Tidak Ditemukan'

        # content extraction : TAKTIK SAPU JAGAT
        content_article = ""
        text_paragraph = []

        # Langsung ambil SEMUA paragraf di seluruh halaman tanpa peduli kotaknya
        all_paragraph = soup.find_all('p')

        for p in all_paragraph:
            text = p.text.strip()
            
            # Filter Sangat Ketat: 
            # 1. Harus lebih dari 60 huruf (agar menu/link pendek terbuang)
            # 2. Tidak mengandung kalimat promosi jurnalis
            if (len(text) > 60 and 
                'Baca Juga' not in text and 
                'Cek Berita' not in text and 
                'Google News' not in text and 
                'Simak berita lainnya' not in text):
                
                text_paragraph.append(text)

        content_article = " ".join(text_paragraph)

        # Jika masih kosong juga, tandai gagal
        if not content_article:
            content_article = "Format Non-Text/Gagal Ekstrak"

        # Saving Data 
        data_article.append({
            'date_publication': date,
            'media_source': 'Bisnis.com',
            'title_article': clean_title,
            'content_article': content_article,
            'url_article': url_target
        })

        print(f'[{index + 1}/{len(df_link)}] | Success : {clean_title[:50]}...')
        time.sleep(2)
    
    except Exception as e:
         print(f'[{index + 1}/{len(df_link)}] | Failed for Url {url_target} - Error : {e}')

print("-" * 50)
print('Trial extraction was completed')

# saving extraction output into .csv
df_output = pd.DataFrame(data_article)
file_name = 'bisnis_article_bursa_saham_Q1_2026_(28-31).csv'
df_output.to_csv(file_name, index=False)

print(f'Document successfully saved in {file_name}')
