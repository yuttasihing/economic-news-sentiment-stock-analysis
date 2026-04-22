import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import time
import os

# Reading Master Database
file_master = 'Master_Database_Artikel_Media_Q1_FULLDATA.csv'
print(f'open document : {file_master}')
df = pd.read_csv(file_master)

print(f'Total Data : {len(df)} article')
print('Activating Indobert Model......')

# Activating Indobert Model for Sentiment Analysis
sentiment_analysis = pipeline(
    "sentiment-analysis",
    model="mdhugol/indonesia-bert-sentiment-classification",
    tokenizer="mdhugol/indonesia-bert-sentiment-classification"
)

# Preparing New Output Column
# PERBAIKAN TYPO: confidance -> confidence
if 'sentiment_label' not in df.columns:
    df['sentiment_label'] = None
    df['polarity_score'] = None
    df['ai_confidence'] = None

print('Indobert Active!! Analysis Starting')

# Looping with tqdm (Loading bar Visual)
# PERBAIKAN BUG 1: Menghapus koma ekstra setelah 'row'
for index, row in tqdm(df.iterrows(), total=len(df), desc="News Analyzing"):
    
    # Skip if this article has already been analyzed
    if pd.notna(row['sentiment_label']):
        continue

    news_text = str(row['content_article'])

    # FILTER: If the article fails to extract or is too short, it will automatically be Neutral
    # PERBAIKAN BUG 3: Menggunakan .lower() untuk mengabaikan perbedaan huruf kapital
    if "gagal ekstrak" in news_text.lower() or len(news_text) < 50:
        df.at[index, 'sentiment_label'] = 'NETRAL'
        df.at[index, 'polarity_score'] = 0.0
        df.at[index, 'ai_confidence'] = 0.0
        continue

    # article limit: 1500 characters
    text_limit = news_text[:1500]

    try:
        # input text into AI
        output = sentiment_analysis(text_limit)

        # takes output from AI
        raw_tag = output[0]['label']
        score_confidence = output[0]['score']

        # Converting into score polarization (-1 to 1)
        if raw_tag == 'LABEL_0':
            sentiment = 'NEGATIF'
            # PERBAIKAN BUG 2: Menghapus kurung kurawal
            polarity = -score_confidence 
        elif raw_tag == 'LABEL_1':
            sentiment = "NETRAL"
            polarity = 0.0
        elif raw_tag == 'LABEL_2':
            sentiment = 'POSITIF'
            polarity = score_confidence
        else:
            sentiment = "UNKNOWN" 
            polarity = 0.0

        # Saving into table 
        df.at[index, 'sentiment_label'] = sentiment
        df.at[index, 'polarity_score'] = round(polarity, 4)
        df.at[index, 'ai_confidence'] = round(score_confidence, 4)

    except Exception as e:
        df.at[index, 'sentiment_label'] = 'ERROR'
        df.at[index, 'polarity_score'] = 0.0
        df.at[index, 'ai_confidence'] = 0.0

    # Autosave system to .csv file for finished analyzing 500 article
    if (index + 1) % 500 == 0:
        file_checkpoint = 'autosave_sentiment_Q1.csv'
        df.to_csv(file_checkpoint, index=False)
        tqdm.write(f'AUTOSAVE {index + 1} : Article successfully saved')

# Saving Final Result 
final_file = 'Output_Final_Sentiment_Media_Q1_2026.csv'
df.to_csv(final_file, index=False)

print(f'Analysis Successfully!! Data was saved in: {final_file}')
