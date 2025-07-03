from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import FinancialStatement, SectorsPERatio
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assumed tickers of large-cap companies outperforming S&P 500's long-term average. 
        # These should be determined through external analysis since direct comparison isn't possible here.
        self.tickers = ["AAPL", "MSFT", "GOOG", "AMZN"]
        self.data_list = [FinancialStatement(i) for i in self.tickers] + [SectorsPERatio()]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}

        # Example logic to potentially reflect outperformance, can be refined based on actual strategy.
        # Here we're simplistically allocating based on a RSI indicator as a proxy for strength/performance.
        for ticker in self.tickers:
            rsi = RSI(ticker, data["ohlcv"], 14)  # Assuming a 14-day RSI
            
            # If RSI indicates the stock is not overbought, allocate to it, 
            # assuming it signifies potentially continuing upward momentum without being overvalued.
            if rsi and rsi[-1] < 70: 
                allocation_dict[ticker] = 0.25  # Equally divide the allocation among selected tickers.
            else:
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)