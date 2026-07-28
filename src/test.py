import yfinance as yf

info = yf.Ticker("TTD").info

print(info["exchange"])
print(info["fullExchangeName"])