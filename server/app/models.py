from typing import Union, Optional
from pydantic import BaseModel, Field


class Filters(BaseModel):
    min_score: int = Field(0, ge=0)
    min_similarity: int = Field(0.0, ge=0)
    model: Optional[str] = Field(None)
    provider: Optional[str] = Field(None)
    min_timestamp: Optional[int] = Field(0, ge=0)
    max_timestamp: Optional[int] = Field(999999999999, ge=0)


class RequestBody(BaseModel):
    filters: Filters
    search: Union[int, str] = Field(..., description="An integer ID or a string search key")
    sort_by: str = Field("miner", description="Field to sort by")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sorting order, 'asc' or 'desc'")
