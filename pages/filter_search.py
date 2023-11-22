import pandas as pd
import fasttext
import fasttext.util
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
fasttext.FastText.eprint = lambda x: None
# The following lines must be ran once locally
nltk.download('stopwords')
nltk.download('punkt')

# NOTE: You must download the model, for this code currently, the model is downloaded via:
# "fasttext.util.download_model('en', if_exists='ignore')"
# I (Adi) have it on my local machine, the file is 7gigs so I havent pushed it to the repo
# The file is in the home directory of the repo, named 'cc.en.300.bin'

print('Checking if model downloaded')
fasttext.util.download_model('en', if_exists='ignore')
print('Model detected')

print('Loading model')
ft = fasttext.load_model('cc.en.300.bin')

print('Loading stopwords')
stop_words = set(stopwords.words('english'))  # Set of English stopwords
print('Stopwords loaded')

# Function to remove stopwords from a text string
# Input:
def remove_stopwords(text):
    """Remove stopwords from a text string

    Args:
        text (str): Text

    Returns:
        String with stopwords removed
    """
    tokens = word_tokenize(text)  # Tokenize the text into words
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]  # Remove stopwords
    return ' '.join(filtered_tokens)  # Join the filtered tokens back into a string


# Calculate the cosine similarity of two vectors
cos_similarity = lambda a, b: np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

# Testing removing dimensions from the model, lowers performance too much in practice with no noticable performance gain
# fasttext.util.reduce_model(ft, 100)
# print(ft.get_dimension())

def find_top_const(etf, query, file_output=False, prnt=False, return_res=False):
    """Given an ETF and a search query, find the top 10 constituents of the ETF that are most similar to the query

    Args:
        etf (pandas df): Consists of an ETF's constituents, their 'Description', 'Sector', 'Industry', and 'Weights'
        query (string): Search query from sales
        file_output (bool): Whether or not to output the results to a CSV file
        prnt (bool): Whether or not to print the results to the console
        return_res: Whether or not to return the results
    """

    for idx, row in etf.iterrows():
        cos_sim = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Description']))
        etf.loc[idx, 'Cosine Similarity'] = cos_sim if cos_sim > 0.31 else 0

        # Optional for future use
        # etf.loc[idx, 'Sector Similarity'] = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Sector']))
        # etf.loc[idx, 'Industry Similarity'] = cos_similarity(ft.get_sentence_vector(query), ft.get_sentence_vector(row['Industry']))


    # Output the sorted results to a CSV file
    if file_output == True:
        etf.sort_values(by='Cosine Similarity', ascending=False).to_csv(f'pages/data/JPM_{query}.csv', index=False)

    # Print the top 10 results' Names, Weights, and Cosine Similarity
    if prnt == True:
        # print(etf.sort_values(by='Cosine Similarity', ascending=False).head(10)) # Print all columns
        print(etf.sort_values(by='Cosine Similarity', ascending=False).head(10)[['Company', 'Weights', 'Cosine Similarity']])

    if return_res == True:
        etf_sorted = etf.sort_values(by='Cosine Similarity', ascending=False)[['Company', 'Weights', 'Cosine Similarity']]
        return etf_sorted

def main():
    print('Currently supported ETFs: BBIN, DFAC, JEPI, JEPQ, JPST, JQUA, QQQ ')

    etf_input = input("Input ETF tickers (seperated by spaces): ")
    etf_list = etf_input.split(' ') # Split the input into a list of ETFs
    term = input("Input a search query: ")
    printb = input("Print results? (y/n): ")
    fileb = input("Output results to CSV? (y/n): ")

    scores = []

    for etf in etf_list:
        print(f'Analyzing ETF: {etf}')

        source_df = pd.read_csv(f'pages/data/{etf}_constituents.csv')
        source_df.dropna(inplace=True) # Useless for filter, and causes errors (Removes rows with NaN descriptions)
        source_df['Description'] = source_df['Description'].apply(remove_stopwords)

        find_top_const(source_df,
                       term,
                       True if fileb == 'y' else False,
                       True if printb == 'y' else False)

        etf_score = 0
        for idx, row in source_df.iterrows():
            etf_score += float(row['Cosine Similarity']) * float(row['Weights'].strip('%'))

        scores.append([etf,etf_score])


    for score in scores:
        print(f'ETF {score[0]} score: {score[1]} for search term: {term}')


def get_ETF_similarity(tickers: list[str], keyword: str):
    scores = {}

    for etf in tickers:
        # print(f'Analyzing ETF: {etf}')

        source_df = pd.read_csv(f'./pages/data/{etf}_constituents.csv')
        source_df.dropna(inplace=True) # Useless for filter, and causes errors (Removes rows with NaN descriptions)
        source_df['Description'] = source_df['Description'].apply(remove_stopwords)

        source_df_processed = find_top_const(source_df, keyword, return_res=True)
        # print(source_df_processed)

        etf_score = 0
        for idx, row in source_df_processed.iterrows():
            etf_score += float(row['Cosine Similarity']) * float(row['Weights'].strip('%'))

        scores[etf] = etf_score

    # print(scores)
    return scores

run = True

# while run == True:
while run == True and __name__ == "__main__":
    main()
    run = False if input("Run again? (y/n): ") == 'n' else True

# source_df = pd.read_csv(f'pages/data/{etf}_constituents.csv')
# source_df.dropna(inplace=True) # Useless for filter, and causes errors
#



# print(source_df)
