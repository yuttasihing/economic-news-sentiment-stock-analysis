import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

#Reading .csv file
file_source = 'Master_Link_Kontan_Q1_2026_(28-31).csv'
print(f'reading {file_source}')
df_link = pd.read_csv(file_source)

#sample = just take 5 news samples
#df_link = df_link.head(5)

#storage article
data_article = []

#disguise chrome browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

print(f'Starting text extraction trial for {len(df_link)} Kontan articles..."')

for index, row in df_link.iterrows():
    url_target = row['url_article']
    date = row['date_publication']


    try: 
        #Takes the HTML of the referring URL and organizes it into a dom tree.
        response = requests.get(url_target, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        #Title Extraction
        title_tag = soup.find('h1')
        title_clean = title_tag.text.strip() if title_tag else "Judul Tidak Ditemukan"

        #Content Extraction
        clean_content = ""

        #Looking for a news paragraph wrapper box
        box_model = soup.find('div', itemprop='articleBody')
        if not box_model:
            box_model = soup.find('div', class_=['tmpt-desk-kon','detail-desk'])

        if box_model:
            all_paragraph = box_model.find_all('p')
            text_paragraph = []

            for p in all_paragraph:
                text = p.text.strip()
                if len(text) > 30 and 'Baca Juga' not in text and 'Cek Berita' not in text and 'Menarik Dibaca' not in text and 'Selanjutnya:' not in text:
                    text_paragraph.append(text)

            clean_content = " ".join(text_paragraph)

        if not clean_content:
            clean_content = "Format Non-Text/Gagal Ekstrak"

        #Saving Data
        data_article.append({
            'date_publication': date,
            'media_source' : 'Kontan',
            'title_article' : title_clean,
            'content_article' : clean_content,
            'url_article' : url_target
        })

        print(f'[{index + 1}/{len(df_link)}] | Success : {title_clean[:50]}')
        time.sleep(2)

    except Exception as e:
        print(f'[{index + 1}/{len(df_link)}] | Failed for Url {url_target} - Error : {e}')

print('trial extraction was completed')

#Saving into .csv file
df_output = pd.DataFrame(data_article)
file_name = 'kontan_article_Investasi_Q1_2026_(28-31).csv'
df_output.to_csv(file_name, index=False)

print(f'{file_name} was Saved into .csv document')
              


