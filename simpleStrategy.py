import ccxt
import pandas as pd
import pandas_ta as ta
import numpy
numpy.NaN = numpy.nan  
from config import TIMEFRAMES

exchange = ccxt.coinbase({
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'}
})

def fetchData(symbol, timeframe, limit=100): 
    # Using coinbase since it is accessible
    # Using options trading data
    exchange = ccxt.coinbase({
        'enableRateLimit': True,
        'options': {'defaultType': 'swap'}
    })

    finalTimeframe = timeframe
    if(timeframe == TIMEFRAMES["4h"]):
        finalTimeframe = TIMEFRAMES["1h"]

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=finalTimeframe, limit=limit)

    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    if(timeframe == TIMEFRAMES["4h"]):
        # Resample to 4H candles
        df['open'] = df['open'].resample('4h').first()
        df['high'] = df['high'].resample('4h').max()
        df['low'] = df['low'].resample('4h').min()
        df['close'] = df['close'].resample('4h').last()
        df['volume'] = df['volume'].resample('4h').sum()
        df.dropna(inplace=True)  

    return df

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
    
# df = fetchData("ETH/USDT", "1h")
# result = strategy(df, "ETH/USDT")
# print(result)
# print(strategyPrinter(result))
