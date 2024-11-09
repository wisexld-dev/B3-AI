# market_data.py

import requests
from config import ALPHA_VANTAGE_API_KEY

## DADOS DE PREÇO & HISTORICO!
def get_historical_data(symbol: str, interval: str = '1min', output_size: str = 'compact'):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data.get(f'Time Series ({interval})', {})


## RSI
def get_rsi(symbol: str, interval: str = 'daily', time_period: int = 14):
    url = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data.get('Technical Analysis: RSI', {})



## EMA
def get_ema(symbol: str, interval: str = 'daily', time_period: int = 20):
    url = f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data.get('Technical Analysis: EMA', {})
