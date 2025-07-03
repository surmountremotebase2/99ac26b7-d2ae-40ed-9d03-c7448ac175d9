from surmount.base_class import Strategy, TargetAllocation
from surmount.data import FinancialStatement, Ratios, Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Assuming 'tickers' is a predefined list of tickers for companies with >$200Bn Market Cap
        # In a real-world scenario, this list would have to be dynamically generated based on market data
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]
        # Adding FinancialStatement and Ratios to data_list for further analysis
        self.data_list = [FinancialStatement(i) for i in self.tickers] + [Ratios(i) for i in self.tickers]

    @property
    def interval(self):
        # Using daily data for analysis
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Simplified check: Assuming 'returnOnEquity' as a proxy to company's performance against SPY's average
            # This part of the logic would need more sophisticated financial analysis and access to historic SPY return data
            ratios_data = data.get(("ratios", ticker), [])
            if ratios_data:
                latest_ratios = ratios_data[-1]
                roe = latest_ratios.get("returnOnEquity", 0)
                # Check if ROE is significantly higher than SPY's average; here assumed SPY's baseline ROE is 10%
                # The assumption is a simplification, real strategy would need actual performance data comparison
                if roe > 20:  # Assuming that a 20% ROE is indicative of outperforming SPY's return by 2x
                    allocation_dict[ticker] = 1 / len([ticker for ticker in self.tickers if ticker in allocation_dict])
                else:
                    allocation_dict[ticker] = 0
            else:
                # No data available for the ticker, no allocation
                allocation_dict[ticker] = 0
        
        # Normalizing the allocations to ensure they sum up to 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 0:
            for ticker in allocation_dict:
                allocation_dict[ticker] = allocation_dict[ticker] / total_allocation

        return TargetAllocation(allocation_dict)