# server
CONNECTION = ("127.0.0.1", 8080)
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
