from datetime import datetime
from sqlalchemy import select, and_, desc
from dbcon.model import ConnectTap, ConnectTapSpec, Utms
from dbcon.pydantic_models import Package, Doc
from dbcon.config import session


def organization_list():
    org_list = (select(Utms.Id, Utms.Comment, Utms.num))
    result = session.execute(org_list)
    dict_iterator = result.mappings()

    # Получаем список словарей
    results = list(dict_iterator)
    print(results)
    return results


def request_docs(date_start, date_end, org_id):

    request = (
        select(ConnectTapSpec.BaseId, ConnectTapSpec.Mark,
               (ConnectTap.DocDate + ConnectTapSpec.ExpDay).label('expdate'))
        .join(ConnectTap, ConnectTapSpec.BaseId == ConnectTap.id)
        .where(
            and_(
                ConnectTap.Status == 1,
                ConnectTap.DocDate.between(date_start, date_end),
                ConnectTap.OrgId == org_id,
            )
        ).order_by(desc(ConnectTapSpec.BaseId))
    )

    # Получение результатов
    results = session.execute(request).all()

    data = [Doc(BaseId=row[0], Mark=row[1], expdate=row[2]) for row in results]
    #
    package = Package(items=data)

    # Возвращение объекта Package
    return package


org_id = '3'

date_1 = '20.02.2024'
date_2 = '26.03.2024'
if __name__ == '__main__':
    docs = request_docs(date_1, date_2, org_id)
    print(docs)
