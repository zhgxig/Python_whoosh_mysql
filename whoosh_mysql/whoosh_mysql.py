from settings.db_setting import get_db, Goods
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT, NUMERIC, NGRAMWORDS
from whoosh.index import create_in
from jieba.analyse import ChineseAnalyzer

analyzer = ChineseAnalyzer()
db = get_db()
result = db.query(Goods)

schema = Schema(
    id=NUMERIC(stored=True),
    gtitle=TEXT(stored=True, analyzer=analyzer),
    gpic=TEXT(stored=True, analyzer=analyzer),
    isDelete=NUMERIC(stored=True),
    gunit=TEXT(stored=True),
    gclick=NUMERIC(stored=True),
    gjianjie=TEXT(stored=True),
    gkucun=NUMERIC(stored=True),
    gcontent=TEXT(stored=True),
    gtype_id=NUMERIC(stored=True)
)

ix = create_in("./index/", schema, indexname='goods')
writer = ix.writer()

index = 1
for each in result:
    writer.add_document(id=each.id,
                        gtitle=each.gtitle,
                        gpic=each.gpic,
                        isDelete=each.isDelete,
                        gunit=each.gunit,
                        gclick=each.gclick,
                        gjianjie=each.gjianjie,
                        gkucun=each.gkucun,
                        gcontent=each.gcontent,
                        gtype_id=each.gtype_id
                        )
    print(index)
    index = index + 1

writer.commit()
db.close()
