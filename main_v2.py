import argparse
import json
import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format
import random
import numpy as np
import tqdm

from src.sim import Sim

def run(params):
    data = pd.read_csv('./data/sp500.csv')

    res = pd.DataFrame(
        columns=['length','mean','median','std','iqr',
                 'wins','losses','zero','total','wins/losses',
                 'a_r_mean','a_r_median','a_r_std'])
    
    res_all = pd.DataFrame(
        columns=['len', 'year', 'month',
                 'gain', 'annualized_returns'])
    
    for i_l, length in enumerate(params['lengths']):
        for i_y, year in enumerate(params['years']):
            for i_m, month in enumerate(params['months']):
                try:
                    config={'buy': params['buy'],
                            'buy_year': year,
                            'buy_month': month,
                            'sell_year': year+length,
                            'sell_month': month,
                            'dividends': params['dividends'],
                            'inflation_corrected': False}
                    
                    sim = Sim(config, data)
                    sim.run()

                    i_res_all = i_l*len(params['years'])*len(params['months']) + \
                        i_y*len(params['months']) + i_m
                    res_all.at[i_res_all, 'len'] = length
                    res_all.at[i_res_all, 'year'] = year
                    res_all.at[i_res_all, 'month'] = month
                    res_all.at[i_res_all, 'gain'] = sim.gain
                    res_all.at[i_res_all, 'annualized_returns'] = sim.annualized_returns
                except Exception as e:
                    print(length, year, month, e)
                    res_all.at[i_res_all, :] = np.nan
                    
        res.at[i_l, 'length'] = length
        res.at[i_l, 'mean'] = np.mean(res_all[res_all['len']==length]['gain'])
        res.at[i_l, 'median'] = np.median(res_all[res_all['len']==length]['gain'])
        res.at[i_l, 'std'] = np.std(res_all[res_all['len']==length]['gain'])
        res.at[i_l, 'iqr'] = np.quantile(
            res_all[res_all['len']==length]['gain'], 0.75) - \
            np.quantile(res_all[res_all['len']==length]['gain'], 0.25)
        res.at[i_l, 'wins'] = np.sum(res_all[res_all['len']==length]['gain'] > 0)
        res.at[i_l, 'losses'] = np.sum(res_all[res_all['len']==length]['gain'] < 0)
        res.at[i_l, 'zero'] = np.sum(res_all[res_all['len']==length]['gain'] == 0)
        res.at[i_l, 'total'] = res.at[i_l, 'wins'] + res.at[i_l, 'losses'] + res.at[i_l, 'zero']
        res.at[i_l, 'wins/losses'] = res.at[i_l, 'wins'] / res.at[i_l, 'losses']
        res.at[i_l, 'a_r_mean'] = np.mean(np.vstack(res_all[res_all['len']==length]['annualized_returns']))
        res.at[i_l, 'a_r_median'] = np.median(np.vstack(res_all[res_all['len']==length]['annualized_returns']))
        res.at[i_l, 'a_r_std'] = np.std(np.vstack(res_all[res_all['len']==length]['annualized_returns']))
    res_all.to_csv(f'./results/res_all_buy_{params["buy"]}_dividends_{params["dividends"]}.csv')
    res.to_csv(f'./results/res_buy_{params["buy"]}_dividends_{params["dividends"]}.csv')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="path to config file")
    args = parser.parse_args()
    params = json.load(open('./config/'+args.config_file+'.json', 'r'))
    run(params)