import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    postgresql_url: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
        
    @classmethod
    def load_from_yaml(cls, yaml_path: str = "config.yaml") -> "AppConfig":

        with open(yaml_path, "r") as file:
            yaml_data = yaml.safe_load(file)
            if not yaml_data:
                yaml_data = {}
            
        return cls(**yaml_data)
    
app_config = AppConfig.load_from_yaml()