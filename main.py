from modules import *

today = datetime.today().strftime('%Y-%m-%d')
lastmonth = datetime.today() - timedelta(days=30)
# functions.download_forex_data(lastmonth, today, "USD", "MUR")

df = pd.read_excel('forex_data.xlsx', index_col=None, header=None)  

# If today's rate is added to the data, proceed.. else exit(0)

# Find the index where "SELLING" appears
selling_row_idx = df[df.isin(['SELLING']).any(axis=1)].index[0]

# Find the column index where "TT" appears in the same row as "SELLING"
tt_column_idx = df.iloc[selling_row_idx][df.iloc[selling_row_idx] == 'TT'].index[0]

# Select the column with numerical values under "TT" and "SELLING" and add them to an array

# calculate mean
