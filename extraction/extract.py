import logging
from datetime import datetime
from pathlib import Path
from typing import Counter
import pandas as pd
import re
import unicodedata

from utils.minio_client import MinIOClient, upload_chunk


BASE_DIR = Path(__file__).resolve().parent
CHUNCK_SIZE=100_000

                
def normalize_column_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    if name[:1].isdigit():
        name = f"col_{name}"
    return name

def build_column_mapping(columns: list[str]) -> dict[str, str]:
    """Associe chaque nom brut à son nom normalisé et refuse les doublons."""
    mapping = {col: normalize_column_name(col) for col in columns}
 
    counts = Counter(mapping.values())
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    if duplicates:
        message = f"Duplicate column names after normalization: {', '.join(duplicates)}"
        logging.error(message)
        raise ValueError(message)
    
    return mapping


def checking_existing_columns(file_name, expected_columns):
    actuals_columns = pd.read_csv(file_name, sep=";", nrows=0).columns
    
    for p in expected_columns:
        if p not in actuals_columns:
            logging.info('missing columns %s (%s)', p, file_name)
            
        
    return actuals_columns


def read_large_file(file, chunck_size):
    for d_chunck in pd.read_csv(file, sep=";", chunksize=chunck_size, dtype="str"):
        yield d_chunck
    

logger = logging.getLogger(__name__)

def extract(folder: Path, year: int, expected_columns: list[str]) -> None:
    # the file to read
    file_name = folder / f"valeursfoncieres-{year}.txt"
    
    logger.info('Start extraction for %s (%s)', year, file_name)
    
    # creating minio client
    client = MinIOClient()
    
    # checink existing column
    actuals_columns = checking_existing_columns(file_name, expected_columns)
    column_mapping = build_column_mapping(actuals_columns)

    
    # read chunck
    parts = 0
    total_rows  = 0
    
    for part, d_chunck in enumerate(read_large_file(file_name, CHUNCK_SIZE), start=1):
        
        norm_chunck = d_chunck.rename(columns=column_mapping)
        
        key = upload_chunk(client, norm_chunck, year, part)
        
        parts = part
        total_rows += len(norm_chunck)
        
        logger.info("Part %d sent (%d rows): %s", part, len(norm_chunck), key)
        
    logger.info("End extraction for %s: %d parts, %d rows", year, parts, total_rows)
    

def setup_logging(log_dir: Path) -> None:
    """Logs dans un fichier daté et dans la console."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"extraction-{datetime.today():%Y-%m-%d}.log"
 
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )  
    

if __name__ == "__main__":
    setup_logging(BASE_DIR / "log")
    extract(BASE_DIR / "raw", 2025, [])