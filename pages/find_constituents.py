# API key: L3BDZ3DUFUT1L0HO
import pandas as pd
import numpy as np
import csv
import requests

import yfinance as yf
import pandas as pd

stock = yf.Ticker("AAPL")
# print(stock.info)

def get_company_overview(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

def save_to_csv(etf_symbol, constituents):
    headers = ["Symbol", "Company", "Description", "Sector", "Industry"]
    rows = []

    for symbol in constituents:
        print(f'Retrieving data for {symbol}')
        try:
            overview = get_company_overview(symbol)
            company = overview['longName']
            description = overview['longBusinessSummary']
            sector = overview['sector']
            industry = overview['industry']
            rows.append([symbol, company, description, sector, industry])
        except:
            rows.append([symbol, "N/A", "N/A", "N/A", "N/A"])

    with open(f"pages/data/{etf_symbol}_constituents.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"CSV file '{etf_symbol}_constituents.csv' has been created.")

# Replace with the ETF symbol you want to retrieve constituents for
print('ETF Options: BBIN, DFAC, JEPI, JEPQ, JPST, JQUA, QQQ')
etf_symbol = input("Enter ETF symbol: ")

# constituents = get_etf_constituents(etf_symbol, api_key)
# save_to_csv(etf_symbol, constituents, api_key)

df = pd.read_csv(f"pages/data/{etf_symbol}_Holdings.csv")

constituents = df['Ticker'].tolist()
print(constituents)
save_to_csv(etf_symbol, constituents)
# info = stock.fast_info




