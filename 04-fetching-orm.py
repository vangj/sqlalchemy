from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)

with Session(engine) as session:
    session.execute(text('CREATE TABLE some_table (x int, y int)'))

    session.execute(
        text('INSERT INTO some_table(x, y) values(:x, :y)'),
        [{'x': x, 'y': x * x} for x in range(1, 12)]
    )

    # rows are named tuples
    result = session.execute(text('SELECT x, y FROM some_table'))
    print([{'x': r.x, 'y': r.y} for r in result])

    # unpack tuple
    result = session.execute(text('SELECT x, y FROM some_table'))
    print([{'x': x, 'y': y} for x, y in result])

    # treat rows like sequences
    result = session.execute(text('SELECT x, y FROM some_table'))
    print([{'x': r[0], 'y': r[1]} for r in result])

    # get rows to be like dictionaries
    result = session.execute(text('SELECT x, y FROM some_table'))
    print([{'x': r['x'], 'y': r['y']} for r in result.mappings()])

    # parameterized query
    result = session.execute(
        text('SELECT x, y from some_table where y > :y'),
        {'y': 2}
    )
    print([{'x': r.x, 'y': r.y} for r in result])

    # binding parameters
    stmt = text('SELECT x, y from some_table where y > :y').bindparams(y=6)
    result = session.execute(stmt)
    print([{'x': r.x, 'y': r.y} for r in result])

    #update
    result = session.execute(
        text('UPDATE some_table SET y=:y WHERE x=:x'),
        [{'x': 9, 'y': 82}]
    )

    stmt = text('SELECT x, y from some_table where x=:x').bindparams(x=9)
    result = session.execute(stmt)
    print([{'x': r.x, 'y': r.y} for r in result])
    