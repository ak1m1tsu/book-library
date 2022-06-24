from loguru import logger
import config


logger.add(
    sink=config.LOG_PATH,
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL,
    rotation=config.LOG_ROTATION,
    compression=config.LOG_COMPRESSION
)