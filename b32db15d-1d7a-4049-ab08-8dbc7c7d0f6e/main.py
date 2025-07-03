from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Example tickers of stocks that are presumed to have top 20% ratings in the specified criteria.
        # In practice, you would replace this list with your actual high-rated stocks based on external analysis.
        self.tickers = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]

    @property
    def interval(self):
        # The interval can be set according to the data refresh needs; assuming daily for this strategy.
        return "1day"

    @property
    def assets(self):
        # Return the list of assets (tickers) this strategy will work with.
        return self.tickers

    @property
    def data(self):
        # Assuming no additional data is needed beyond basic asset information.
        return []

    def run(self, data):
        # Equally weight the allocation for the selected stocks to distribute investment and avoid mega-cap dominance.
        # The allocation per stock is 1 divided by the number of stocks.
        allocation_per_stock = 1 / len(self.tickers)
        allocation_dict = {ticker: allocation_per_stock for ticker in self.tickers}

        # Returning the target allocation for the selected group of stocks
        return TargetAllocation(allocation_dict)