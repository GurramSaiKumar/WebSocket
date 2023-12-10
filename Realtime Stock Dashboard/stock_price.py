import requests
from django.http import JsonResponse
from constants import API_KEY
from rest_framework import status

api_key = API_KEY


def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        if 'Global Quote' in data:
            stock_price = data['Global Quote']['05. price']
            return stock_price
    return JsonResponse({f'Cannot fetch stock price for {symbol}'}, status=status.HTTP_400_BAD_REQUEST)
