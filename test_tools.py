import pandas as pd
import pytest

from tools import daily_returns, annualised_volatility, max_drawdown, correlation

def test_daily_returns_simple():
    prices = pd.Series([100.0, 110.0, 99.0])

    result = daily_returns(prices)

    assert len(result) == 2
    assert result.iloc[0] == pytest.approx(0.10)
    assert result.iloc[1] == pytest.approx(-0.10)

def test_volatility_of_constant_returns_is_zero():
    returns = pd.Series([0.01, 0.01, 0.01, 0.01])

    assert annualised_volatility(returns) == pytest.approx(0.0)

def test_max_drawdown_simple():
    prices = pd.Series([100.0, 120.0, 90.0, 110.0])

    assert max_drawdown(prices) == pytest.approx(-0.25)

def test_max_drawdown_rising_prices_is_zero():
    prices = pd.Series([100.0, 105.0, 110.0, 120.0])

    assert max_drawdown(prices) == pytest.approx(0.0)

def test_correlation_with_itself_is_one():
    returns = pd.Series([0.01, -0.02, 0.03, -0.01])

    assert correlation(returns, returns) == pytest.approx(1.0)

def test_correlation_with_opposite_is_minus_one():
    returns = pd.Series([0.01, -0.02, 0.03, -0.01])

    assert correlation(returns, -returns) == pytest.approx(-1.0)
