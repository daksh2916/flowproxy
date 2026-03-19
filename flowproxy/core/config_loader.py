import yaml
from pathlib import Path
from ..models.config_models import FlowConfig
from pydantic import ValidationError

DEFAULT_CONFIG_FILE = "flowproxy.yml"

class ConfigLoader:
    def __init__(self):
        self.default_config_file = DEFAULT_CONFIG_FILE


    def load_config(self, path = DEFAULT_CONFIG_FILE)->FlowConfig:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found at {path.resolve()}")
        
        with path.open("r") as f:
            config_content = yaml.safe_load(f)

        try:
            config = FlowConfig.model_validate(config_content)
        except ValidationError as e:
            raise ValueError(f"Invalid config file:\n{e}")
        
        return config

          