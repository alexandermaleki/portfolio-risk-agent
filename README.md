# Portfolio Risk Agent

An LLM agent that answers portfolio risk questions by calling Python tools on real market data. Built from scratch using the OpenAI API, without an agent framework.

## How it works

The model does not perform the risk calculations itself. It receives a question along with a list of available tools and decides whether to call a tool or return a final answer.

When a tool is requested, the agent executes it locally, sends the result back to the model, and repeats the process until a final answer is produced. A step limit prevents endless loops.

Available tools:

* Volatility
* Maximum drawdown
* Correlation

The underlying calculations are unit tested against inputs with known expected results.

## Observations

* Made two tool calls in a single step when comparing two stocks.
* Correctly interpreted "last year" and inferred tickers from company names.
* Refused to provide a P/E ratio when no tool was available to calculate or retrieve it, rather than making one up.
* Explained an invalid ticker error instead of repeatedly retrying the same request.
* Still performed simple arithmetic itself despite being instructed not to. The result was correct in the tested case, but this shows that the constraint is not strictly enforced.

## Limitations

* Market data is retrieved from yfinance, an unofficial source with no accuracy guarantees.
* The agent has no memory between questions.
* The observations are based on a small number of manual runs rather than a systematic evaluation.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your `OPENAI_API_KEY` to a `.env` file, then run:

```bash
python main.py
```

Run the tests with:

```bash
pytest
```
