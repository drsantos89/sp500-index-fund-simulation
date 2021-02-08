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
            self._lump_sum()
        elif self.config['buy'] == 'dca':
            self._dollar_cost_average()
        else:
            raise NotImplementedError
    
    def _get_rows(self):
        b_y = self.config['buy_year']
        b_m = self.config['buy_month']
        s_y = self.config['sell_year']
        s_m = self.config['sell_month']
        
        row_start = data[data['Date']==f"{b_y}-{b_m:02d}-01"].index[0]
        row_end = data[data['Date']==f"{s_y}-{s_m:02d}-01"].index[0]
        
        return row_start, row_end
    
    def _lump_sum(self):
        
        row_start, row_end = self._get_rows()
        
        self.portfolio = 1
        for i_row in range(row_start+1, row_end):
            self.portfolio *= data.loc[i_row,'pct']
            if self.config['dividends']:
                dividend_pct = data.loc[i_row,'Dividend']/data.loc[i_row,'SP500']/12+1
                self.portfolio *= dividend_pct
        
        self.gain = (self.portfolio - 1) * 100
        
    def _dollar_cost_average(self):
        
        row_start, row_end = self._get_rows()
        
        self.portfolio = 1
        for i_row in range(row_start+1, row_end):
            self.portfolio *= data.loc[i_row,'pct']
            if self.config['dividends']:
                dividend_pct = data.loc[i_row,'Dividend']/data.loc[i_row,'SP500']/12+1
                self.portfolio *= dividend_pct
            self.portfolio += 1
        
        self.gain = (self.portfolio/(row_end-row_start)-1) * 100
    
    def _annualized_returns(self):
        
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
        config={'buy': 'lump_sum',
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