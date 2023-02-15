"""Script to generate figures for the report."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set()


def sp500_level(data: pd.DataFrame) -> None:
    """Plot the level of the S&P500 index."""
    sns.lineplot(data["Date"].astype("datetime64[ns]"), data["SP500"])


def per_year_boxplot(data: pd.DataFrame) -> None:
    """Plot the boxplot of the annualized returns per year."""
    fig, ax = plt.subplots(figsize=(6.4 * 2, 4.8))
    sns.boxplot(
        x=data[data["len"] == 1]["year"],
        y=data[data["len"] == 1].annualized_returns.explode(),
        ax=ax,
    )
    plt.xticks(rotation=90)


def per_month_boxplot(data: pd.DataFrame) -> None:
    """Plot the boxplot of the annualized returns per month."""
    fig, ax = plt.subplots(figsize=(6.4 * 2, 4.8))
    sns.boxplot(
        x=data[data["len"] == 1]["month"],
        y=data[data["len"] == 1].annualized_returns.explode(),
        ax=ax,
    )
    plt.xticks(rotation=90)


def years_boxplot(data: pd.DataFrame, year: int) -> None:
    """Plot the boxplot of the annualized returns per year."""
    date = (
        data[data.len == year]
        .apply(lambda x: f"{x['year']}-{x['month']}", axis=1)
        .astype("datetime64[ns]")
    )
    plt.plot(date, data[data.len == year]["gain"])


def over_the_years(data: pd.DataFrame, length: int) -> None:
    """Plot the gain over the years."""
    date = (
        data[data.len == length]
        .apply(lambda x: f"{x['year']}-{x['month']}", axis=1)
        .astype("datetime64[ns]")
    )
    fig, ax = plt.subplots(figsize=(6.4 * 2, 4.8))
    plt.plot(date, data[data.len == length]["gain"])
    plt.axhline(data[data.len == length]["gain"].mean(), c="r", ls="--")
    plt.xlabel("year")
    plt.ylabel(f"{length}-year gain")
