import whoosh.index as index
from whoosh import columns, fields, index, sorting
from whoosh.qparser import QueryParser

# ix = index.open_dir("./")
# facet = sorting.FieldFacet("id", reverse=True)
# searcher = ix.searcher()
#
# searchwords = "新西兰"
# qp = QueryParser("gtitle", schema=ix.schema)
# q = qp.parse(searchwords)
# results = searcher.search(q, sortedby=facet)
# for each in results:
#     print(each)


from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh.sorting import FieldFacet

new_list = []
index = open_dir("./index/", indexname='goods')  # 读取建立好的索引
with index.searcher() as searcher:
    parser = QueryParser("gtitle", index.schema)  # 要搜索的项目，比如“phone_name
    myquery = parser.parse("鸭蛋")
    facet = FieldFacet("id", reverse=True)  # 按序排列搜索结果
    results = searcher.search(myquery, limit=None, sortedby=facet)  # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
    for result1 in results:
        print(dict(result1))
        new_list.append(dict(result1))