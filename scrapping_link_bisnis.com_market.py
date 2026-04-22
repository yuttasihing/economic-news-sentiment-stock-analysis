import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

#preparing time periodical Q1 2026
start_date = '2026-03-28'
end_date = '2026-03-31'
list_date = pd.date_range(start=start_date, end=end_date)

list_link_article = []
unique_link = set() #For avoid duplicate url 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print('start BISNIS.COM (Bursa dan Saham) link sweep operation Q1 2026...')

#Looping date 
for date in list_date:
    #formating date type similiar with URL Indeks (YYYY-MM-DD)
    date_format = date.strftime('%Y-%m-%d')

    #Assemble the Business.com target URL
    url_target = f'https://www.bisnis.com/index?categoryId=194&date={date_format}&type=indeks'

    print(f'Combing news date: {date_format}')

    try:
        response = requests.get(url_target,headers=headers,timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        total_news = 0

        all_link = soup.find_all('a')

        for tag_a in all_link:
            if 'href' in tag_a.attrs:
                link = tag_a['href']

                #Scrap only Market Column and Bursa dan Saham sub-column (7/url code)
                if 'market.bisnis.com/read/' in link and '/7/' in link:

                    #avoid duplicate link
                    if link not in unique_link:
                        unique_link.add(link)

                        list_link_article.append({
                            'date_publication': date_format,
                            'url_article': link,
                            'media_source': 'bisnis.com'
                        })

                        total_news += 1

        print(f'Found {total_news} stock news links')
        time.sleep(2)

    except Exception as e:
        print(f'An error occurred on {date_format}: {e}')

print('Scanning complete! Currently tidying up data...')

df_link = pd.DataFrame(list_link_article)
output_file = 'Master_Link_Bisnis_Q1_2026.csv'
df_link.to_csv(output_file, index=False)

print(f'Success! A total of {len(df_link)} news links were successfully saved in "{output_file}".')