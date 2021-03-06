# -*- coding: utf-8 -*-

from ccxt.async.okcoinusd import okcoinusd


class allcoin (okcoinusd):

    def describe(self):
        return self.deep_extend(super(allcoin, self).describe(), {
            'id': 'allcoin',
            'name': 'Allcoin',
            'countries': 'CA',
            'hasCORS': False,
            'extension': '',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/31561809-c316b37c-b061-11e7-8d5a-b547b4d730eb.jpg',
                'api': {
                    'web': 'https://www.allcoin.com',
                    'public': 'https://api.allcoin.com/api',
                    'private': 'https://api.allcoin.com/api',
                },
                'www': 'https://www.allcoin.com',
                'doc': 'https://www.allcoin.com/About/APIReference',
            },
            'api': {
                'web': {
                    'get': [
                        'Home/MarketOverViewDetail/',
                    ],
                },
                'public': {
                    'get': [
                        'depth',
                        'kline',
                        'ticker',
                        'trades',
                    ],
                },
                'private': {
                    'post': [
                        'batch_trade',
                        'cancel_order',
                        'order_history',
                        'order_info',
                        'orders_info',
                        'repayment',
                        'trade',
                        'trade_history',
                        'userinfo',
                    ],
                },
            },
            'markets': None,
        })

    async def fetch_markets(self):
        result = []
        response = await self.webGetHomeMarketOverViewDetail()
        coins = response['marketCoins']
        for j in range(0, len(coins)):
            markets = coins[j]['Markets']
            for k in range(0, len(markets)):
                market = markets[k]['Market']
                base = market['Primary']
                quote = market['Secondary']
                id = base.lower() + '_' + quote.lower()
                symbol = base + '/' + quote
                result.append({
                    'id': id,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'type': 'spot',
                    'spot': True,
                    'future': False,
                    'info': market,
                })
        return result

    def parse_order_status(self, status):
        if status == -1:
            return 'canceled'
        if status == 0:
            return 'open'
        if status == 1:
            return 'open'  # partially filled
        if status == 2:
            return 'closed'
        if status == 10:
            return 'canceled'
        return status

    def get_create_date_field(self):
        # allcoin typo create_data instead of create_date
        return 'create_data'

    def get_orders_field(self):
        # allcoin typo order instead of orders(expected based on their API docs)
        return 'order'
