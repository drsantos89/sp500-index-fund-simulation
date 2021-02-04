import pandas as pd
import random

data = pd.read_csv('data.csv')

def sim(year, month, len_):
    
    buy = data[data['Date']==f"{year}-{month}-01"]
    buy = buy['SP500'].iat[0]
    
    sell = data[data['Date']==f"{year+len_}-{month}-01"]
    sell = sell['SP500'].iat[0]
    
    val = sell-buy
    
    return val

years = [random.randint(1871,1997) for x in range(20)]

for i in years:
    print(i)
    print(sim(i, '05', 20))
    