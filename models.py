from peewee import *
import json
import wiki as wikiapi
import yahoo as yfapi

DB_NAME = 'default.db'
db = SqliteDatabase(DB_NAME)

class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


class Stock(BaseModel):
    code = CharField()
    name = CharField()
    sector = CharField()
    industry = CharField()
    country = CharField()
    phone = CharField()
    website = CharField()
    summary = TextField()

    def __str__(self):
        return self.name


class WikiRecord(BaseModel):
    title = CharField()
    summary = TextField()
    url = CharField()

    def __str__(self):
        return f'{self.title}'


def init_db():
    db.connect()
    db.create_tables([Stock, WikiRecord])
    db.close()


def close_db(e=None):
    db.close()


# binding flask with peewee
def init_app(app):
    app.teardown_appcontext(close_db)


def init_stock_from_response(response):
    if response is None:
        print("[*]Error none stock")
        return None

    info = yfapi.yahoo_get_stock_info(response)
    stock_obj = Stock.create(
        code=info['code'],
        name=info['name'],
        sector=info['sector'],
        country=info['country'],
        phone=info['phone'],
        website=info['website'],
        summary=info['summary'],
        industry=info['industry'],
    )

    return stock_obj


def init_record_from_response(response):
    if response is None:
        print("[*]Error none response")
        return None

    wiki_info = wikiapi.wiki_get_summary(response)
    record_obj = WikiRecord.create(
        title=wiki_info['title'],
        summary=wiki_info['summary'],
        url=wiki_info['url'],
    )

    return record_obj


if __name__ == "__main__":
    # run only once to create tables
    init_db()
    wikiapi.init_cache()
    yfapi.init_cache()

    wiki_res = wikiapi.wiki_request_page('Apple_Inc.')
    wiki_test = init_record_from_response(wiki_res)
    wiki_test.save()
    print(wiki_test)

    aapl = yfapi.yahoo_request_stock('AAPL')
    print(aapl)
    stock_test = init_stock_from_response(aapl)
    stock_test.save()
    print(stock_test)
