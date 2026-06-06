from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_secret_key: str = "changeme"

    database_url: str = "sqlite+aiosqlite:///./dev.db"
    redis_url: str = "redis://localhost:6379"

    data_dir: Path = Path.home() / "party3d-data"

    opensplat_bin: Path = Path.home() / "OpenSplat/build/opensplat"
    max_gaussians: int = 1_000_000
    opensplat_iterations: int = 30_000
    sam2_checkpoint: Path = Path.home() / "models/sam2/sam2.1_hiera_base_plus.pt"

    max_photos_per_event: int = 400
    job_timeout_seconds: int = 7200
    memory_alert_gb: float = 18.0
    memory_kill_gb: float = 22.0

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / "uploads"

    @property
    def workspaces_dir(self) -> Path:
        return self.data_dir / "workspaces"

    @property
    def outputs_dir(self) -> Path:
        return self.data_dir / "outputs"

    def ensure_dirs(self) -> None:
        for d in [self.uploads_dir, self.workspaces_dir, self.outputs_dir]:
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()
