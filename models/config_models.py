from pydantic import BaseModel
from typing import Optional
from enum import Enum

class AppConfig(BaseModel):
    name: str
    port: int
    build: str


class ScalingConfig(BaseModel):
    metric: str
    threshold: int


class OrchestratorConfig(BaseModel):
    replica: int
    min_replica: int
    max_replica: int
    scaling: Optional[ScalingConfig] = None


class ProxyMode(str, Enum):
    load_balancer = "load_balancer"
    reverse_proxy = "reverse_proxy"
    hybrid = "hybrid"


class ProxyConfig(BaseModel):
    mode: ProxyMode = ProxyMode.load_balancer 
    strategy: str


class FlowConfig(BaseModel):
    app: AppConfig
    orchestration: OrchestratorConfig
    proxy: ProxyConfig