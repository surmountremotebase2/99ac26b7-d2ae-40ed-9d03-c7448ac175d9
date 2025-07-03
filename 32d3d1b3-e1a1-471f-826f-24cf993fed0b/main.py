from surmount.base_class import Strategy, TargetAllocation
from surmount.data import FinancialStatement, Asset
from surmount.technical_indicators import SMA, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a broad list of tickers known to have high market caps, focusing on diversification across sectors.
        self.tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "FB", "BRK.B"]
        self.data_list = [FinancialStatement(i) for i in self.tickers] + [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        # Using daily data for long-term trend analysis.
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        selected_stocks = []

        for ticker in self.tickers:
            financials = data.get(("financial_statement", ticker), [])
            asset_info = data.get(("asset", ticker), {})
            if not financials or not asset_info:
                log(f"Missing data for {ticker}")
                continue

            # Check if latest market cap is greater than $200 billion
            if asset_info.get("marketCap", 0) > 200e9:
                # Simple strategy: Look for companies with positive net income and revenue growth as a sign of strong fundamentals.
                latest_financials = financials[0]
                if latest_financials["netIncome"] > 0 and latest_financials["revenue"] > latest_financials.get("lastRevenue", 0):
                    selected_stocks.append(ticker)

        # Equally distribute allocation among selected stocks
        if selected_stocks:
            allocation = 1.0 / len(selected_stocks)
            for ticker in selected_stocks:
                allocation_dict[ticker] = allocation
        else:
            log("No stocks meet the criteria, maintaining current positions.")
            return TargetAllocation({})  # Optionally adjust to handle no suitable investments found.

        return TargetAllocation(allocation_dict)