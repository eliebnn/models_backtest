from models_backtest.models.grid_trading import GridTrading
from pnl_report.methods import PnLMethods

# This repo can be downloaded here: https://github.com/eliebnn/pnl_report

import pandas as pd
import random


def get_pnl_report(grid):

    df = pd.DataFrame()

    df['qty'] = [t.qty for t in grid.trades]
    df['price'] = [t.price for t in grid.trades]

    return PnLMethods(data=df, method='avg').run()


if __name__ == '__main__':

    values = list(range(0, 100, 1)) * 5
    random.shuffle(values)

    levels = [20, 25, 30, 35, 40, 45]
    base_quantity = 1

    grid = GridTrading(levels=levels, values=values, base_qty=base_quantity).run()
    pnl = get_pnl_report(grid)

    print(f"Your P&L is: {pnl.pnl}")
    print(f"Number of Trades: {grid.trades}")

    print()
