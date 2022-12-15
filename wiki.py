import wikipediaapi
import os
import json
from api_conf import WIKI_CACHE
import requests

# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"
wiki_cache = {}


def wiki_save_cache(cache: dict):
    cache_json = json.dumps(cache, indent=4, ensure_ascii=False)
    with open(WIKI_CACHE, 'w', encoding='utf-8') as f:
        f.write(cache_json)


def wiki_load_cache():
    with open(WIKI_CACHE, 'r', encoding='utf-8') as f:
        cache_json = f.read()
    return json.loads(cache_json)


def init_cache():
    global wiki_cache
    if os.path.exists(WIKI_CACHE):
        wiki_cache = wiki_load_cache()
    else:
        wiki_cache = {}


def is_in_cache(cache, wiki_name: str):
    if wiki_name in cache:
        return True
    else:
        return False


def wiki_request_page_no_cached(wiki_name: str):
    print("[*]No Cache wiki : {}".format(wiki_name))
    wiki_wiki = wikipediaapi.Wikipedia('en')
    wiki_page = wiki_wiki.page(wiki_name)
    if not wiki_page.exists():
        print("[*]No Wiki Page : {}".format(wiki_name))
        return None

    ret = {
        'title': wiki_page.title,
        'summary': wiki_page.summary,
        'url': wiki_page.fullurl,
        'sections': [s.title for s in wiki_page.sections],
        'fulltext': wiki_page.text
    }

    return ret


def wiki_request_page(wiki_name: str):
    global wiki_cache
    if is_in_cache(wiki_cache, wiki_name):
        print("[*]Cache Hit: {}".format(wiki_name))
        return wiki_cache[wiki_name]
    else:
        wiki_page = wiki_request_page_no_cached(wiki_name)
        if wiki_page is not None:
            wiki_cache[wiki_name] = wiki_page
            wiki_save_cache(wiki_cache)
        return wiki_page


def wiki_get_summary(wiki_response):
    if wiki_response is None:
        return None

    ret = {
        'title': wiki_response['title'],
        'summary': wiki_response['summary'],
        'url': wiki_response['url'],
    }

    return ret


def wiki_get_sections(wiki_response):
    if wiki_response is None:
        return None

    return wiki_response['sections']


def wiki_get_fulltext(wiki_response):
    if wiki_response is None:
        return None

    return wiki_response['fulltext']


def wiki_scrap_category_pages(category_members, level=0, max_level=0):
    def _scrap_category_pages(category_members, acc_lst, level, max_level):
        for c in category_members.values():
            acc_lst.append(c.title)
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                return _scrap_category_pages(c.categorymembers, acc_lst, level=level + 1, max_level=max_level)

    ret = []
    _scrap_category_pages(category_members, ret, level, max_level)
    ret.sort()

    return ret


# run once to generate cache
def wiki_run_once_gen_cache():
    wiki_wiki = wikipediaapi.Wikipedia('en')
    category = wiki_wiki.page("Category:Finance")

    # get wiki summary
    pages = wiki_scrap_category_pages(category.categorymembers)
    wiki_data = {}
    for page in pages:
        wiki_response = wiki_request_page(page)
        wiki_data[page] = wiki_get_summary(wiki_response)

    print(wiki_data)
    wiki_save_cache(wiki_cache)


# if __name__ == "__main__":
     # init_cache()
     # wiki_run_once_gen_cache()

