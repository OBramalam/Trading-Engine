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
        self.portfolio_values = []
        self.portfolio_history = []

    
    def run_backtest(self):
        risk_per_trade = 1
        
        print("Building signals...")
        signals = self.build_signals()

        for index, row in self.data.iterrows():
            close_price = row['Close']
            signal = row['signal'] 

            if signal > 0: # buy
                available_cash = self.portfolio['cash']
                current_position = self.portfolio['positions'].get(self.data.name, 0)

                if current_position == 0:
                    position_size = available_cash * risk_per_trade / close_price
                    self.execute_trade(symbol=self.data.name, quantity=position_size, price=close_price)

            elif signal < 0: # sell
                position_size = self.portfolio['positions'].get(self.data.name, 0)

                if position_size > 0:
                    self.execute_trade(symbol=self.data.name, quantity=-position_size, price=close_price)

            current_portfolio_value = self.get_portfolio_value(close_price)
            self.portfolio_values.append(current_portfolio_value)
            
            self.portfolio_history.append({
                'cash': self.portfolio['cash'],
                'positions': self.portfolio['positions'].copy()
            })


    def build_signals(self):
        signal_series = None

        for config in self.signals_configs:
            signal_func = available_signals[config["name"]]
            signal = signal_func(self.data, **config["params"])

            if signal_series is None:
                signal_series = signal
            else:
                # add signals together so a buy and sell signal will cancel each other out when evaluated by run_backtest
                signal_series = signal_series + signal 
        
        self.data['signal'] = signal_series

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

        buy_mask = trade_quantities > 0
        sell_mask = trade_quantities < 0

        buy_prices = trade_prices[buy_mask]
        sell_prices = trade_prices[sell_mask]

        min_trades = min(len(buy_prices), len(sell_prices))
        buy_prices = buy_prices[:min_trades]
        sell_prices = sell_prices[:min_trades]

        trade_returns = (sell_prices - buy_prices) / buy_prices

        trade_quantities = trade_quantities[trade_quantities > 0]

        trade_pnl = trade_returns * trade_quantities[:-1]

        total_pnl = np.sum(trade_pnl)
        average_trade_return = np.mean(trade_returns)
        win_ratio = np.sum(trade_pnl > 0) / len(trade_pnl)

        return total_pnl, average_trade_return, win_ratio


    def get_portfolio_value(self, price):
        positions_value = sum(self.portfolio['positions'].get(symbol, 0) * price for symbol in self.portfolio['positions'])
        return self.portfolio['cash'] + positions_value


    def get_portfolio_returns(self):
        returns = np.diff(self.portfolio_values) / self.portfolio_values[:-1]
        return returns


    def print_portfolio_summary(self):
        print('--- Portfolio Summary ---')
        print('Cash:', self.portfolio['cash'])
        print('Positions:')
        for symbol, quantity in self.portfolio['positions'].items():
            print(symbol + ':', quantity)


    def plot_portfolio_value(self, plot_signals=True):
        dates = self.data.index
        signals = self.data['signal']

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot portfolio value
        ax1.plot(dates, self.portfolio_values, label='Portfolio Value')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Portfolio Value')
        ax1.set_title('Portfolio Value Over Time')

        if plot_signals:
            ax2 = ax1.twinx()
            ax2.plot(dates, signals, 'r-', label='Buy/Sell Signal')
            ax2.set_ylabel('Signal')
            ax2.grid(None)

        fig.tight_layout()
        plt.show()