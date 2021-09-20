import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def sp500_level(data=None):
    sns.lineplot(data['Date'].astype('datetime64[ns]'),
                 data['SP500'])
       
def per_year_boxplot(data=None):
    fig, ax = plt.subplots(figsize=(6.4*2, 4.8))
    sns.boxplot(x=data[data['len']==1]['year'],
                y=data[data['len']==1].annualized_returns.explode(),
                ax=ax)
    plt.xticks(rotation=90)

def per_month_boxplot(data=None):
    fig, ax = plt.subplots(figsize=(6.4*2, 4.8))
    sns.boxplot(x=data[data['len']==1]['month'],
                y=data[data['len']==1].annualized_returns.explode(),
                ax=ax)
    plt.xticks(rotation=90)
    
def years_boxplot(data=None):
    fig, ax = plt.subplots(figsize=(6.4*2, 4.8))
    sns.boxplot(data=data,
                x='len',
                y='gain',
                ax=ax)
    
def years_boxplot(data=None):
    fig, ax = plt.subplots(figsize=(6.4*2, 4.8))
    sns.histplot(data=data,
                x='len',
                y='gain',
                ax=ax)
def years_boxplot(data=None, year=None):
    date = data[data.len==year].apply(
        lambda x: f"{x['year']}-{x['month']}", axis=1).astype('datetime64[ns]')
    plt.plot(date, data[data.len==year]['gain'])

def over_the_years(data, length):  
    date = data[data.len==length].apply(lambda x: f"{x['year']}-{x['month']}", axis=1).astype('datetime64[ns]')
    fig, ax = plt.subplots(figsize=(6.4*2, 4.8))
    plt.plot(date, data[data.len==length]['gain'])
    plt.axhline(data[data.len==length]['gain'].mean(), c='r', ls='--')
    plt.xlabel('year')
    plt.ylabel(f'{length}-year gain')
