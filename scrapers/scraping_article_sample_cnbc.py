import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Read file Master Link Q1 2026
source_file = "Master_Link_CNBC_Q1_2026_(28-31).csv"
print(f"open file {source_file}...")
df_link = pd.read_csv(source_file)

# Trying using 5 Sample article to extract
# df_link = df_link.head(5) 

data_article = []

# Disguised as a Chrome browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Start process scrapping article : {len(df_link)}")
print("-" * 50)

for index, row in df_link.iterrows():
    url_target = row['url_article']
    date = row['date_publication']
    
    try:
        response = requests.get(url_target, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Title Extract
        tag_title = soup.find('h1')
        clean_title = tag_title.text.strip() if tag_title else "title not found"
            
        # Logic Extract (PERBAIKAN VARIABEL DI SINI)
        clean_content = "" 
        
        # Python will try to find all possible article box names on CNBC
        possibility_class = ['detail_text', 'detail-text', 'artikel-berita', 'article-body', 'content']
        possibility_content = soup.find('div', class_=possibility_class)
        
        # If article box was found
        if possibility_content:
            all_paragraph = possibility_content.find_all('p')
            text_paragraph = []
            
            for p in all_paragraph:
                text = p.text.strip()
                # Just take a long enough paragraph and not a "Baca juga" link.
                if len(text) > 30 and "Baca:" not in text and "Saksikan" not in text:
                    text_paragraph.append(text)
                    
            # combine all paragraph
            clean_content = " ".join(text_paragraph)
        
        # if box was found, but not have article content (Atau kotak tidak ditemukan sama sekali)
        if not clean_content:
            clean_content = "Format Non-Teks (either Video/Foto)"
            
        # Saving data
        data_article.append({
            'date_publication': date,
            'media_source': 'CNBC',
            'title_article': clean_title,
            'content_article': clean_content,
            'url_article': url_target
        })
        
        # Laporan progres mencetak Judul agar terminal lebih rapi
        print(f"[{index + 1}/{len(df_link)}] Success: {clean_title[:40]}...")
        time.sleep(2)
        
    except Exception as e:
        print(f"[{index + 1}/{len(df_link)}] FAILED in url {url_target} - Error: {e}")

print("-" * 50)
print("Extraction Completed")

# Saving document in .csv
df_output = pd.DataFrame(data_article)
file_name = "CNBC_article_market_Q1.csv"
df_output.to_csv(file_name, index=False)

print(f"{file_name} saved successfully!!!")
