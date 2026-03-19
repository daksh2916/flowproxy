from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class RequestData(BaseModel):
    id: str
    method: str
    url: str
    headers: Dict[str, str]
    query_parameter: Dict[str, str] = Field(default_factory=dict)
    body: Optional[Any] = None
