# CryptoSignalTelegramBot
A telegram bot that can be used to check for trading signals for cryptocurrency pairs in an centralised exchange

## Setup

1. Clone the repo
2. Create a `.env` file in the root directory
3. Add your Telegram bot token: `TELEGRAM_TOKEN="your_token_here"`
4. Run the bot

## Features
* Trend analysis on a crytocurrency symbol
* Buy/sell signal found using a simple **EMA 20** and **RSI** strategy
* Back test engine that back test the current strategy used and returns a buy/sell price chart and a summary stats of the strategy
