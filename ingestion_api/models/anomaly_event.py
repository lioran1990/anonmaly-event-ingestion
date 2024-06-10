from pydantic import BaseModel, Field, validator
from typing import List, Optional, Any


class AnomalyEvent(BaseModel):
    id: str = Field(..., pattern=r'^\d{4,12}$')
    event_id: str = Field(..., pattern=r'^\d{4,12}$')
    role_id: str
    event_type: str
    event_timestamp: str
    affected_assets: Optional[List[str]] = None

    @validator('id', 'event_id')
    def id_must_be_numeric(cls, v):
        if not v.isdigit():
            raise ValueError('must be a number with 4-12 digits')
        return v


# Define the base response models
class Metadata(BaseModel):
    request_id: str


class BaseResponse(BaseModel):
    data: Any
    metadata: Metadata


# Define the specific response data model for the ingest endpoint
class IngestResponseData(BaseModel):
    status: str


class IngestResponse(BaseResponse):
    data: IngestResponseData
