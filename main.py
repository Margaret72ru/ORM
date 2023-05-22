import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_db, fill_test_data, Book, Shop, Publisher, Sale, Stock

DSN = 'postgresql://postgres:postgres@localhost:5432/test_db'
engine = sqlalchemy.create_engine(DSN)

create_db(engine)

Session = sessionmaker(bind=engine)
session = Session()

fill_test_data(session)

pub_name = input("Введите имя или идентификатор издателя:")

if pub_name.isdecimal():
    qPub = session.query(Publisher).filter(Publisher.id == pub_name).subquery()
else:
    qPub = session.query(Publisher).filter(Publisher.name.like(pub_name)).subquery()

for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Stock, Stock.id_book == Book.id).\
        join(Shop, Shop.id == Stock.id_shop).\
        join(Sale, Sale.id_stock == Stock.id).\
        join(Publisher, Publisher.id == Book.id_publisher).\
        join(qPub, qPub.c.id == Book.id_publisher).all():
    print(f'{c.title:40}\t| {c.name}\t| {c.price:5}\t| {c.date_sale.strftime("%m.%d.%Y")}')

session.close()