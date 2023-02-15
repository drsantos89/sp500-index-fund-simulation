"""Scimulate the performance of a portfolio."""
from typing import Any

import numpy as np
import pandas as pd


class Sim:
    """Simulate the performance of a portfolio."""

    def __init__(self, config: dict[str, Any], data: pd.DataFrame) -> None:
        self.config = config
        self.data = data

        self.portfolio: float = 1
        self.previous_year: float = 0
        self.gain: float = 0
        self.annualized_returns: list[float] = []

    def run(self) -> None:
        """Run the simulation."""
        if self.config["buy"] == "lump_sum":
            self._lump_sum()
        elif self.config["buy"] == "dca":
            self._dollar_cost_average()
        else:
            raise NotImplementedError
        self._annualized_returns()

    def _get_rows(self) -> tuple[int, int]:
        """Get the start and end row of the simulation period."""
        b_y = self.config["buy_year"]
        b_m = self.config["buy_month"]
        s_y = self.config["sell_year"]
        s_m = self.config["sell_month"]

        row_start = self.data[self.data["Date"] == f"{b_y}-{b_m:02d}-01"].index[0]
        row_end = self.data[self.data["Date"] == f"{s_y}-{s_m:02d}-01"].index[0]

        return row_start, row_end

    def _lump_sum(self) -> None:
        """Simulate a lump sum investment."""
        row_start, row_end = self._get_rows()

        self.portfolio = 1
        self.annualized_returns = [self.portfolio]

        for i, i_row in enumerate(range(row_start, row_end)):
            self.portfolio *= self.data.loc[i_row, "pct"]

            if self.config["dividends"]:
                dividend_pct = self.data.loc[i_row, "Dividend"] / 12 + 1
                self.portfolio *= dividend_pct

            if (i + 1) % 12 == 0:
                self.annualized_returns.append(self.portfolio)

        self.gain = (self.portfolio - 1) * 100

    def _dollar_cost_average(self) -> None:
        """Simulate a dollar cost average investment."""
        row_start, row_end = self._get_rows()

        self.portfolio = 0
        self.previous_year = 0
        self.annualized_returns = [1.0]

        for i, i_row in enumerate(range(row_start, row_end)):
            self.portfolio += 1

            self.portfolio *= self.data.loc[i_row, "pct"]
            if self.config["dividends"]:
                dividend_pct = self.data.loc[i_row, "Dividend"] / 12 + 1
                self.portfolio *= dividend_pct

            if (i + 1) % 12 == 0:
                self.annualized_returns.append(
                    self.portfolio / (self.previous_year + 12)
                )
                self.previous_year = self.portfolio

        self.gain = (self.portfolio / (row_end - row_start) - 1) * 100

    def _annualized_returns(self) -> None:
        """Calculate the annualized returns."""
        self.annualized_returns = (
            np.array(self.annualized_returns[1:])
            / np.array(self.annualized_returns[:-1])
            * 100
            - 100
        )
