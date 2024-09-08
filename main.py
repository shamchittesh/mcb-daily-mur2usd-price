from modules import *

USD1 = 46.66
USD2 = USD1-2

Amount = 500000
USD1TR = 500000/USD1
USD2TR = 500000/USD2

diff = USD2TR - USD1TR
diff_mru = diff*USD2
print(f'amountUSD {USD2TR}')
print(f'diffusd = {diff} / diffmur =  {diff_mru}')

today = datetime.today().strftime('%Y-%m-%d')
lastmonth = datetime.today() - timedelta(days=30)

functions.download_forex_data(lastmonth,today, "USD", "MUR")

df = pd.read_excel('forex_data.xlsx', index_col=None, header=None)  
print(df)
# If today's rate is added to the data, proceed.. else exit(0)
# functions.checkifrateistoday()


column_with_selling_tt=functions.find_column(df)
lastprice = functions.get_lastprice(df,column_with_selling_tt)
mean=functions.get_mean(df,column_with_selling_tt)

# is2pct = functions.isdeviation(mean,2)
# is5pct = functions.isdeviation(mean,5)
# is10pct = functions.isdeviation(mean,10)