#Import yfinance and pandas library
import yfinance as yf
import pandas as pd

#Determine IHSG ticker on Yahoo Finance
thicker_ihsg = "^JKSE"

#Determine time periodd (Format : YYYY-MM-DD)
start_date = "2026-01-01"
end_date = "2026-04-01"

print(f'Currently pulling IHSG data from {start_date} to {end_date} ..........')

#Downloading data using yfinance
data_ihsg = yf.download(thicker_ihsg, start=start_date, end=end_date)
data_ihsg.columns = data_ihsg.columns.get_level_values(0)

#take only open, high, low, close, and volume columns
ihsg_full_data = data_ihsg[['Open','High','Low','Close','Volume']].round(0)

#Change the date data format
ihsg_full_data.reset_index(inplace=True)
ihsg_full_data['Date'] = ihsg_full_data['Date'].dt.strftime('%d-%m-%Y')

#Save data in .csv format
file_output = 'IHSG_Jan_Mar_2026.csv'
ihsg_full_data.to_csv(file_output, index=False)

print('Extract complete')
