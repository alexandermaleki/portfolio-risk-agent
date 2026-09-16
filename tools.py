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

def daily_returns(prices):
    """Convert a price series into daily percentage returns.

    Drops the first row, which has no previous day to compare against.
    """
    return prices.pct_change().dropna()

if __name__ == "__main__":
    prices = fetch_prices("INVE-B.ST", "2024-01-01", "2024-12-31")
    returns = daily_returns(prices)

    print(returns.head())
    print(f"\nPrice rows:  {len(prices)}")
    print(f"Return rows: {len(returns)}")
    print(f"Mean daily return: {returns.mean():.5f}")
    print(f"Largest gain:      {returns.max():.4f}")
    print(f"Largest loss:      {returns.min():.4f}")
