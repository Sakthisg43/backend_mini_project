
from decouple import config


def connect_to_db(app):
    db_connection = 'postgresql://{}:{}@{}:{}/{}'.format(
        config('user'),
        config('password'),
        config('host'),
        config('port'),
        config('db_name')
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    return app