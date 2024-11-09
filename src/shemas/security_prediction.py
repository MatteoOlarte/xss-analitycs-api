from pydantic import BaseModel


class SecurityPredictionSchema(BaseModel):
    is_secure: bool
    model: str
    confidence: float
