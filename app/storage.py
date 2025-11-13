import os
from typing import Dict, Any
from datetime import datetime
import logging
from pathlib import Path
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
logger = logging.getLogger(__name__)
def gcs_client():
    # Only used when USE_LOCAL_STORAGE is not true
    return storage.Client(project=os.getenv("GCP_PROJECT_ID"))

def upload_bytes(bucket: str, blob_name: str, data: bytes, content_type: str = "application/octet-stream"):
    """
    If USE_LOCAL_STORAGE=true,
    Otherwise, upload to GCS.
    """
    use_local = os.getenv("USE_LOCAL_STORAGE", "").lower() == "true"
    if use_local:
        base = Path("local_uploads") / bucket
        dest = base / blob_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return f"local://{dest.as_posix()}"
    else:
        try:
            client = gcs_client()
            b = client.bucket(bucket)
            blob = b.blob(blob_name)
            blob.upload_from_string(data, content_type=content_type)
            return f"gs://{bucket}/{blob_name}"
        except DefaultCredentialsError as e:
            # Make the error clear if user forgot creds
            raise RuntimeError(
                "GCP credentials missing. Set GOOGLE_APPLICATION_CREDENTIALS, "
                "GCP_PROJECT_ID, GCS_RAW_BUCKET, GCS_PROCESSED_BUCKET or set USE_LOCAL_STORAGE=true."
            ) from e


Base = declarative_base()

class MetadataRecord(Base):
    __tablename__ = "file_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(String(32), unique=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))
    filename = Column(String(255))
    filesize_bytes = Column(Integer)
    filetype = Column(String(100))
    uploaded_utc = Column(String(20))
    phone_valid = Column(String(10))
    email_valid = Column(String(10))  # New field
    anomaly = Column(String(10))      # New field
    anomaly_details = Column(JSON)    # New field
    raw_key = Column(Text)
    processed_key = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Database connection
engine = None
SessionLocal = None

def init_database():
    global engine, SessionLocal
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.warning("DATABASE_URL not set, skipping database initialization")
        return
    
    try:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

def save_metadata_to_db(metadata: Dict[str, Any]) -> bool:
    """Save metadata to PostgreSQL database"""
    if SessionLocal is None:
        logger.warning("Database not initialized, skipping metadata save")
        return False
    
    try:
        db = SessionLocal()
        record = MetadataRecord(
            upload_id=metadata.get("upload_id"),
            name=metadata.get("name"),
            email=metadata.get("email"),
            phone=metadata.get("phone"),
            filename=metadata.get("filename"),
            filesize_bytes=metadata.get("filesize_bytes"),
            filetype=metadata.get("filetype"),
            uploaded_utc=metadata.get("uploaded_utc"),
            phone_valid=str(metadata.get("phone_valid")),
            email_valid=str(metadata.get("email_valid")),  # New field
            anomaly=str(metadata.get("anomaly")),           # New field
            anomaly_details=metadata.get("anomaly_details"), # New field
            raw_key=metadata.get("raw_key"),
            processed_key=metadata.get("processed_key")
        )
        
        db.add(record)
        db.commit()
        db.close()
        logger.info(f"Metadata saved to database for upload_id: {metadata.get('upload_id')}")
        return True
    except Exception as e:
        logger.error(f"Failed to save metadata to database: {e}")
        return False
