import ccxt
import pandas as pd
import numpy
numpy.NaN = numpy.nan  
from config import TIMEFRAMES

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