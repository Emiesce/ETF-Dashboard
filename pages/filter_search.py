import pandas as pd
import fasttext
import fasttext.util
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
fasttext.FastText.eprint = lambda x: None
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

print('Loading model')
ft = fasttext.load_model('pages/models/cc.en.300.bin')

# fasttext.util.reduce_model(ft, 100)
print(ft.get_dimension())

def find_top_const(etf, query, file_output=False, prnt=False):
    # Given an 'ETF' dataframe with a 'Description' column, and a 'query' string, find the top 10 most similar
    # etf_score = 0

    for idx, row in etf.iterrows():
        cos_sim = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Description']))
        etf.loc[idx, 'Cosine Similarity'] = cos_sim if cos_sim > 0.31 else 0
        etf.loc[idx, 'Sector Similarity'] = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Sector']))
        etf.loc[idx, 'Industry Similarity'] = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Industry']))

    # Print the top 10 results' Names, Weights, and Cosine Similarity
    if prnt == True:
        # print(etf.sort_values(by='Cosine Similarity', ascending=False).head(10))
        print(etf.sort_values(by='Cosine Similarity', ascending=False).head(10)[['Company', 'Weights', 'Cosine Similarity']])

    # Output the sorted results to a CSV file
    if file_output == True:
        etf.sort_values(by='Cosine Similarity', ascending=False).to_csv(f'pages/data/JPM_{query}.csv', index=False)

def search_multiple(term):
    pass


def main():
    print('Currently supported ETFs: BBIN, DFAC, JEPI, JEPQ, JPST, JQUA, QQQ ') # I will add more as I make more '{ETF}_constituents.csv' files using find_constituents.py
    choice = input("Single or multiple search terms? (s/m): ")
    if choice == 's':
        etf = input("Input an ETF ticker: ")
        source_df = pd.read_csv(f'pages/data/{etf}_constituents.csv')
        source_df.dropna(inplace=True)
        source_df['Description'] = source_df['Description'].apply(remove_stopwords)

        term = input("Input a search query: ")
        file_output = input("Output to CSV? (y/n): ")

        find_top_const(source_df, term, True if file_output == 'y' else False, prnt=True)

        etf_score = 0
        for idx, row in source_df.iterrows():
            etf_score += float(row['Cosine Similarity']) * float(row['Weights'].strip('%'))
        print(f'ETF {etf} score: {etf_score} for search term: {term}')
    
    else:
        etf_input = input("Input ETF tickers (seperated by spaces): ")
        etf_list = etf_input.split(' ')
        term = input("Input a search query: ")
        scores = []
        for etf in etf_list:
            print(f'Analyzing ETF: {etf}')
            source_df = pd.read_csv(f'pages/data/{etf}_constituents.csv')
            source_df.dropna(inplace=True)
            source_df['Description'] = source_df['Description'].apply(remove_stopwords)

            find_top_const(source_df, term, False, True)

            etf_score = 0
            for idx, row in source_df.iterrows():
                etf_score += float(row['Cosine Similarity']) * float(row['Weights'].strip('%'))
            scores.append([etf,etf_score])
        for score in scores:
            print(f'ETF {score[0]} score: {score[1]} for search term: {term}')





run = True

while run == True:
    main()
    run = False if input("Run again? (y/n): ") == 'n' else True

# source_df = pd.read_csv(f'pages/data/{etf}_constituents.csv')
# source_df.dropna(inplace=True) # Useless for filter, and causes errors
#



# print(source_df)
