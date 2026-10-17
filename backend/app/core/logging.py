import logging
import sys


def setup_logging(debug: bool = False) -> None:
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s: %(message)s"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    # Suppress verbose third-party network tracing in terminal
    for noisy_logger in ["httpcore", "httpx", "urllib3"]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
