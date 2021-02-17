from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


API_KEY = '374572dd-4a56-4981-a078-0b5c57ec2c5e'
api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': API_KEY,}


class Get_info:

    def __init__(self, symbol, convert='USD'):
        self.symbol = symbol
        self.convert = convert


    def get_filtered_data(self):
        parameters = {
            'symbol': self.symbol,
            'convert': self.convert
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(api_url, params=parameters)
            data = json.loads(response.text)
            price = data['data'][self.symbol]['quote'][self.convert]['price']
            cap = data['data'][self.symbol]['quote'][self.convert]['market_cap']
            percent_change_24h = data['data'][self.symbol]['quote'][self.convert]['percent_change_24h']
            percent_change_7d = data['data'][self.symbol]['quote'][self.convert]['percent_change_7d']
            percent_change_1h = data['data'][self.symbol]['quote'][self.convert]['percent_change_1h']
            return price
            # print('The market cap is', cap, self.convert)
            # print('The 1 hour change is', percent_change_1h, self.convert)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


grt = Get_info('DGB','BTC')
print(grt.get_filtered_data())
