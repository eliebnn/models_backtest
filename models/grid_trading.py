from pnl_report.methods import PnLMethods

import pandas as pd


class Level:

    def __init__(self, level=None, side='STATIC'):
        self.level = level
        self.side = side

    def to_buy(self):
        self.side = 'BUY'

    def to_sell(self):
        self.side = 'SELL'

    def to_static(self):
        self.side = 'STATIC'


class Trade:

    def __init__(self, qty, price, tsp=None):
        self.qty = qty
        self.price = price
        self.tsp = tsp


class GridTrading:

    def __init__(self, levels, values, base_qty=1):
        self.levels = {l: Level(level=l) for l in levels}
        self.values = values
        self.trades = []

        self.base_qty = base_qty
        self.init()

    def init(self):
        for l in self.levels.keys():
            if self.values[0] > l:
                self.levels[l].to_buy()

        self.levels[list(self.levels)[0]].to_buy()

    def get_id(self, price):
        return sum([1 if price >= l else 0 for l in self.levels.keys()] + [-1])

    def is_crossing(self, price, prev_price):
        return False if self.get_id(prev_price) == self.get_id(price) else True

    def crossed_level_id(self, price, prev_price):
        prev_id = self.get_id(prev_price)
        level_id = self.get_id(price)

        return False if prev_id == level_id else max([prev_id, level_id])

    def add_trade(self, qty, price):
        return self.trades.append(Trade(qty, price))

    def is_valid_id(self, level_id):
        return True if level_id in range(0, (len(self.levels) - 1)) else False

    def run(self):

        for idx, price in enumerate(self.values):

            previous = self.values[idx - 1] if idx else price

            if not self.is_crossing(price, previous):
                continue

            level_id = self.crossed_level_id(price, previous)
            level = list(self.levels.keys())[level_id]

            if self.levels[level].side == 'BUY':
                self.trades.append(Trade(self.base_qty, price))

                self.levels[level].to_static()
                if self.is_valid_id(level_id + 1):
                    self.levels[list(self.levels.keys())[level_id + 1]].to_sell()

            if self.levels[level].side == 'SELL':
                self.trades.append(Trade(-self.base_qty, price))

                self.levels[level].to_static()
                if self.is_valid_id(level_id - 1):
                    self.levels[list(self.levels.keys())[level_id - 1]].to_buy()

        return self

    def get_pnl_report(self):

        df = pd.DataFrame()

        df['qty'] = [t.qty for t in self.trades]
        df['price'] = [t.price for t in self.trades]

        return PnLMethods(data=df, method='avg').run()


if __name__ == '__main__':
    pass