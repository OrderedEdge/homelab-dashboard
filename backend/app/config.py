from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    prometheus_url: str = "http://192.168.10.21:9090"
    docker_hosts: str = "cosmos:192.168.10.16"
    poll_interval: int = 30
    services_file: str = "/app/services.json"

    class Config:
        env_prefix = "DASHBOARD_"


settings = Settings()
