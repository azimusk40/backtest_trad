import pandas as pd
import matplotlib.pyplot as plt

class BacktestCrossMA:
    def __init__(self) -> None:
        self.df = pd.DataFrame()

    def load_data(self, path):
        self.df = pd.read_csv(path)
        self.df["time"] = pd.to_datetime(self.df["time"], unit="ms")
        self.df = self.df.set_index(self.df["time"])
        del self.df["time"]

    def populate_indicators(self):
        self.df['ma50'] = self.df['close'].rolling(50).mean()
        self.df['ma200'] = self.df['close'].rolling(200).mean()

    def populate_signals(self):
        self.df['buy_signal'] = False
        self.df['sell_signal'] = False
        self.df.loc[(self.df['ma50'] > self.df['ma200']), 'buy_signal'] = True
        self.df.loc[(self.df['ma50'] < self.df['ma200']), 'sell_signal'] = True

    def run_backtest(self):
        balance = 1000
        position = None
        asset = "BTC"

        for index, row in self.df.iterrows():

            if position is None and row['buy_signal']:
                open_price = row['close']
                position = {
                    'open_price': open_price,
                    'open_size': balance,
                }
                print(f"{index} - Buy for {balance}$ of {asset} at {open_price}$")

            elif position and row['sell_signal']:
                close_price = row['close']
                trade_result = (close_price - position['open_price']) / position['open_price']
                balance = balance + trade_result * position['open_size']
                position = None
                print(f"{index} - Sell for {balance}$ of {asset} at {close_price}$")      
            
        
        print(f"Final balance: {balance}$")
    def plot(self):
        # plot the backtest
        graph = self.df[['close', 'ma50', 'ma200']].plot(figsize=(10, 6))
        graph.set_xlabel("time")
        graph.set_ylabel("price")
        graph.scatter(
            self.df.loc[self.df['buy_signal']].index,
            self.df.loc[self.df['buy_signal']]['close'],
            marker='^',
            color='green',
            s=20
        )
        graph.scatter(
            self.df.loc[self.df['sell_signal']].index,
            self.df.loc[self.df['sell_signal']]['close'],
            marker='o',
            color='red',
            s=20
        )
        graph.legend(["close", "ma50", "ma200", "buy", "sell"], loc="upper left", fontsize=12 )
        plt.show()


# lancer le backtest
backtest = BacktestCrossMA()
backtest.load_data("APPL_1D.csv")
backtest.populate_indicators()
backtest.populate_signals()
backtest.run_backtest()
backtest.plot()