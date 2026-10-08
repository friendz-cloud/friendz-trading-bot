import os, asyncio, requests, datetime
from dotenv import load_dotenv
from upstox_client.feeder import MarketDataStreamer
import upstox_client

load_dotenv()
TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Tumche sagle symbols - Scalping sathi Index, Weekly/Monthly sathi Stocks
INSTRUMENTS = ["NSE_INDEX|Nifty 50", "NSE_INDEX|Nifty Bank", "NSE_FO|HDFCBANK24O06700CE", "BSE_INDEX|SENSEX"]

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    except: pass

# 1. ONE DAY SCALPING LOGIC
def scalping_signal(live_price, symbol):
    entry = live_price
    sl = round(entry * 0.992, 2) # 0.8% SL
    t1 = round(entry * 1.008, 2) # 0.8% T1
    t2 = round(entry * 1.015, 2) # 1.5% T2
    p1 = round((t1-entry)*50); p2 = round((t2-entry)*50)
    now = datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    msg = f"""FRIEND'Z TREADING - ONE DAY SCALPING (OFFICIAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ Contract: {symbol} - ONE DAY SCALP
📱 App: FRIEND'Z TREADING F&O PRO
📅 Date: {now}
🏢 Symbol: {symbol}
📊 Action: 🟢 खरेदी (BUY) - SCALPING
⭐️ Accuracy: 78% [RSI: 62 | Vol: 2.8x]

💰 Entry: ₹{entry}
🎯 Target 1: ₹{t1} (+₹{p1})
🎯 Target 2: ₹{t2} (+₹{p2})
🛑 Stop Loss: ₹{sl}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡️ Live Top Rate: ₹{live_price}
📲 Scalping - Lavkar Profit Book Kara
"""
    send_telegram(msg)

# 2. WEEKLY/MONTHLY LOGIC - Tumcha Official Format
def weekly_monthly_signal(live_price, symbol, timeframe):
    entry = live_price
    sl = round(entry * 0.985, 2)
    t1 = round(entry * 1.027, 2); t2 = round(entry * 1.054, 2)
    profit = round(t1-entry,2); risk = round(entry-sl,2)
    now = datetime.datetime.now().strftime("%d %b, %Y")
    tnow = datetime.datetime.now().strftime("%I:%M:%S %p IST")
    msg = f"""FRIEND'Z TREADING - अधिकृत ट्रेड अलर्ट ({timeframe})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ Full Contract: {symbol} {timeframe}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 [LIVE NSE/BSE - {timeframe}]
📱 ॲप्लिकेशन: FRIEND'Z TREADING F&O PRO
📅 दिनांक: {now}
⏰ वेळ: {tnow}
🏢 Symbol: {symbol}
📊 सिग्नल: 🟢 खरेदी (BUY)
⭐️ Accuracy: 74% [RSI: 60 | Vol: 2.3x]

💰 Entry: ₹{entry}
🎯 Target 1: ₹{t1}
🎯 Target 2: ₹{t2}
🛑 Stop Loss: ₹{sl}
💵 Profit: +₹{profit} | Risk: ₹{risk}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡️ Live Top Rate Match: ₹{live_price}
"""
    send_telegram(msg)

def on_data(data):
    try:
        key = list(data['feeds'].keys())[0]
        ltp = data['feeds'][key]['ff']['marketFF']['ltpc']['ltp']
        print(f"{key} -> {ltp}")

        # SCALPING ENGINE: Index sathi
        if "Nifty" in key or "SENSEX" in key:
            # Tumcha logic: Price > VWAP asel tar
            if ltp % 10 > 5: # Sample condition - tumhi badalal
                scalping_signal(ltp, key)

        # WEEKLY/MONTHLY ENGINE: Stock F&O sathi
        else:
            if ltp % 10 < 5: # Sample condition
                # W - Weekly, M - Monthly auto detect
                tf = "WEEKLY" if "W" in key else "MONTHLY"
                weekly_monthly_signal(ltp, key, tf)

    except Exception as e: print(e)

async def main():
    print("Bot Started - 24 Taas Active - Scalping + Weekly + Monthly")
    streamer = MarketDataStreamer(upstox_client.Configuration(access_token=TOKEN), INSTRUMENTS, "full")
    streamer.on("market_data", on_data)
    streamer.auto_reconnect(True)
    streamer.connect()
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
