from pydantic import BaseModel


class FeatureFile(BaseModel):
    id: str
    filename: str
    hash: str
    created_at: str
