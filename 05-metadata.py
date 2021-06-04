from sqlalchemy import MetaData, ForeignKey, create_engine
from sqlalchemy import Table, Column, Integer, String

metadata = MetaData()

user_table = Table(
    'user_account',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('full_name', String)
)

address_table = Table(
    'address',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)

print(user_table.primary_key)
print(user_table.c.id)
print(user_table.c.name)
print(user_table.c.full_name)

print('-' * 15)

print([field_name for field_name in user_table.c.keys()])

print('-' * 15)

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)

metadata.create_all(engine)
metadata.drop_all(engine)