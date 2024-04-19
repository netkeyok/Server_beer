from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, and_, desc, func

from api_request.request_to_sm import get_article_name
from dbcon.model import ConnectTap, ConnectTapSpec, Utms, ConnectTapNames
from dbcon.pydantic_models import Package, Doc
from dbcon.config import session

gmt_plus_5 = timezone(timedelta(hours=5))


def organization_list():
    org_list = (select(Utms.Id, Utms.Comment, Utms.num))
    result = session.execute(org_list)
    dict_iterator = result.mappings()

    # Получаем список словарей
    results = list(dict_iterator)
    return results


def request_docs(date_start, date_end, org_id=None):
    # Создание базового запроса
    query = (
        select(ConnectTapSpec.BaseId, ConnectTapSpec.Mark,
               (ConnectTap.DocDate + ConnectTapSpec.ExpDay).label('expdate'),
               ConnectTapNames.NAME.label('name'),
               ConnectTapNames.BARCODE.label('barcode'))
        .join(ConnectTap, ConnectTapSpec.BaseId == ConnectTap.id)
        .join(ConnectTapNames, ConnectTapNames.BARCODE == func.SUBSTRING(ConnectTapSpec.Mark, 4, 13))
        .where(
            and_(
                ConnectTap.Status == 1,
                ConnectTap.DocDate.between(date_start, date_end),
            )
        ).order_by(desc(ConnectTapSpec.BaseId))
    )

    # Добавление условия org_id, если он не равен None
    if org_id is not None:
        query = query.where(ConnectTap.OrgId == org_id)

    # Выполнение запроса и получение результатов
    results = session.execute(query).all()

    # Обработка результатов
    data = []
    for row in results:
        data.append(Doc(BaseId=row[0], Mark=row[1], expdate=row[2], name=row[3], barcode=row[4]))

    # Создание и возврат объекта Package
    package = Package(items=data)
    return package


def update_tap_names(barcode, name):
    with session as s:
        if name is None:
            name = 'Штрихкод отсутствует в Супермаг'
        new_barcode = ConnectTapNames(
            BARCODE=barcode,
            NAME=name,
            UPDATED=datetime.now(gmt_plus_5),
        )
        s.merge(new_barcode)
        s.commit()


def get_barcode_names(mark):
    shcode = mark[3:16]
    with session as e:
        barcode_name = (
            select(ConnectTapNames.NAME).where(ConnectTapNames.BARCODE == shcode)
        )
        result = e.execute(barcode_name).fetchone()
    if result is not None:
        return {'name': result[0]}
    else:
        return {}


def update_articles_name(day=5):
    counter = Counter()
    current_time = datetime.now()
    print("Текущее время:", current_time)
    days_ago = current_time - timedelta(days=day)
    docs = request_docs(date_start=days_ago, date_end=current_time).items
    for doc in docs:
        name = get_article_name(doc.Mark)
        if name:
            shcode = doc.Mark[3:16]
            update_tap_names(barcode=shcode, name=name)
            counter['Updated'] += 1
        else:
            counter['Missing'] += 1
    return dict(counter)


org_id = '3'

date_1 = '20.02.2024'
date_2 = '26.03.2024'
if __name__ == '__main__':
    data = request_docs(date_1, date_2).items
    for d in data:
        print(d)
    # data = organization_list()
    # for i in data:
    #     print(i['Id'])
    # data = update_articles_name()
    # data = get_barcode_names('0104670212250164215EDPGhr93y/w3')
    # print(data['name'])
