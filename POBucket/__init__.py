import os
import dotenv
import pymysql

from pathlib import Path


DIR_PATH = Path(__file__).resolve().parent.parent

pymysql.install_as_MySQLdb()
dotenv.load_dotenv(f'{DIR_PATH}/env/.env')


MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DATABASE"),
        'USER': os.environ.get("SQL_SERVER_USER"),
        'PASSWORD': os.environ.get('SQL_SERVER_ROOT_PASSWORD'),
        'HOST': os.environ.get('SQL_SERVER_HOST'),
        'PORT': os.environ.get('SQL_SERVER_PORT'),
    }
}

SQLITE3 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'{DIR_PATH}/Database/db.sqlite3',
    }
}
