from io import BytesIO
from simpleStrategy import strategy
from dataFetcher import fetchData
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt


# === Backtest Engine ===
def backtest_strategy(strategy_fn, tradeData, symbol):
    result = strategy_fn(tradeData, symbol)

    position = None
    trades = []

    for i in range(1, len(result)):
        row = result.iloc[i]
        if position is None and row['buy_signal']:
            position = 'long'
            trades.append({'type': 'buy', 'price': row['close'], 'time': row.name})
        elif position == 'long' and row['sell_signal']:
            trades.append({'type': 'sell', 'price': row['close'], 'time': row.name})
            position = None

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(tradeData.index, tradeData['close'], label='Close Price', color='blue')
    if 'ema20' in tradeData.columns:
        plt.plot(tradeData.index, tradeData['ema20'], label='EMA20', color='orange', linestyle='--')

    for trade in trades:
        color = 'green' if trade['type'] == 'buy' else 'red'
        marker = '^' if trade['type'] == 'buy' else 'v'
        plt.plot(trade['time'], trade['price'], marker=marker, color=color, markersize=10)

    plt.title(f'{symbol} Strategy Backtest')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Performance Summary
    profits = []
    for i in range(0, len(trades) - 1, 2):
        buy = trades[i]
        sell = trades[i + 1]
        profits.append(sell['price'] - buy['price'])

    total_return = sum(profits)
    win_trades = len([p for p in profits if p > 0])
    total_trades = len(profits)
    win_rate = (win_trades / total_trades) * 100 if total_trades > 0 else 0

    summary = {
        'Total Trades': total_trades,
        'Winning Trades': win_trades,
        'Win Rate (%)': round(win_rate, 2),
        'Total Return ($)': round(total_return, 2),
        'Last Signal': 'BUY' if tradeData.iloc[-1].get('buy_signal') else 'SELL' if tradeData.iloc[-1].get('sell_signal') else 'HOLD'
    }

    return (summary, buf)