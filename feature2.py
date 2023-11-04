import pandas as pd

#x1 is JPM's ETF, x2 is target competitor's ETF
def find_advantage(df, x1, x2):
    df['ESG Rate'] = df['ESG Rate'].astype(str)
    etf1 = df[df['Symbol'] == x1].iloc[0][1:]
    etf2 = df[df['Symbol'] == x2].iloc[0][1:]
    # print(df['ESG Rate'])
    
    # Remove '%' symbol and commas, and convert to float
    etf1 = etf1.str.replace('%', '').str.replace(',', '').astype(float)
    etf2 = etf2.str.replace('%', '').str.replace(',', '').astype(float)
    # print(etf1)
    # print(etf2)

    # Calculate percentage difference for each column
    diff = ((etf1 - etf2) / etf1) * 100
    # print(diff)

    # Find the best and the second best column
    best = diff.idxmax()
    diff[best] = float('-inf')
    second_best = diff.idxmax()

    return best, second_best 


df = pd.read_csv('example.csv')
print(find_advantage(df, 'JPEI', 'QQQ'))
