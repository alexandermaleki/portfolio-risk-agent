TICKER_DESCRIPTION = (
    "Yahoo Finance ticker. Stockholm-listed shares use a "
    ".ST suffix, e.g. INVE-B.ST for Investor B."
)

DATE_PARAMS = {
    "start": {
        "type": "string",
        "description": "Start date in YYYY-MM-DD format.",
    },
    "end": {
        "type": "string",
        "description": "End date in YYYY-MM-DD format.",
    },
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_volatility",
            "description": (
                "Calculate the annualised volatility of a stock over a date range. "
                "Volatility measures how much daily returns fluctuate and is a "
                "standard measure of risk. Returns a decimal, e.g. 0.21 means 21%."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": TICKER_DESCRIPTION},
                    **DATE_PARAMS,
                },
                "required": ["ticker", "start", "end"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_max_drawdown",
            "description": (
                "Calculate the maximum drawdown of a stock over a date range: the "
                "largest fall from a previous peak to a later low. Returns a "
                "negative decimal, e.g. -0.25 means the price fell 25% from its high."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": TICKER_DESCRIPTION},
                    **DATE_PARAMS,
                },
                "required": ["ticker", "start", "end"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_correlation",
            "description": (
                "Calculate the correlation of daily returns between two stocks over "
                "a date range. Returns a value between -1 and 1: 1 means they move "
                "together perfectly, 0 means no relationship, -1 means opposite."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker_a": {"type": "string", "description": TICKER_DESCRIPTION},
                    "ticker_b": {"type": "string", "description": TICKER_DESCRIPTION},
                    **DATE_PARAMS,
                },
                "required": ["ticker_a", "ticker_b", "start", "end"],
            },
        },
    },
]
