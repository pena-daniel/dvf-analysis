import logging
import os
import io
import pandas as pd
from datetime import datetime
from typing import TypedDict

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = (
    "MINIO_ENDPOINT",
    "MINIO_ROOT_USER",
    "MINIO_ROOT_PASSWORD",
    "MINIO_BUCKET",
)


class MinIOClient:
    """Client S3 (boto3) pour MinIO en local, compatible AWS S3."""

    def __init__(self, region: str = "us-east-1") -> None:
        missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
        if missing:
            message = f"Missing environement variable : {', '.join(missing)}"
            logger.error(message)
            raise ValueError(message)

        self.endpoint = os.environ["MINIO_ENDPOINT"]
        self.bucket = os.environ["MINIO_BUCKET"]

        self.client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=os.environ["MINIO_ROOT_USER"],
            aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
            region_name=region,
        )

        self._ensure_bucket_exists()

    def create_object(
        self,
        key: str,
        content: str | bytes,
        content_type: str = "application/octet-stream",
    ) -> None:
        """Envoie un objet dans le bucket. Lève une exception en cas d'échec."""
        body = content.encode("utf-8") if isinstance(content, str) else content
        try:
            self.client.put_object(
                Bucket=self.bucket, Key=key, Body=body, ContentType=content_type
            )
        except ClientError:
            logger.exception("Échec de l'envoi de s3://%s/%s", self.bucket, key)
            raise
        logger.info("Objet envoyé : s3://%s/%s (%d octets)", self.bucket, key, len(body))


    @staticmethod
    def _error_code(exc: ClientError) -> str:
        return exc.response.get("Error", {}).get("Code", "")

    def _ensure_bucket_exists(self) -> None:
        """Vérifie que le bucket existe et le crée sinon (confort en local)."""
        try:
            self.client.head_bucket(Bucket=self.bucket)
            logger.info("Bucket trouvé : %s", self.bucket)
            return
        except ClientError as exc:
            if self._error_code(exc) not in ("404", "NoSuchBucket"):
                logger.exception("Impossible de vérifier le bucket %s", self.bucket)
                raise

        logger.info("Bucket %s absent, création en cours", self.bucket)
        try:
            self.client.create_bucket(Bucket=self.bucket)
        except ClientError as exc:
            if self._error_code(exc) == "BucketAlreadyOwnedByYou":
                return
            logger.exception("Impossible de créer le bucket %s", self.bucket)
            raise
        logger.info("Bucket créé : %s", self.bucket)
        
        
def upload_chunk(client: MinIOClient, df: pd.DataFrame, year: int, part: int) -> str:
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, engine="pyarrow")

    key = f"dvf/year={year}/part-{part:05d}.parquet"
    client.create_object(key, buffer.getvalue(), content_type="application/vnd.apache.parquet")
    return key