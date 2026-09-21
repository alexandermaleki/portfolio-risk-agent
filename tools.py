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

def get_volatility(ticker, start, end):
    """Agent-facing: annualised volatility for one ticker over a period."""
    prices = fetch_prices(ticker, start, end)
    returns = daily_returns(prices)
    return round(float(annualised_volatility(returns)), 4)

def get_max_drawdown(ticker, start, end):
    """Agent-facing: worst peak-to-trough fall for one ticker over a period."""
    prices = fetch_prices(ticker, start, end)
    return round(float(max_drawdown(prices)), 4)


def get_correlation(ticker_a, ticker_b, start, end):
    """Agent-facing: correlation of daily returns between two tickers."""
    returns_a = daily_returns(fetch_prices(ticker_a, start, end))
    returns_b = daily_returns(fetch_prices(ticker_b, start, end))
    return round(float(correlation(returns_a, returns_b)), 4)

if __name__ == "__main__":
    print(get_volatility("INVE-B.ST", "2024-01-01", "2024-12-31"))
    print(get_max_drawdown("INVE-B.ST", "2024-01-01", "2024-12-31"))
    print(get_correlation("INVE-B.ST", "VOLV-B.ST", "2024-01-01", "2024-12-31"))
