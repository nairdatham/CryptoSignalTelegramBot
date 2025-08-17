import pandas_ta  as ta
import pandas as pd
import numpy
numpy.NaN = numpy.nan  

def analyze_market_structure(df):
    # Select last few candles for structure analysis
    recent_highs = df['high'].tail(4).values
    recent_lows = df['low'].tail(4).values

    bullish = all(recent_highs[i] > recent_highs[i - 1] and recent_lows[i] > recent_lows[i - 1]
                  for i in range(1, len(recent_highs)))
    bearish = all(recent_highs[i] < recent_highs[i - 1] and recent_lows[i] < recent_lows[i - 1]
                  for i in range(1, len(recent_highs)))

    sidewayStructure = not bullish and not bearish

    if bullish:
        return "BULLISH structure 🟢"
    elif bearish:
        return "BEARISH structure 🔴"
    elif sidewayStructure:
        return "Choppy sideways price action 🟡"

def analyze_structure_enhanced(df):
    # Calculate EMA 10 and EMA 20
    df['ema10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()

    # Structure analysis: Last 4 candles for HH/HL or LH/LL
    recent_highs = df['high'].tail(4).values
    recent_lows = df['low'].tail(4).values

    bullish_structure = all(recent_highs[i] > recent_highs[i - 1] and recent_lows[i] > recent_lows[i - 1]
                            for i in range(1, len(recent_highs)))
    bearish_structure = all(recent_highs[i] < recent_highs[i - 1] and recent_lows[i] < recent_lows[i - 1]
                            for i in range(1, len(recent_highs)))

    sidewayStructure = not bullish_structure and not bearish_structure

    # EMA logic
    latest_close = df['close'].iloc[-1]
    latest_ema10 = df['ema10'].iloc[-1]
    latest_ema20 = df['ema20'].iloc[-1]

    # Conditions
    price_above_emas = latest_close > latest_ema10 and latest_close > latest_ema20
    ema10_above_ema20 = latest_ema10 > latest_ema20

    # Combine logic
    if bullish_structure and price_above_emas and ema10_above_ema20:
        return "BULLISH structure 🟢"
    elif bearish_structure and not price_above_emas and not ema10_above_ema20:
        return "BEARISH structure 🔴"
    elif sidewayStructure:
        return "Choppy sideways price action 🟡"


def analyze_market_structure_with_indicators(df):
    # Apply technical indicators
    df['ma20'] = ta.sma(df['close'], length=20)  # Simple Moving Average
    df['rsi'] = ta.rsi(df['close'], length=14)   # RSI as confirmation

    # Analyze highs/lows
    recent_highs = df['high'].tail(4).values
    recent_lows = df['low'].tail(4).values

    # Candlestick structure logic
    bullish_structure = all(
        recent_highs[i] > recent_highs[i - 1] and recent_lows[i] > recent_lows[i - 1]
        for i in range(1, len(recent_highs))
    )

    bearish_structure = all(
        recent_highs[i] < recent_highs[i - 1] and recent_lows[i] < recent_lows[i - 1]
        for i in range(1, len(recent_highs))
    )

    # Filter with moving average and RSI
    latest_close = df['close'].iloc[-1]
    latest_ma20 = df['ma20'].iloc[-1]
    latest_rsi = df['rsi'].iloc[-1]

    sidewayStructure = not bullish_structure and not bearish_structure

    if bullish_structure and latest_close > latest_ma20 and latest_rsi > 55:
        return "BULLISH structure 🟢"
    elif bearish_structure and latest_close < latest_ma20 and latest_rsi < 45:
        return "BEARISH structure 🔴"
    elif sidewayStructure:
        return "Choppy sideways price action 🟡"