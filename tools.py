import yfinance as yf


def fetch_prices(ticker, start, end):
    """Fetch daily closing prices for one ticker.

    Returns a pandas Series indexed by date.
    """
    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        raise ValueError(f"No data returned for {ticker} between {start} and {end}")

    close = data["Close"]

    
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    return close


if __name__ == "__main__":
    prices = fetch_prices("INVE-B.ST", "2024-01-01", "2024-12-31")
    print(prices.head())
    print(prices.tail())
    print(f"\nRows: {len(prices)}")
