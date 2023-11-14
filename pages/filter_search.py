import pandas as pd
import fasttext
import fasttext.util
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# The following lines must be ran once locally
# nltk.download('stopwords')
# nltk.download('punkt')

# NOTE: You must download the model, for this code currently, the model is downloaded via:
#"fasttext.util.download_model('en', if_exists='ignore')"
# I (Adi) have it on my local machine, the file is 7gigs so I havent pushed it to the repo

stop_words = set(stopwords.words('english'))  # Set of English stopwords

# # Function to remove stopwords from a text string
def remove_stopwords(text):
    tokens = word_tokenize(text)  # Tokenize the text into words
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]  # Remove stopwords
    return ' '.join(filtered_tokens)  # Join the filtered tokens back into a string

cos_similarity = lambda a, b: np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))


def find_top_const(etf, query, file_output=False):
    # Given an 'ETF' dataframe with a 'Description' column, and a 'query' string, find the top 10 most similar
    ft = fasttext.load_model('pages/models/cc.en.300.bin')

    for idx, row in etf.iterrows():
        cos_sim = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Description']))
        etf.loc[idx, 'Cosine Similarity'] = cos_sim

    # Print the top 10 results
    print(etf.sort_values(by='Cosine Similarity', ascending=False).head(10))

    # Output the sorted results to a CSV file
    if file_output == True:
        etf.sort_values(by='Cosine Similarity', ascending=False).to_csv(f'pages/data/JPM_{query}.csv', index=False)


print('Currently supported ETFs: JEPI, BBIN ') # I will add more as I make more '{ETF}_constituents.csv' files using find_constituents.py
etf = input("Input an ETF ticker: ")

source_df = pd.read_csv(f'pages/data/{etf}_constituents.csv')
source_df.dropna(inplace=True) # Useless for filter, and causes errors
source_df['Description'] = source_df['Description'].apply(remove_stopwords)

term = input("Input a search query: ")
file_output = input("Output to CSV? (y/n): ")

find_top_const(source_df, term, True if file_output == 'y' else False)
