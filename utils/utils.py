from datetime import datetime
import logging
from pathlib import Path


def setup_logging(log_dir: Path , filename: str) -> None:
    """Logs dans un fichier daté et dans la console."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{filename}-{datetime.today():%Y-%m-%d}.log"
 
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )  
    