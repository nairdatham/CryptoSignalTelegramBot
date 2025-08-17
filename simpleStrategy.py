import pandas_ta as ta
import numpy
numpy.NaN = numpy.nan  
from dataFetcher import fetchData

def strategy(df, symbol):
    df["symbol"] = symbol

    # Indicators
    df['ema20'] = ta.ema(df['close'], length=20)
    df['rsi'] = ta.rsi(df['close'], length=14)

    # Signals
    df['buy_signal'] = (df['close'] > df['ema20']) & (df['rsi'] > 55)
    df['sell_signal'] = (df['close'] < df['ema20']) & (df['rsi'] < 45)

    return df

def strategyPrinter(df):
    results = {}
    latest = df.iloc[-1]
    symbol = latest['symbol']
    result = ""

    if latest['buy_signal']:
        result =  f"📈 BUY signal for {symbol} at {latest.name} — Price: {latest['close']:.2f}, RSI: {latest['rsi']:.2f}"
    elif latest['sell_signal']:
        result =  f"📉 SELL signal for {symbol} at {latest.name} — Price: {latest['close']:.2f}, RSI: {latest['rsi']:.2f}"
    else:
        result = f"⏸️ No clear signal for {symbol} at {latest.name} — Price: {latest['close']:.2f}, RSI: {latest['rsi']:.2f}"

    results["result"] = result

    return results
