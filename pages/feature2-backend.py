import pandas as pd
import matplotlib.pyplot as plt

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

def plot_timeseries(etf1, etf2, column, period=365):
    etf1_data = select_column(etf1, column)[:period]
    etf2_data = select_column(etf2, column)[:period]
    print(type(etf2_data[column][0]))
    etf1_data['Date'] = pd.to_datetime(etf1_data['Date'])
    etf2_data['Date'] = pd.to_datetime(etf2_data['Date'])
    plt.plot(etf1_data['Date'], etf1_data[column], label=etf1)
    plt.plot(etf2_data['Date'], etf2_data[column], label=etf2)
    plt.title(f'{column} of {etf1} and {etf2}')
    plt.legend()
    plt.show()


# List of what metric to plot for each advantage
plot_metric = {
    'Tot Asset US$ (M)' : 'FUND_NET_ASSET_VAL',
    'Avg Dvd Yield' : 'TOT_RETURN_INDEX_GROSS_DVDS',
    'Alpha' : 'FUND_NET_ASSET_VAL',
    'Tot Ret' : 'FUND_NET_ASSET_VAL',
}

def plot_advantages(df, x1, x2):
    advantages = find_advantage(df, x1, x2)
    print(f'Detecting {len(advantages)} advantages')
    print(f'Advantages: {advantages}')
    for row in advantages.items():
        print(f' Plotting {row[0]}')
        split_row = row[0].split()
        print(split_row)
        if split_row[-1][1] == 'Y': # Check the last split word for 'Y'
            plot_timeseries(
                'JEPI',
                'QQQ',
                plot_metric[' '.join(split_row[:-1])],
                365*int(split_row[-1][0]) # Multiply year value by 365 
            ) 
    # plot_timeseries(x1, x2, row[0]) # TODO: Fix name discrepancy between select_column and find_advantage
        else:
            plot_timeseries('JEPI', 'QQQ', plot_metric[row[0]])

df = pd.read_csv('Competitor Data.csv')
# print(df)
df = clean_competitor_data(df)
# print(df)
# print(find_advantage(df, 'JEPI US Equity', 'CQQQ US Equity'))
# print(find_advantage(df, 'BBSC US Equity', 'SPYG US Equity'))
# print(select_column('QQQ', 'FUND_NET_ASSET_VAL'))
# plot_timeseries('DFAC', 'QQQ', 'FUND_NET_ASSET_VAL', 365)
print(find_advantage(df, 'JEPI US Equity', 'CQQQ US Equity'))
plot_advantages(df, 'JEPI US Equity', 'CQQQ US Equity')

# print(select_column('QQQ', 'FUND_NET_ASSET_VAL'))
# print(select_column('QQQ', 'TOT_RETURN_INDEX_GROSS_DVDS'))