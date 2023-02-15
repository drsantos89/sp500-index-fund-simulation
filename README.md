# Simulate investments on the S&P500 index fund

This repository contains the code use to produce the results publish on:
https://wire.insiderfinance.io/what-to-expect-from-investing-in-s-p-500-index-funds-52185812bc3

## How to run:

    python main_v2.py <config>

where config is the name of the config file in the config folder.

## Config file structure:

- buy:
  - lumpsum: simulates a lump-sum investment
  - dca: simulats dolar-cost-averaging
- dividends (reinvest)
   - true
   - false
- year (to start investing)
  - int or list from 1872 to 2021
- months (to start investing)
  - int or list from 1 to 12
- lengths (of the investment in years)
  - int from 1

## Outputs:

Results are saved as CSVs in the results folder
