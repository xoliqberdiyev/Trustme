import os

import environ

environ.Env.read_env(os.path.join('.env'))


env = environ.Env(
    DB_ENGINE=(str, 'django.db.backends.postgresql'),
    DB_NAME=(str),
    DB_USER=(str, 'postgres'),
    DB_PASSWORD=(str),
    DB_HOST=(str, 'localhost'),
    DB_PORT=(int, 5432),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
    SECRET_KEY=(str),
    BOT_TOKEN=(str)
)