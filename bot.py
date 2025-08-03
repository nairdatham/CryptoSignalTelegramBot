import telebot
from telebot import types
from config import TELEGRAM_TOKEN, COIN_LIST, TIMEFRAMES, INFORMATION
# from strategy import check_conditions
from trend import fetchData
from trend import analyze_market_structure

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_state = {}  # store user selections for inline flow

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
        "🤖 Welcome to the Crypto Signal Bot!\n\n"
        "Use:\n"
        "• /check COIN TIMEFRAME (e.g. /check BTC/USDT 1h)\n"
        "• /scanall – scan all coins and timeframes\n"
        "• Or use buttons below 👇",
        reply_markup=coin_buttons()
    )

# Inline button step 1: Coin selector
def coin_buttons():
    markup = types.InlineKeyboardMarkup()
    for coin in COIN_LIST:
        markup.add(types.InlineKeyboardButton(coin, callback_data=f"Coin:{coin}"))
    return markup

# Inline button step 2: Information selector
def information_buttons(coin):
    markup = types.InlineKeyboardMarkup()
    for info in INFORMATION:
        markup.add(types.InlineKeyboardButton(info, callback_data=f"Information:{coin}:{info}"))
    return markup

# Inline button step 3: Timeframe selector
def timeframe_buttons(coin, info):
    markup = types.InlineKeyboardMarkup()
    for tf in TIMEFRAMES:
        markup.add(types.InlineKeyboardButton(tf, callback_data=f"Timeframe:{coin}:{info}:{tf}"))
    return markup

# Handle button presses
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("Coin:"):
        coin = call.data.split(":")[1]
        user_state[call.from_user.id] = {"Coin": coin}
        bot.send_message(call.message.chat.id, f"📈 You selected {coin}\nNow choose a which information to check:",
                         reply_markup=information_buttons(coin))
    elif call.data.startswith("Information:"):
        coin = call.data.split(":")[1]
        info = call.data.split(":")[2]
        user_state[call.from_user.id] = {"Coin": coin, "Information": info}
        bot.send_message(call.message.chat.id, f"📈 You selected {coin}\n to check on its {info} Now choose a timeframe to check:",
                         reply_markup=timeframe_buttons(coin, info))
    elif call.data.startswith("Timeframe:"):
        _, coin, info, tf = call.data.split(":")
        bot.send_message(call.message.chat.id, f"⏳ Analyzing {coin} for {info} on {tf}...")
        try:
            df = fetchData(coin, tf)
            if(info == INFORMATION["Trend"]):
                msg = analyze_market_structure(df)
            elif (info == INFORMATION["Signal"]):
                # results = check_conditions(df, coin)
                # msg = f"🔔 Signal for {coin} on {tf}:\n"
                # for key, val in results.items():
                #     msg += f"• {key}: {val}\n"
                msg = "Signal feature is not available currently"
            bot.send_message(call.message.chat.id, msg)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error: {e}")

# /check command
@bot.message_handler(commands=['check'])
def handle_check(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "❌ Usage: /check COIN/USDT INFORMATION TIMEFRAME\nExample: /check BTC/USDT Trend 1h OR BTC/USDT Signal 1h")
            return

        symbol, info, timeframe = parts[1].upper(), parts[2].title(), parts[3].lower()

        if info not in INFORMATION:
            bot.reply_to(message, f"❌ Invalid information given. Use: {', '.join(INFORMATION)}")
            return

        if timeframe not in TIMEFRAMES:
            bot.reply_to(message, f"❌ Invalid timeframe. Use: {', '.join(TIMEFRAMES)}")
            return

        bot.send_message(message.chat.id, f"📊 Analyzing {symbol} for {info} on {timeframe}...")
        df = fetchData(symbol, timeframe)

        if(info == INFORMATION["Trend"]):
            msg = analyze_market_structure(df)
        elif (info == INFORMATION["Signal"]):
            # results = check_conditions(df, symbol)
            # msg = f"🔔 Signal for {symbol} on {timeframe}:\n"
            # for key, val in results.items():
            #     msg += f"• {key}: {val}\n"
            msg = "Signal feature is not available currently"

        bot.send_message(message.chat.id, msg)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

# /scanall command
@bot.message_handler(commands=['scanall'])
def handle_scan_all(message):
    final_message = []
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "❌ Usage: /scanall INFORMATION\nExample: /scanall Trend")
        return

    info = parts[1].title()

    if info not in INFORMATION:
        bot.reply_to(message, f"❌ Invalid information given. Use: {', '.join(INFORMATION)}")
        return
    
    bot.send_message(message.chat.id, f"🔍 Scanning all coins and timeframes for the specified information... This may take a while.")
    for coin in COIN_LIST:
        for tf in TIMEFRAMES:
            try:
                df = fetchData(coin, tf)
                if(info == INFORMATION["Trend"]):
                    msg = analyze_market_structure(df)
                    msg = f"{coin} {tf} {msg}"
                    final_message.append(msg)
                elif (info == INFORMATION["Signal"]):
                    # results = check_conditions(df, coin)
                    # msg = f"🔔 Signal for {coin} on {tf}:\n"
                    # for key, val in results.items():
                    #     msg += f"• {key}: {val}\n"
                    msg = "Signal feature is not available currently"
                    final_message.append(msg)
                # bot.send_message(message.chat.id, msg)
            except Exception as e:
                final_message.append(f"❌ Error with {coin} {info} {tf}: {e}")

    bot.send_message(message.chat.id, "\n".join(final_message))

print("Bot is running with inline buttons...")
bot.polling()
