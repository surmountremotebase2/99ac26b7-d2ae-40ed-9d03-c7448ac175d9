from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA, MACD
from surmount.data import InsiderTrading, SectorsPERatio
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the sectors we are interested in; these can be adjusted based on current market conditions
        self.sectors = ["Technology", "Healthcare", "Consumer Discretionary", "Financials"]
        self.rsi_period = 14  # RSI calculation period
        self.sma_short_period = 50  # Short-term SMA window
        self.sma_long_period = 200  # Long-term SMA window

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        # List of assets we'll be trading; this could be ETFs that represent the sectors we're interested in
        return ["XLK", "XLV", "XLY", "XLF"]  # Technology, Healthcare, Consumer Discretionary, Financials ETFs

    @property
    def data(self):
        # Data required for strategy
        data_list = [SectorsPERatio(sector) for sector in self.sectors]
        data_list += [InsiderTrading(asset) for asset in self.assets]
        return data_list

    def run(self, data):
        allocation_dict = {}
        for asset in self.assets:
            # Fetch RSI and SMA values
            rsi_value = RSI(asset, data["ohlcv"], self.rsi_period)
            sma_short = SMA(asset, data["ohlcv"], self.sma_short_period)
            sma_long = SMA(asset, data["ohlcv"], self.sma_long_period)

            if len(rsi_value) == 0 or len(sma_short) == 0 or len(sma_long) == 0:
                continue  # Skip if data is insufficient

            # Strategy Logic: Invest in sectors when RSI is below 70 (not overbought), and short-term SMA crosses above long-term SMA (uptrend)
            if rsi_value[-1] < 70 and sma_short[-1] > sma_long[-1]:
                allocation_dict[asset] = 0.25  # Equal allocation for simplicity, can be optimized based on risk preference
            else:
                allocation_dict[asset] = 0  # No investment if conditions are not met

            # Insider Trading Check
            insider_data_key = ("insider_trading", asset)
            if insider_data_key in data and data[insider_data_key]:
                recent_insider_activity = data[insider_data_key][-1]  # Most recent record
                if recent_insider_activity['transactionType'].startswith("S"):
                    allocation_dict[asset] = 0  # Avoid investment if recent insider selling activity
            
            # Sector P/E Ratio Analysis - This section could be enhanced to compare against historical sector P/E ratios for relative valuation
            sector_pe_key = ("sectors_pe_ratio", self.sectors[self.assets.index(asset)])
            if sector_pe_key in data and data[sector_pe_key]:
                recent_sector_pe = data[sector_pe_key][-1]  # Most recent record
                # Example logic: Reduce allocation if P/E ratio is high indicating overvaluation; specific thresholds would require historical analysis
                if recent_sector_pe['pe'] > 25:  # Example: Consider high if P/E ratio is above 25
                    allocation_dict[asset] *= 0.5  # Reduce allocation
            
        # Ensure the total allocation does not exceed 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {k: v / total_allocation for k, v in allocation_dict.items()}  

        return TargetAllocation(allocation_dict)