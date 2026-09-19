import logging
import os
import io
import pandas as pd
import psycopg
from pandas import DataFrame


from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = (
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "EXTERNAL_PG_PORT",
    "POSTGRE_HOST"
)


class PgClient:
	

    def __init__(self, region: str = "us-east-1") -> None:
        missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
        if missing:
            message = f"Missing environement variable : {', '.join(missing)}"
            logger.error(message)
            raise ValueError(message)
  
    def connect(self) -> None:
        
        try:
            self.db_connect = psycopg.connect(
				port = os.environ["EXTERNAL_PG_PORT"],
				host = os.environ["POSTGRE_HOST"],
				dbname = os.environ["POSTGRES_DB"],
				user = os.environ["POSTGRES_USER"],
				password = os.environ["POSTGRES_PASSWORD"],
				
			)
        except psycopg.OperationalError as e:
            
            logger.error(f"Connection error : {e}")
            
            raise
        
    def close(self):
        self.db_connect.close()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.close()
	
    def insert_io_data(self, data : DataFrame , schema = "bronze" , table="dvf"):
        data_io = io.StringIO()
        data.to_csv(path_or_buf = data_io , index = False)
        data_io.seek(0)
        sql_statement = f"COPY {schema}.{table} ({', '.join(data.columns.values)}) FROM STDIN WITH (Format CSV , header True)"

        try:
            with self.db_connect.cursor() as c:
                with c.copy(sql_statement) as copy:
                    while chunck := data_io.read(1024*1024):
                        copy.write(chunck)
            
                self.db_connect.commit()
        except psycopg.Error as e :
            logger.exception("Error when trying to insert data into the db")
            self.db_connect.rollback()
            raise
            
    	
     