import json
import sys

from loguru import logger as logger_


def serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "message": record["message"],
        "level": record["level"].name,
        **record["extra"].get("extra", {}),
    }
    return json.dumps(subset, ensure_ascii=False)


def patching(record):
    record["serialized_log"] = serialize(record)


logger_.remove(0)

logger = logger_.patch(patching)
logger.add(sys.stderr, format="{serialized_log}")

__all__ = [
    "logger"
]