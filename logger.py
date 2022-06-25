from loguru import logger
import config


logger.add(
    sink=config.ERROR_PATH,
    format=config.LOG_FORMAT,
    level=config.ERROR,
    rotation=config.LOG_ROTATION,
    compression=config.LOG_COMPRESSION
)

logger.add(
    sink=config.DEBUG_PATH,
    format=config.LOG_FORMAT,
    level=config.DEBUG,
    rotation=config.LOG_ROTATION,
    compression=config.LOG_COMPRESSION
)

logger.add(
    sink=config.INFO_PATH,
    format=config.LOG_FORMAT,
    level=config.INFO,
    rotation=config.LOG_ROTATION,
    compression=config.LOG_COMPRESSION
)
