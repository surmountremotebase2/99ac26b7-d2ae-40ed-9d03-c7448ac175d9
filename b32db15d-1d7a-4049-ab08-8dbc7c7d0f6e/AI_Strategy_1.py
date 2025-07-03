from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA, MACD  # Although not used directly in filtering based on your criteria, these can be part of more complex strategies.

class RevenueGrowthFCFROICStrategy(Strategy):
    def __init__(self):
        # Preset list of stocks that have been identified to meet the criteria
        # This list should be updated based on an external analysis of financial metrics
        self.selected_stocks = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D"]  # Example tickers, replace with actual ones that meet the financial metrics criteria

    @property
    def assets(self):
        # The strategy is focused on a predefined set of stocks
        return self.selected_stocks

    @property
    def interval(self):
        # Let's assume daily data is sufficient for our needs
        return "1day"

    @property
    def data(self):
        # No additional data sources are required here as the selection is based on fundamental criteria outside Surmount
        return []

    def run(self, data):
        allocation_dict = {}

        # Equally weighting the investment across the selected stocks
        equal_weight = 1 / len(self.selected_stocks)
        for stock in self.selected_stocks:
            allocation_dict[stock] = equal_weight

        return TargetAllocation(allocation_dict)