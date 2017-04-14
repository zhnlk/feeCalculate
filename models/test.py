# encoding:utf8
from models.CashModel import Cash
from models.CommonModel import session

session.add(Cash())
session.add(Cash())

session.add(Cash())
session.add(Cash())
session.add(Cash())
session.add(Cash())
session.flush()
session.commit()

print(session.query(Cash).all())
