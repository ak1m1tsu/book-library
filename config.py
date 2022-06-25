# server
CONNECTION=("127.0.0.1", 8080)
COMMAND_COUNT=7

# logging
ERROR_PATH='./logs/error.log'
DEBUG_PATH='./logs/debug.log'
LOG_FORMAT="{time} | {level} | {message}"
ERROR='ERROR'
DEBUG='DEBUG'
LOG_ROTATION='10 KB'
LOG_COMPRESSION='zip'