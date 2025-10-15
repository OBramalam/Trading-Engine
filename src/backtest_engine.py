import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from .signals.signal_registry import available_signals


class BacktestEngine():
    def __init__(self, data, start_value, signal_configs):
        self.data = data
        self.portfolio = {'cash': start_value, 'positions': {}}
        self.signals_configs = signal_configs
        self.trades = []

    
    def run_backtest(self):
        risk_per_trade = 0.02 

        signals = self.build_signals()
        self.data['signal'] = signals
        print("Data:")
        print(self.data)

        for index, row in self.data.iterrows():
            close_price = row['Close']
            signal = row['signal'] 

            if signal < 0: # buy
                available_cash = self.portfolio['cash']
                position_size = available_cash * risk_per_trade / close_price
                self.execute_trade(symbol=self.data.name, quantity=position_size, price=close_price)
            elif signal > 0: # sell
                position_size = self.portfolio['positions'].get(self.data.name, 0)
                if position_size > 0:
                    self.execute_trade(symbol=self.data.name, quantity=-position_size, price=close_price)


    def build_signals(self):
        signal_series = []

        for config in self.signals_configs:
            signal_func = available_signals[config["name"]]
            signal = signal_func(self.data, **config["params"])

            if signal_series.len == 0:
                signal_series = signal
            else:
                # add signals together so a buy and sell signal will cancel each other out when evaluated by run_backtest
                signal_series = signal_series + signal 

        return signal_series


    def execute_trade(self, symbol, quantity, price):

        self.portfolio['cash'] -= quantity * price

        if symbol in self.portfolio['positions']:
            self.portfolio['positions'][symbol] += quantity
        else:
            self.portfolio['positions'][symbol] = quantity

        self.trades.append({'symbol': symbol, 'quantity': quantity, 'price': price})


    def calculate_performance(self):
        # Calculate performance metrics based on executed trades
        trade_prices = np.array([trade['price'] for trade in self.trades])
        trade_quantities = np.array([trade['quantity'] for trade in self.trades])

        trade_returns = np.diff(trade_prices) / trade_prices[:-1]
        trade_pnl = trade_returns * trade_quantities[:-1]

        total_pnl = np.sum(trade_pnl)
        average_trade_return = np.mean(trade_returns)
        win_ratio = np.sum(trade_pnl > 0) / len(trade_pnl)

        return total_pnl, average_trade_return, win_ratio



    def get_portfolio_value(self, price):
        positions_value = sum(self.portfolio['positions'].get(symbol, 0) * price for symbol in self.portfolio['positions'])
        return self.portfolio['cash'] + positions_value


    def get_portfolio_returns(self):
        portfolio_value = [self.get_portfolio_value(row['Close']) for _, row in self.data.iterrows()]
        returns = np.diff(portfolio_value) / portfolio_value[:-1]
        return returns


    def print_portfolio_summary(self):
        print('--- Portfolio Summary ---')
        print('Cash:', self.portfolio['cash'])
        print('Positions:')
        for symbol, quantity in self.portfolio['positions'].items():
            print(symbol + ':', quantity)


    def plot_portfolio_value(self):
        portfolio_value = [self.get_portfolio_value(row['Close']) for _, row in self.data.iterrows()]
        dates = self.data.index
        signals = self.data['signal']

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot portfolio value
        ax1.plot(dates, portfolio_value, label='Portfolio Value')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Portfolio Value')
        ax1.set_title('Portfolio Value Over Time')

        # Plot buy/sell signals
        ax2 = ax1.twinx()
        ax2.plot(dates, signals, 'r-', label='Buy/Sell Signal')
        ax2.set_ylabel('Signal')
        ax2.grid(None)

        fig.tight_layout()
        plt.show()