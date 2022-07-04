import os
from dotenv import load_dotenv


load_dotenv()

# server
COMMAND_COUNT = 7
BOOK_HEADERS = ['ID', 'Имя', 'Автор', 'Кол-во страниц']

# logging
ERROR_PATH = './logs/error.log'
DEBUG_PATH = './logs/debug.log'
INFO_PATH = './logs/info.log'
LOG_FORMAT = "[•] | {time} | {level} | {message}"
ERROR = 'ERROR'
DEBUG = 'DEBUG'
INFO = 'INFO'
LOG_ROTATION = '10 KB'
LOG_COMPRESSION = 'zip'

# database
DATABASE_URL = os.getenv('DATABASE_URL')

#rabbitmq
RABBITMQ_DEFAULT_USER=os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS=os.getenv('RABBITMQ_DEFAULT_PASS')