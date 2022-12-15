import os
import yfinance as yf
from api_conf import YAHOO_CACHE, YAHOO_TICKERS
import json
import pandas as pd
import requests
from yahoo_oauth import OAuth2

# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"
yahoo_cache = {}

from yahoo_oauth import OAuth2
oauth = OAuth2(None, None, from_file='oauth2.json')

def yahoo_load_cache():
    with open(YAHOO_CACHE, 'r', encoding='utf-8') as f:
        cache_json = f.read()
    return json.loads(cache_json)


def yahoo_save_cache(cache):
    cache_json = json.dumps(cache, indent=4, ensure_ascii=False)
    with open(YAHOO_CACHE, 'w', encoding='utf-8') as f:
        f.write(cache_json)


def init_cache():
    global yahoo_cache
    if os.path.exists(YAHOO_CACHE):
        yahoo_cache = yahoo_load_cache()
    else:
        yahoo_cache = {}


def is_in_cache(cache, ticker: str):
    if ticker in cache:
        return True
    else:
        return False


def wrap_pd(stock_attr):
    if stock_attr is None:
        return None
    else:
        return stock_attr.to_json()


# no cache version
def yahoo_request_hist(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period="max")

    except Exception as e:
        print("[*]Error: {}".format(e))
        ret = None

    return ret


def yahoo_request_stock_no_cached(ticker: str):
    print("[*]No Cache: {}".format(ticker))
    try:
        stock = yf.Ticker(ticker)
        ret = {
            'code': stock.ticker,
            'info': stock.info,
            'news': stock.news,
            'holders': wrap_pd(stock.institutional_holders),
            'shares': wrap_pd(stock.shares),
            'quar_balance': wrap_pd(stock.quarterly_balancesheet),
            'quar_cashflow': wrap_pd(stock.quarterly_cashflow),
            'quar_financial': wrap_pd(stock.quarterly_financials),
            'quar_earning': wrap_pd(stock.quarterly_earnings),
        }
    except Exception as e:
        print("[*]Error: {}".format(e))
        ret = None
    return ret


# estimate cache
def yahoo_request_stock(ticker: str):
    global yahoo_cache
    if is_in_cache(yahoo_cache, ticker):
        print("[*]Cache Found : {}".format(ticker))
        return yahoo_cache[ticker]
    else:
        stock = yahoo_request_stock_no_cached(ticker)
        if stock is not None:
            print("try cache : {}".format(ticker))
            yahoo_cache[ticker] = stock
            # save to cache file
            yahoo_save_cache(yahoo_cache)

        return stock


def yahoo_get_stock_info(stock_response):
    if stock_response is None:
        return None

    ret = {
        'code': stock_response['code'],
        'name': stock_response['info']['longName'] if 'longName' in stock_response['info'] else "",
        'sector': stock_response['info']['sector'] if 'sector' in stock_response['info'] else "",
        'country': stock_response['info']['country'] if 'country' in stock_response['info'] else "",
        'phone': stock_response['info']['phone'] if 'phone' in stock_response['info'] else "",
        'website': stock_response['info']['website'] if 'website' in stock_response['info'] else "",
        'summary': stock_response['info']['longBusinessSummary'] if 'longBusinessSummary' in stock_response['info'] else "",
        'industry': stock_response['info']['industry'] if 'industry' in stock_response['info'] else "",
    }
    return ret


def yahoo_get_stock_estimates(stock_response):
    if stock_response is None:
        return None

    ret = {
        'current': stock_response['info']['currentPrice'] if 'currentPrice' in stock_response['info'] else "",
        'volume': stock_response['info']['volume'] if 'volume' in stock_response['info'] else "",

        'open': stock_response['info']['open'] if 'open' in stock_response['info'] else "",
        'prevClose': stock_response['info']['previousClose'] if 'previousClose' in stock_response['info'] else "",
        'peg': stock_response['info']['pegRatio'] if 'pegRatio' in stock_response['info'] else "",
    }
    return ret


def yahoo_get_stock_hist(stock_response):
    if stock_response is None:
        return None

    return pd_json_to_df(stock_response['history'])


def yahoo_get_stock_news(stock_response):
    if stock_response is None:
        return None

    return stock_response['news']


def pd_json_to_df(pd_json):
    ret_json = json.loads(pd_json)
    ret_df = pd.DataFrame.from_dict(ret_json)
    return ret_df


def yahoo_get_stock_holders(stock_response):
    if stock_response is None:
        return None

    return pd_json_to_df(stock_response['holders'])


def yahoo_get_stock_shares(stock_response):
    if stock_response is None:
        return None

    return pd_json_to_df(stock_response['shares'])


def yahoo_get_stock_quarterly_data(stock_response):
    if stock_response is None:
        return None

    ret = {
        'balance': pd_json_to_df(stock_response['quar_balance']),
        'cashflow': pd_json_to_df(stock_response['quar_cashflow']),
        'financial': pd_json_to_df(stock_response['quar_financial']),
        'earning': pd_json_to_df(stock_response['quar_earning'])
    }
    return ret


def yahoo_run_once_gen_cache():
    for ticker in YAHOO_TICKERS:
        response = yahoo_request_stock(ticker)


# if __name__ == "__main__":
    # init_cache()
    # yahoo_run_once_gen_cache()
    # msft_response = yahoo_request_stock("MSFT")
    # quar_data = yahoo_get_stock_quarterly_data(msft_response)