import pandas as pd

print('reading dataset')

df_article = pd.read_csv('Master_Database_Artikel_Media_Q1_FULLDATA.csv')
df_sentiment = pd.read_csv('Output_Final_Sentiment_Media_Q1_2026.csv')

# adding only needed column in sentiment document
df_sentiment_clean = df_sentiment[['url_article','sentiment_label','polarity_score','ai_confidence']]

print('Merging data....')
# left join proccess
df_fact_article = pd.merge(df_article, df_sentiment_clean, on='url_article', how='left')

df_fact_article['date_publication'] = pd.to_datetime(df_fact_article['date_publication']).dt.date

#Saving output 
file_output = 'Fact_Article_Sentiment_Q1.csv'
df_fact_article.to_csv(file_output, index=False)

print(f'Successfully!!! Fact Table Article with {len(df_fact_article)} was saved in {file_output}')
