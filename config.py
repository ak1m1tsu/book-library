from enum import Enum


# server
CONNECTION=("127.0.0.1", 8080)

# logging
LOG_PATH='./logs/error.log'
LOG_FORMAT="{time} | {level} | {message}"
LOG_LEVEL='ERROR'
LOG_ROTATION='10 KB'
LOG_COMPRESSION='zip'