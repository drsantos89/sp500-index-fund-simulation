import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def per_year_boxplot(data):
    fig, ax = plt.subplots(figsize=(6.4*2, 4.8))
    sns.boxplot(x=data[data['len']==1]['year'],
                y=data[data['len']==1].annualized_returns.explode(), ax=ax)
    plt.xticks(rotation=90)

def per_month_boxplot():
    fig, ax = plt.subplots(figsize=(6.4*2, 4.8))
    sns.boxplot(x=data[data['len']==1]['month'],
                y=data[data['len']==1].annualized_returns.explode(), ax=ax)
    plt.xticks(rotation=90)