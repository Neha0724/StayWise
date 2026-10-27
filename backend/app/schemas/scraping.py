from pydantic import BaseModel, Field

class ScrapeRequest(BaseModel):
    city: str = Field("Mumbai", min_length=2, max_length=80)
    limit: int = Field(30, ge=5, le=100)
