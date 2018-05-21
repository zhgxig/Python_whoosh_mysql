# -*- coding:utf-8 -*-
import os
import time
import pymongo
from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME, NUMERIC
from jieba.analyse import ChineseAnalyzer
from whoosh.index import create_in, open_dir
from bson.objectid import ObjectId
import jieba
# jieba.load_userdict("dict.txt")
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh import scoring, sorting
from datetime import datetime
from collections import Counter
analyzer = ChineseAnalyzer()


schema = Schema(
            id=ID(unique=True, stored=True),
            content=TEXT(stored=False, analyzer=analyzer),
            info=TEXT(stored=False, analyzer=analyzer),
            score=TEXT(stored=False),
            title=TEXT(stored=False, analyzer=analyzer)
        )

client = pymongo.MongoClient("localhost:27017")
db = client['DouBan']
collections = db['dou_ban_movie']

if not os.path.exists('./index/'):
    os.mkdir("./index/")
    create_in("./index/", schema)

ix = open_dir("./index/")

# # 追加排序
# with ix.writer() as w:
#     sorting.add_sortable(w, "score", sorting.FieldFacet("score"))


for one in collections.find({}):
    with ix.writer() as writer:
        writer.update_document(
            id=one['_id'].__str__(),
            content=one['content'],
            info=one['info'],
            score=one["score"],
            title=one['title']
        )

start = time.time()
with ix.searcher(weighting=scoring.BM25F()) as searcher:
    query = MultifieldParser(["content", "info", "score", "title"], ix.schema).parse("中国")
    # query = QueryParser("content", ix.schema).parse("xss")

    mf = sorting.MultiFacet()
    mf.add_field("score", reverse=True)

    results = searcher.search(query, limit=10, sortedby=mf)
    # results = searcher.search_page(query, 2, pagelen=10)

    for one in results:
        # print(one['content'])
        # print(one.highlights("content"))
        _id = ObjectId(one['id'])
        res = collections.find({'_id': _id})[0]
        print(res)
    # keywords = [keyword for keyword, score in results.key_terms("content", docs=10, numterms=5)]
    # print(keywords)
end = time.time()
print(end - start)





