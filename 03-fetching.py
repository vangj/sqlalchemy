from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)

with engine.connect() as conn:
    conn.execute(text('CREATE TABLE some_table (x int, y int)'))

    conn.execute(
        text('INSERT INTO some_table(x, y) values(:x, :y)'),
        [{'x': x, 'y': x * x} for x in range(1, 12)]
    )

    # rows are named tuples
    result = conn.execute(text('SELECT x, y FROM some_table'))
    print([{'x': r.x, 'y': r.y} for r in result])

    # unpack tuple
    result = conn.execute(text('SELECT x, y FROM some_table'))
    print([{'x': x, 'y': y} for x, y in result])

    # treat rows like sequences
    result = conn.execute(text('SELECT x, y FROM some_table'))
    print([{'x': r[0], 'y': r[1]} for r in result])

    # get rows to be like dictionaries
    result = conn.execute(text('SELECT x, y FROM some_table'))
    print([{'x': r['x'], 'y': r['y']} for r in result.mappings()])

    # parameterized query
    result = conn.execute(
        text('SELECT x, y from some_table where y > :y'),
        {'y': 2}
    )
    print([{'x': r.x, 'y': r.y} for r in result])

    # binding parameters
    stmt = text('SELECT x, y from some_table where y > :y').bindparams(y=6)
    result = conn.execute(stmt)
    print([{'x': r.x, 'y': r.y} for r in result])
    