from typing import Final
from datetime import datetime
from pathlib import Path
from types import TracebackType
import itertools
import logging as log
import os
import sys

LOGS_PATH: Final[Path] = Path.cwd() / "logs"
LOG_FILES_LIMIT: Final[int | dict[str, int] | None] = 10
INFO_OVERFLOW_LOGGERS: Final[tuple[str, ...]] = ()
DEBUG_FILE: Final[bool] = True


LOGS_PATH.mkdir(exist_ok=True)
LOG_ORIGIN = "main"
current_time = datetime.utcnow().strftime("%d.%m.%y_%H.%M.%S.%f")
filename = f"{LOG_ORIGIN}_log_{current_time}.txt"

stream_handler = log.StreamHandler(sys.stdout)
main_handler = log.FileHandler(LOGS_PATH / filename, mode="a", encoding="UTF-8")
handlers = [stream_handler, main_handler]

stream_handler.setLevel(log.INFO)
main_handler.setLevel(log.INFO)
log.basicConfig(
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
    datefmt="%d.%m.%y %H:%M:%S",
    level=log.DEBUG,
    handlers=handlers,
)

if DEBUG_FILE:
    debug_handler = log.FileHandler(
        LOGS_PATH / f"debug_{filename}",
        mode="a",
        encoding="UTF-8"
    )
    handlers.append(debug_handler)
    debug_handler.setLevel(log.DEBUG)


def _handle_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: "TracebackType",
) -> None:
    if not issubclass(exc_type, KeyboardInterrupt):
        error_logger.exception(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    return sys.__excepthook__(exc_type, exc_value, exc_traceback)


def reset_loggers():
    """Reset log level for unnecessary loggers

    (disable logs with too high level)
    """
    for i in INFO_OVERFLOW_LOGGERS:
        log.getLogger(i).setLevel(log.WARNING)


def _cleanup_old_logs():
    log_files = sorted(
        itertools.chain(
            LOGS_PATH.glob(f"{LOG_ORIGIN}_log_*.txt"),
            LOGS_PATH.glob(f"debug_{LOG_ORIGIN}_log_*.txt"),
        ),
        key=lambda x: os.path.getctime(x),
        reverse=True
    )
    for i in log_files[get_count_limit():]:
        if i.is_file() and i.name != filename:
            i.unlink()


def get_count_limit(origin: str | None = None) -> int:
    """Get limit of logs count"""
    if origin is None:
        origin = LOG_ORIGIN

    if LOG_FILES_LIMIT is None:
        limit = 10
    elif isinstance(LOG_FILES_LIMIT, int):
        limit = LOG_FILES_LIMIT
    else:
        limit = LOG_FILES_LIMIT.get(origin, LOG_FILES_LIMIT.get("_", 10))

    if DEBUG_FILE:
        limit *= 2
    return limit


error_logger = log.getLogger("errors")
sys.excepthook = _handle_exception
_cleanup_old_logs()
reset_loggers()
