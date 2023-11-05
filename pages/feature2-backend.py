import pandas as pd

###x1 is JPM's ETF, x2 is target competitor's ETF
def find_advantage(df, x1, x2):
    # Get data for the two ETFs
    etf1 = df[df['Ticker'] == x1].iloc[0][1:]
    etf2 = df[df['Ticker'] == x2].iloc[0][1:]
    etf1 = etf1[8:].astype(float)
    etf2 = etf2[8:].astype(float)
    
    # Remove '%' symbol and commas, and convert to float
    # etf1 = etf1.str.replace('%', '').str.replace(',', '').astype(float)
    # etf2 = etf2.str.replace('%', '').str.replace(',', '').astype(float)

    # Calculate percentage difference for each column
    diff = ((etf1 - etf2) / etf1) * 100
    
    advantages = diff[diff > 0]
    return advantages

    # Find the best and the second best column
    # best = diff.idxmax()
    # diff[best] = float('-inf')
    # second_best = diff.idxmax()
    # return best, second_best 
    

###Clean competitor_data.csv
def clean_competitor_data(data_df):
    modified_df = data_df.copy()
    # Replace NaN with -inf for Parent Comp. Name = "JP Morgan ETFs/USA"
    modified_df.loc[modified_df["Parent Comp. Name"] == "JP Morgan ETFs/USA"] = modified_df.loc[modified_df["Parent Comp. Name"] == "JP Morgan ETFs/USA"].fillna(float('-inf'))
    # Replace NaN with +inf for the rest of the data
    modified_df = modified_df.fillna(float('inf'))
    return modified_df

###choose a etf and an attribute
def select_column(etf, column):
    file_path = 'price data/' + etf + '.csv'
    data_df = pd.read_csv(file_path)
    selected_columns = ['Date', column]
    selected_data = data_df[selected_columns]
    return selected_data


df = pd.read_csv('Competitor Data.csv')
# print(df)
df = clean_competitor_data(df)
# print(df)
print(find_advantage(df, 'JEPI US Equity', 'CQQQ US Equity'))
print(find_advantage(df, 'BBSC US Equity', 'SPYG US Equity'))
print(select_column('QQQ', 'FUND_NET_ASSET_VAL'))

