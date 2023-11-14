import pandas as pd
import fasttext
import fasttext.util
import numpy as np

# The code below is used to remove stopwords from the 'Description' column of the JPM_ETF_Holdings.csv file
# Can be made into a function and used in the future if needed

# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# nltk.download('stopwords')
# nltk.download('punkt')
#
# source_df = pd.read_csv('pages/data/JPM_ETF_Holdings.csv')
#
# constituents = source_df[['Description']].copy()
# print(constituents.head())
#
# stop_words = set(stopwords.words('english'))  # Set of English stopwords
#
# # Function to remove stopwords from a text string
# def remove_stopwords(text):
#     tokens = word_tokenize(text)  # Tokenize the text into words
#     filtered_tokens = [word for word in tokens if word.lower() not in stop_words]  # Remove stopwords
#     return ' '.join(filtered_tokens)  # Join the filtered tokens back into a string
#
# # Apply the remove_stopwords function to the 'Description' column
# source_df['Description'] = source_df['Description'].apply(remove_stopwords)
#
# source_df.to_csv('pages/data/JPM_ETF_Holdings_cleaned.csv', index=False)  # Save the cleaned data to a CSV file

source_df = pd.read_csv('pages/data/JPM_ETF_Holdings_cleaned.csv')
cos_similarity = lambda a, b: np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def find_top_const(etf, query, file_output=False):
    ft = fasttext.load_model('pages/models/cc.en.300.bin')

    for idx, row in etf.iterrows():
        cos_sim = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Description']))
        etf.loc[idx, 'Cosine Similarity'] = cos_sim

    # Print the top 10 results
    print(etf.sort_values(by='Cosine Similarity', ascending=False).head(10))

    # Output the sorted results to a CSV file
    if file_output == True:
        etf.sort_values(by='Cosine Similarity', ascending=False).to_csv(f'pages/data/JPM_{query}.csv', index=False)

find_top_const(source_df, 'technology')

