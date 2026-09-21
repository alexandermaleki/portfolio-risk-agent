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

def annualised_volatility(returns):
    """Standard deviation of daily returns, scaled to a yearly figure.

    Uses 252 trading days per year.
    """
    return returns.std() * (252 ** 0.5)

def max_drawdown(prices):
    """Largest peak-to-trough fall over the period, as a negative fraction.

    -0.25 means that at the worst point the price was 25% below its
    previous high.
    """
    running_peak = prices.cummax()
    drawdown = prices / running_peak - 1
    return drawdown.min()

def correlation(returns_a, returns_b):
    """Correlation of two return series, aligned by date.

    1 means they move together perfectly, 0 means no relationship,
    -1 means they move in opposite directions.
    """
    return returns_a.corr(returns_b)

if __name__ == "__main__":
    inve = fetch_prices("INVE-B.ST", "2024-01-01", "2024-12-31")
    volv = fetch_prices("VOLV-B.ST", "2024-01-01", "2024-12-31")

    inve_r = daily_returns(inve)
    volv_r = daily_returns(volv)

    print(f"Investor volatility: {annualised_volatility(inve_r):.4f}")
    print(f"Investor drawdown:   {max_drawdown(inve):.4f}")
    print(f"Volvo volatility:    {annualised_volatility(volv_r):.4f}")
    print(f"Volvo drawdown:      {max_drawdown(volv):.4f}")
    print(f"Correlation:         {correlation(inve_r, volv_r):.4f}")
