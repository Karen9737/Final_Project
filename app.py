
# Presentation: app

from flask import Flask, render_template, request
import wiki as wikiapi
import yahoo as yfapi
import models
from data import earning_line, holders_pie
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stock', methods=['GET'])
def stock_get():
    return render_template('stock_index.html')


@app.route('/stock', methods=['POST'])
def stock_post():
    ticker_code = request.form['ticker']
    stock_res = yfapi.yahoo_request_stock(ticker_code)

    if stock_res is None:
        return render_template('404.html')

    # process text info
    stock_info = yfapi.yahoo_get_stock_info(stock_res)
    if len(stock_info['summary']) > 100:
        stock_info['summary'] = stock_info['summary'][:500] + '...'

    # other financial info
    stock_news = yfapi.yahoo_get_stock_news(stock_res)
    stock_est = yfapi.yahoo_get_stock_estimates(stock_res)
    stock_holders = yfapi.yahoo_get_stock_holders(stock_res)
    quar_data = yfapi.yahoo_get_stock_quarterly_data(stock_res)
    stock_earning = quar_data['earning']

    # prepare echarts data
    pie_data = holders_pie(stock_holders)
    line_data = earning_line(stock_earning)

    # render
    return render_template(
        'stock.html',
        stock_info=stock_info,
        stock_est=stock_est,
        news=stock_news,
        pie_data=pie_data,
        line_data=line_data
    )


@app.route('/wiki', methods=['GET'])
def wiki_get():
    return render_template('wiki_index.html')


@app.route('/wiki', methods=['POST'])
def wiki_post():
    wiki_word = request.form['wiki']
    wiki_res = wikiapi.wiki_request_page(wiki_word)

    if wiki_res is None:
        return render_template('404.html')

    wiki_info = wikiapi.wiki_get_summary(wiki_res)

    # split to paragraphs
    summary = wiki_info['summary']
    summary_p = summary.split('\n')
    wiki_info['summary'] = [p for p in summary_p if len(p) > 0]

    # get sections
    wiki_secs = wikiapi.wiki_get_sections(wiki_res)

    return render_template('wiki.html', wiki_info=wiki_info, sections=wiki_secs)


@app.route('/kline', methods=['GET'])
def kline_get():
    return render_template('kline_index.html')


@app.route('/kline', methods=['POST'])
def kline_post():
    ticker = request.form['ticker']
    max_hist = yfapi.yahoo_request_hist(ticker)

    if max_hist is None:
        render_template('404.html')

    hist_dates = max_hist.index.to_numpy().tolist()
    opens = max_hist['Open'].values.tolist()
    closes = max_hist['Close'].values.tolist()
    highs = max_hist['High'].values.tolist()
    lows = max_hist['Low'].values.tolist()

    kline_data = [
        [
            hist_dates[i].strftime('%Y/%m/%d'),
            opens[i], closes[i], highs[i], lows[i]]
        for i in range(len(hist_dates))
    ]

    return render_template(
        'kline.html',
        ticker=ticker,
        kline_data=kline_data
    )


if __name__ == "__main__":
    wikiapi.init_cache()
    yfapi.init_cache()
    models.init_app(app)
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    app.run(host='127.0.0.1', debug=True)
