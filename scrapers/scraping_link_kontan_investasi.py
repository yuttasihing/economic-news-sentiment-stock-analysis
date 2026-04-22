import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# preparing time periodical Q1 2026 (Jan-Mar 2026)
start_date = '2026-03-28'
end_date = '2026-03-31'
list_date = pd.date_range(start=start_date, end=end_date)

list_link_article = []
# Senjata Baru: Tempat penampung sementara untuk mencegah link ganda
unique_links = set()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print('Commencing KONTAN (Investasi) link sweep operation Q1 2026...')
print("-" * 50)

# Looping day process
for date in list_date:
    day = date.strftime('%d')
    month = date.strftime('%m')
    year = date.strftime('%Y')

    url_target = f'https://www.kontan.co.id/search/indeks?kanal=investasi&tanggal={day}&bulan={month}&tahun={year}&pos=indeks'

    print(f"browse the news on the date: {date.strftime('%Y-%m-%d')}")

    try:
        response = requests.get(url_target, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        total_news = 0
        
        # --- TAKTIK SNIPER ---
        # 1. Cari SEMUA tautan di halaman tersebut, di mana pun letaknya
        semua_link = soup.find_all('a')

        for tag_a in semua_link:
            if 'href' in tag_a.attrs:
                link = tag_a['href']

                # 2. Filter Ketat: Pastikan itu URL artikel berita Kontan, bukan link iklan/sosmed
                if '/news/' in link and 'kontan.co.id' in link:
                    
                    # 3. Tambal https: jika tidak ada
                    if link.startswith('//'):
                        link = 'https:' + link
                        
                    # 4. Filter Duplikat: Jika link belum pernah diambil, masukkan ke data!
                    if link not in unique_links:
                        unique_links.add(link) # Catat link agar tidak diambil dua kali
                        
                        list_link_article.append({
                            'date_publication': date.strftime('%Y-%m-%d'),
                            'url_article': link,
                            'media_source': 'Kontan'
                        })
                        total_news += 1

        print(f' -> {total_news} news link found')
        time.sleep(2)

    except Exception as e:
        print(f" -> there was a disruption on {date.strftime('%Y-%m-%d')} : {e}")

print("-" * 50)
print('Searching finished! currently tidying up the data...')

# Saving into .csv
df_link = pd.DataFrame(list_link_article)
file_name = "Master_Link_Kontan_Q1_2026.csv"
df_link.to_csv(file_name, index=False)

print(f'Success! Total : {len(df_link)}! File successfully saved!!')
