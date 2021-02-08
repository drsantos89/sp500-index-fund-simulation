import pandas as pd
import random
import numpy as np

data = pd.read_csv('data.csv')
data['pct'] = data['SP500'].pct_change() + 1

class Sim(object):
    def __init__(self, config):
        
        self.config = config
        
    def run(self):
        if self.config['buy'] == 'lump_sum':
            self._lump_sum_buy()
        elif self.config['buy'] == 'dca':
            self._dollar_cost_average()
        else:
            raise NotImplementedError
            
        self._current_valuation()
        
        if self.config['dividends']:
            self._reinvest_dividends()
        else:
            self.dividend = 0
            
        self.gain = self.value/self.cost*100 + self.dividend/self.value*100 - 100
        
    def _lump_sum_buy(self):
        
        year = self.config['buy_year']
        month = self.config['buy_month']
        
        buy = data[data['Date']==f"{year}-{month:02d}-01"]
        self.cost = buy['SP500'].iat[0]
        
    def _current_valuation(self):
        
        year = self.config['sell_year']
        month = self.config['sell_month']
        
        sell = data[data['Date']==f"{year}-{month:02d}-01"]
        self.value = sell['SP500'].iat[0]
        
    def _reinvest_dividends(self):
        dividends = []
        
        year = self.config['buy_year']
        for month in range(self.config['buy_month'], 12+1):
            buy = data[data['Date']==f"{year}-{month:02d}-01"]
            dividends.append(buy['Dividend'].iat[0])
            
        for year in range(self.config['buy_year']+1, self.config['sell_year']):
            for month in range(1, 12+1):
                buy = data[data['Date']==f"{year}-{month:02d}-01"]
                dividends.append(buy['Dividend'].iat[0])
        
        year = self.config['sell_year']
        for month in range(1, self.config['sell_month']):
            buy = data[data['Date']==f"{year}-{month:02d}-01"]
            dividends.append(buy['Dividend'].iat[0])

        self.dividend = np.sum(dividends)/12
    
    def _dollar_cost_average(self):
        valuations = []
        
        year = self.config['buy_year']
        for month in range(self.config['buy_month'], 12+1):
            buy = data[data['Date']==f"{year}-{month:02d}-01"]
            valuations.append(buy['SP500'].iat[0])
            
        for year in range(self.config['buy_year']+1, self.config['sell_year']):
            for month in range(1, 12+1):
                buy = data[data['Date']==f"{year}-{month:02d}-01"]
                valuations.append(buy['SP500'].iat[0])
        
        year = self.config['sell_year']
        for month in range(1, self.config['sell_month']):
            buy = data[data['Date']==f"{year}-{month:02d}-01"]
            valuations.append(buy['SP500'].iat[0])

        self.cost = np.mean(valuations)
        
        b_y = self.config['buy_year']
        b_m = self.config['buy_month']
        s_y = self.config['sell_year']
        s_m = self.config['sell_month']
        
        row_start = data[data['Date']==f"{b_y}-{b_m:02d}-01"].index[0]
        row_end = data[data['Date']==f"{s_y}-{s_m:02d}-01"].index[0]
        
        self.portfolio = 1
        for i_row in range(row_start+1, row_end):
            self.portfolio *= data.loc[i_row, 'pct'] + 1
            
    
years = [random.randint(1871,1987) for x in range(1000)]
months = [random.randint(1,12) for x in range(1000)]
lengths = [1,2,3,5,10,20,30]

res = pd.DataFrame(columns=['length',
                            'mean',
                            'mean_annualized',
                            'median',
                            'median_annualized',
                            'std',
                            'iqr',
                            'gains'])

for il, length in enumerate(lengths):
    gains = []
    for year, month in zip(years, months):
        config={'buy': 'dca',
                'buy_year': year,
                'buy_month': month,
                'sell_year': year+length,
                'sell_month': month,
                'dividends': True}
        
        sim = Sim(config)
        sim.run()
        gains.append(sim.gain)
    res.at[il, 'length'] = length
    res.at[il, 'mean'] = np.mean(gains)
    res.at[il, 'mean_annualized'] = res.at[il, 'mean']/length
    res.at[il, 'median'] = np.median(gains)
    res.at[il, 'median_annualized'] = res.at[il, 'median']/length
    res.at[il, 'std'] = np.std(gains)
    res.at[il, 'iqr'] = np.quantile(gains, 0.75) - np.quantile(gains, 0.25)
    res.at[il, 'wins'] = np.sum(np.array(gains) > 0)
    res.at[il, 'losses'] = np.sum(np.array(gains) < 0)
    res.at[il, 'wins/losses'] = res.at[il, 'wins'] / res.at[il, 'losses']
    res.at[il, 'gains'] = gains

import matplotlib.pyplot as plt
plt.hist(res, bins=100)