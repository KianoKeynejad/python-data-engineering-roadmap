import logging
from pathlib import Path


def setup_logging():

    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        filename=log_file,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger(__name__)