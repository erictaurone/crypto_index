import requests_html as rh
from pprint import pprint
from crypto.config import COINMARKETCAP_PRIVATE_KEY, CRYPTO_SYMBOLS

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


# %%
def extract_crypto_data(private_key: str):
    session = rh.HTMLSession()

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': private_key,
    }
    parameters = {
        'symbol': CRYPTO_SYMBOLS,
    }
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    return response.json()


# %%

data = extract_crypto_data(COINMARKETCAP_PRIVATE_KEY)
