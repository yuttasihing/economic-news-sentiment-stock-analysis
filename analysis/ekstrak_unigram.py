import pandas as pd
import re
from tqdm import tqdm

#reading master database
file_master = 'Master_Database_Artikel_Media_Q1_FULLDATA.csv'
print(f'open data : {file_master}')
df = pd.read_csv(file_master)

#Prepring Stopwords List
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

basic_stopwords = set(stopwords.words('indonesian'))

#Extra stopwords Economic context
stopwords_extra = {
    'rp', 'pt', 'tbk', 'persen', 'juta', 'miliar', 'triliun', 'jakarta', 
    'indonesia', 'cnbc', 'kontan', 'bisnis', 'com', 'id', 'reporter', 
    'editor', 'co', 'saham', 'harga', 'perusahaan', 'pasar', 'bursa',
    'efek', 'bei', 'ihsg', 'investor', 'satu', 'dua', 'tahun', 'hari',
    'kuartal', 'ini', 'itu', 'dan', 'yang', 'di', 'ke', 'dari', 'pada',
    'dalam', 'untuk', 'dengan', 'atau', 'tidak', 'akan', 'juga', 'ada',
    'bisa', 'sudah', 'lebih', 'saat', 'bagi', 'hingga', 'namun','senin','selasa',
    'rabu','kamis','jumat','sabtu','minggu'
}

#combine stopwords 
all_stopwords = basic_stopwords.union(stopwords_extra)

#Cleaning Text Function
def cleaning_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

print('Clean up article text from punctuation and numbers...')
#Create a new column containg clean text
df['clean_text'] = df['content_article'].apply(cleaning_text)

#4. Explode Proccess (breaking down sentences into unigram)
print('breaking down sentences into unigram')
#Split sentences based on spaces
df['unigram'] = df['clean_text'].str.split()

#Break the word list down into rows
df_unigram = df.explode('unigram')

#Discard Lines whose unigram are empty (excess spaces)
df_unigram = df_unigram.dropna(subset=['unigram'])

#Discard short words (less than 3 letters)
df_unigram = df_unigram[df_unigram['unigram'].str.len() > 2]

#5. Filtering Stopwords
print('filtering stopword and stopwords extra')
df_unigram = df_unigram[~df_unigram['unigram'].isin(all_stopwords)]

#6. Aggregating Frequency 
print('Calculated unigram frequent based on date_publication and media_source')
df_final = df_unigram.groupby(['date_publication','media_source','unigram']).size().reset_index(name='frequency')

#sort data from highest frequency per date
df_final = df_final.sort_values(by=['date_publication','media_source','frequency'], ascending=[True,True,False])

#7. Saving Output
file_output = 'dataset_unigram_article_2026_Q1.csv'
df_final.to_csv(file_output, index=False)

print('extraction successfully!!')
print(f'total rows unigram = {len(df_final)} rows')
print(f'{file_output} was ready for next analysis')

