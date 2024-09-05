from modules import *

today = datetime.today().strftime('%Y-%m-%d')
lastmonth = datetime.today() - timedelta(days=30)

functions.download_forex_data(lastmonth,today, "USD", "MUR")

df = pd.read_excel('forex_data.xlsx', index_col=None, header=None)  
print(df)
# If today's rate is added to the data, proceed.. else exit(0)
# functions.checkifrateistoday()

column_with_selling_tt=functions.find_column(df)

# Check if the column was found
if column_with_selling_tt is not None:
    # Find the mean of the numeric values in the found column
    numeric_values = pd.to_numeric(df[column_with_selling_tt], errors='coerce')
    print(numeric_values)
    mean_value = numeric_values.mean()
    print(f"Mean of the values in the column with 'SELLING' and 'TT': {mean_value}")
else:
    print("No rates column found.")

