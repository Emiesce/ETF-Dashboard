# ETF-Dashboard

## Overview

This Dashboard is separated into four pages (each coded in the Pages module), an ETF Filtering System (feature1), a Competitor Analysis Feature (feature2), a Macroeconomic Indciator System (Macro) and a Recommendation System (feature3). Developed in Python and using the DASH library, the codebase also contains the necessary data downloaded from various sources (Bloomberg Terminal etc.) to demonstrate the capabilities of each feature using real data. The ETF Filter system relies on a NLP algorithm imported from the open-source library "fastText" to perform constituent-level filterig.

## Dependencies

To install all required packages (after having installed Python 3.11.4), run "pip install -r requirements.txt" to install all necessary dependencies. The requirements.txt file contains a list of all libraries and dependencies and their respective versions used to develop and run the dashboard.

## File Structure

The "Pages" Folder contains the actual Python code for each feature including the backend code integrated into the frontend. Each feature is simply designated as feature1, feature2, and feature3, it also contains "data" Folder containing the holdings and constituents for the ETF Filter feature. "price data" contains the prices for certain ETFs for the timeseries demo on the dashboard, and the "static" folder contains the metrics for each ETF (to showcase on the Competitor Analysis feature) and the descriptions of each client in the Recommendation System feature. "macro data" contains data for the macroeconomic indicator feature, and the "assets" folder contains various imported images and logos to display on the dashboard. 

## Before Running

The ETF Filter feature requires a machine learning model from the "fastText" library to be installed, which will occur automatically after running the dashboard once. This will require at least 8 GB of free storage space to properly install. No cofnigurations files or settings are needed otherwise.

## How to Run
After unzipping the file, in order to run the dashboard, type "python dashboard.py" or "python3 dashboard.py" in your Terminal. Make sure you have installed the necessary dependencies (i.e. run "pip install -r requirements.txt") after installing the proper version of Python. After the following output "Dash is running on http://127.0.0.1:8050/" in the Terminal appears, input "http://127.0.0.1:8050/" into your browser to access the dashboard.

Technology Used: Python, Plotly Dash, TailwindCSS, fastText Library, Pandas, NumPy

Python version: 3.11.4

## Considerations while running code

While running the code, any changes made in the Python code will be udpated in real-time. Refrain from editing the code unless you are actively working on modifying the codebase to avoid breaking the dashboard pages. Additionally, certain ETFs will not have Price or Constituent Filtering data to display in various features (e.g. Price Data for most ETFs are non-existent, as well as the Filtering system), please review the Tickers in "price data" and "data" before testing the Timeseries Chart and ETF Filter features respectively to see what data can actually be shown.

