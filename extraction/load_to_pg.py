
import logging
from pathlib import Path
from extraction import extract
from utils.minio_client import MinIOClient
from utils.pg_client import PgClient
from utils.utils import setup_logging
import pandas as pd
import io


BASE_DIR = Path(__file__).resolve().parent

logger = logging.getLogger(__name__)

def load_to_pg(year:int) :
	"""Load the extracted data into PostgreSQL."""
	# Placeholder for the actual implementation
	logger.info(f"Loading data for year {year} into PostgreSQL.")
	# Here you would add the code to connect to PostgreSQL and load the data
	client = MinIOClient()
	prefix = f"dvf/year={year}/"
	keys = client.list_keys(prefix=prefix) 
	
	
	if not keys:
		message = f"There is no object in Minio for the specified prefix {prefix}"
     
		logger.error(message)
		
		raise ValueError(message)

	with PgClient() as pg: 
	
		for key in keys:
			logger.info(f"Loading {key} into PostgreSQL.")
			# Here you would add the code to download the object from MinIO and load it into PostgreSQL
			key_content = client.get_object(key)
			
			df = pd.read_parquet(io.BytesIO(key_content))

			df["annee"] = str(year) 

			pg.insert_io_data(df)

			




if __name__ == "__main__":
    setup_logging(BASE_DIR / "log" , "extraction")
    load_to_pg(2025)