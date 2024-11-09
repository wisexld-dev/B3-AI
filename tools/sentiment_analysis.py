# sentiment_analysis.py

import requests
from config import ALPHA_VANTAGE_API_KEY, TWELVE_DATA_API_KEY

# Funções da Alpha Vantage para RSI e EMA
def get_rsi(symbol: str, interval: str = 'daily', time_period: int = 14):
    url = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: RSI' not in data:
        print(f"Erro: Resposta da API RSI inesperada: {data}")
    return data.get('Technical Analysis: RSI', {})

def get_ema(symbol: str, interval: str = 'daily', time_period: int = 20):
    url = f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: EMA' not in data:
        print(f"Erro: Resposta da API EMA inesperada: {data}")
    return data.get('Technical Analysis: EMA', {})

# Função da Twelve Data para MACD
def get_macd_twelve_data(symbol: str, interval: str = '1day'):
    url = f'https://api.twelvedata.com/macd'
    params = {
        'symbol': symbol,
        'interval': interval,
        'apikey': TWELVE_DATA_API_KEY,
        'series_type': 'close'
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'values' not in data:
        print(f"Erro: Resposta inesperada da API Twelve Data: {data}")
        return None
    
    macd_data = data['values']
    return macd_data

# Função para calcular o sentimento do mercado usando ambas as APIs
def calculate_market_sentiment(symbol: str, interval: str = 'daily'):
    # Coletar dados de RSI e EMA usando Alpha Vantage
    rsi_data = get_rsi(symbol, interval)
    ema_data = get_ema(symbol, interval)
    
    # Coletar dados de MACD usando Twelve Data
    macd_data = get_macd_twelve_data(symbol, '1day')
    
    # Verificar se todos os dados foram obtidos
    if not rsi_data or not ema_data or not macd_data:
        print("Erro: Dados insuficientes para calcular o sentimento de mercado.")
        return "Erro: Dados insuficientes"

    # Obter os valores mais recentes de cada indicador
    try:
        latest_rsi = float(list(rsi_data.values())[0]['RSI'])
        latest_ema = float(list(ema_data.values())[0]['EMA'])
        latest_macd = float(macd_data[0]['macd'])
        latest_signal = float(macd_data[0]['macd_signal'])
    except (IndexError, KeyError) as e:
        print(f"Erro ao acessar dados do indicador: {e}")
        return "Erro: Dados incompletos"

    # Análise de Sentimento do Mercado combinando os três indicadores
    if latest_rsi > 70 and latest_macd > latest_signal:
        sentiment = "alta-alta"  # Forte tendência de alta
    elif latest_rsi > 70:
        sentiment = "alta"       # Tendência de alta
    elif latest_rsi < 30 and latest_macd < latest_signal:
        sentiment = "baixa-baixa"  # Forte tendência de baixa
    elif latest_rsi < 30:
        sentiment = "baixa"        # Tendência de baixa
    elif 30 < latest_rsi < 70 and latest_macd > latest_signal:
        sentiment = "alta-baixa"  # Reversão para alta
    elif 30 < latest_rsi < 70 and latest_macd < latest_signal:
        sentiment = "baixa-alta"  # Reversão para baixa
    else:
        sentiment = "neutro"       # Nenhuma tendência clara

    return sentiment
