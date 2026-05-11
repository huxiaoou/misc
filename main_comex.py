import yfinance as yf
import time

def get_silver_price():
    # Fetch data for the nearest COMEX silver contract
    silver = yf.Ticker("SI=F")
    
    # Get the latest price (fast info is often more up-to-date)
    # Using .info for detailed data or .history for recent ticks
    live_price = silver.fast_info['last_price']
    print(f"COMEX Silver (SI=F) Real-Time Price: ${live_price:.2f}")

# Call the function
get_silver_price()
