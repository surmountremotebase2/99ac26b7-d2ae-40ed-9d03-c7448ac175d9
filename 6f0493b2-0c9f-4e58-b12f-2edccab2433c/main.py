from surmount.base_class import Strategy, TargetAllocation
from surmount.data import FinancialStatement, MarketCap

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with a list of tickers you're interested in.
        # Note: The tickers list can be dynamically generated based on external criteria,
        # but for simplicity, we're using a static list here.
        self.tickers = ["AAPL", "GOOGL", "AMZN", "MSFT", "FB"]
        
        self.data_list = []
        # Add MarketCap and FinancialStatement data requirements for each ticker
        for ticker in self.tickers:
            self.data_list += [MarketCap(ticker), FinancialStatement(ticker)]

    @property
    def interval(self):
        # Set the interval for the data. Since we're dealing with annual returns and market cap,
        # daily data interval is sufficient for our analysis.
        return "1day"

    @property
    def assets(self):
        # Return the list of tickers that the strategy should consider.
        return self.tickers

    @property
    def data(self):
        # Return the list of required data for the strategy.
        return self.data_list

    def run(self, data):
        # Initialize an empty allocation dictionary. This will be filled based on our criteria.
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Access MarketCap for each ticker
            market_cap_data = data.get(("market_cap", ticker))
            # Access FinancialStatement for each ticker
            financial_data = data.get(("financial_statement", ticker))

            # Check if both MarketCap and FinancialStatement data exist
            if market_cap_data and financial_data:
                # For simplicity, we're using the last available data point for market cap and
                # the total revenue to calculate the annual return as an example.
                # Real calculations might require more detailed financial metrics.
                
                # Check if the latest market cap is above 200 billion
                if market_cap_data[-1]['value'] > 200e9:
                    # Assuming 'revenue' gives us a proxy for company performance.
                    # Calculate the annual return. This is a simplification and should be refined.
                    current_revenue = financial_data[-1]['revenue']
                    previous_revenue = financial_data[-2]['revenue'] if len(financial_data) > 1 else 0
                    
                    if previous_revenue > 0:
                        annual_return = (current_revenue - previous_revenue) / previous_revenue
                        
                        # Check if the annual return is above 20%
                        if annual_return > 0.2:
                            allocation_dict[ticker] = 1.0 / len([t for t in self.tickers if t in allocation_dict])
        
        # Normalize allocations if necessary. This ensures the sum of the allocations does not exceed 1.
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: weight / total_allocation for ticker, weight in allocation_dict.items()}

        return TargetAllocation(allocation_dict)