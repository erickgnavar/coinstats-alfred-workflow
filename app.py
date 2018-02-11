import json
import locale
import sys
import urllib2

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())


CURRENCY_SYMBOL = locale.localeconv()['int_curr_symbol'].lower().strip() or 'usd'


def make_response():
    url = 'https://api.coinmarketcap.com/v1/ticker/?convert={}'.format(CURRENCY_SYMBOL)
    try:
        response = urllib2.urlopen(url).read()
        data = json.loads(response)
        return sorted(data, key=lambda x: int(x['rank']))
    except Exception:
        return []


def make_item(coin):
    price_key = 'price_{}'.format(CURRENCY_SYMBOL)
    market_cap_key = 'market_cap_{}'.format(CURRENCY_SYMBOL)
    coin['price'] = locale.currency(float(coin[price_key]), grouping=True)
    coin['market_cap'] = locale.currency(float(coin[market_cap_key]), grouping=True)
    return {
        'uid': coin['rank'],
        'title': '{} - {} - {}'.format(coin['name'], coin['symbol'], coin['price']),
        'subtitle': 'Market cap: {}'.format(coin['market_cap']),
        'type': 'default',
        'icon': {
            'path': './icons/{}.png'.format(coin['symbol'].lower())
        },
        'arg': coin['id']
    }


def filter_data(data, query):
    def fun(x):
        q = query.lower()
        name = x['name'].lower()
        symbol = x['symbol'].lower()
        return q in name or q in symbol
    return list(filter(fun, data))


def output(data):
    return {
        'items': list(map(make_item, data))
    }


data = make_response()

query = sys.argv[1]

sys.stdout.write(json.dumps(output(filter_data(data, query))))
