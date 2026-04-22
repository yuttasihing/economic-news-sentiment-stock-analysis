import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#Setting Periodical Time Q1 2026 (1 Januari - 31 March)
start_date = '2026-03-28'
end_date = '2026-03-31'

#create automatic date list using pandas
date_list = pd.date_range(start=start_date, end=end_date)

#Temporary data storage
date_list_storage = []

#Disguise as a regular Chrome browser to avoid being blocked.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f'start storage CNBC link from {start_date} to {end_date}')

#Looping Day Process
for date in date_list:
    #change date format 
    date_format_url = date.strftime('%Y/%m/%d')

    url_target = f'https://www.cnbcindonesia.com/market/indeks/5?date={date_format_url}'

    print(f'News Date : {date_format_url}')
    
    try:
        response = requests.get(url_target, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text,'html.parser')
        all_article = soup.find_all('article')
        total_news = 0

#Extract link
        for article in all_article:
            tag_a = article.find('a')
            if tag_a and 'href' in tag_a.attrs:
                link = tag_a['href']

                #Adding data in storage 
                date_list_storage.append({
                    'date_publication': date.strftime('%Y-%m-%d'),
                    'url_article': link,
                    'media_source': 'CNBC'
                })

                total_news += 1

        print(f'finding {total_news} link article')

        time.sleep(2)

    except Exception as e:
        print(f'There was a disruption to the date {date_format_url}: {e}')

print("Currently tidying up the data...")

df_link = pd.DataFrame(date_list_storage)
nama_file = "Master_Link_CNBC_Q1_2026.csv"
df_link.to_csv(nama_file, index=False)

print(f"finish!!! {len(df_link)} news link saved in '{nama_file}'.")



