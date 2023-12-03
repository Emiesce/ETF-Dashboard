import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


tckr = yf.Ticker('DFAC')
# benchmark = yf.Ticker('NDAQ')
# benchmark_df = benchmark.history(period="max")
df = tckr.history(period="max")

# print(tckr.info)
#
df['Returns'] = df['Close'].pct_change()
# benchmark_df['Returns'] = benchmark_df['Close'].pct_change()

# # Remove the first row of NaN
# df = df[1:]
# benchmark_df = benchmark_df[1:]
#
# df['Alpha'] = np.nan
# df['Beta'] = np.nan
#
#
# def calc_alpha_beta(data, benchmark_data):
#     x = data['Returns'].values
#     y = benchmark_data['Returns'].values
#
#     # print(x)
#
#     model = np.polyfit(x, y, 1)
#     alpha = model[1]
#     beta = model[0]
#     data['Alpha'] = alpha
#     data['Beta'] = beta
#    
#     return alpha, beta
#
# for i in range(len(df)):
#     if i > 0:
#         df['Alpha'][i], df['Beta'][i] = calc_alpha_beta(df[:i], benchmark_df[:i])
#
# window = 30
# df['Alpha MA'] = df['Alpha'].rolling(window).mean()
# df['Beta MA'] = df['Beta'].rolling(window).mean()
# df['Volatility'] = df['Returns'].rolling(window).std() * np.sqrt(window)
#
# # Plot alpha and beta for the last year
# plt.plot(df['Alpha'][-365:], label='Alpha')
# plt.show()
df.rename(columns={'Close': 'PX_LAST'}, inplace=True)
df.rename(columns={'Volume': 'PX_VOLUME'}, inplace=True)
df = df[::-1]
df.to_csv('DFAC US Equity.csv')
