import os

db_host = os.environ.get('db_host', 'localhost')
db_port = str(os.environ.get('db_port', '5432'))
db_name = str(os.environ.get('db_name', 'fastapi-notes'))
db_username = str(os.environ.get('db_username', 'postgres'))
db_password = str(os.environ.get('db_password', ''))
ssl_mode = str(os.environ.get('ssl_mode', 'prefer'))


DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, db_host, db_port, db_name,
                                                               ssl_mode)

