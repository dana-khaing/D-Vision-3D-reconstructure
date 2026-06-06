from app.config import settings
from worker.pipeline import run_pipeline


class WorkerSettings:
    redis_settings_str = settings.redis_url
    functions = [run_pipeline]
    max_jobs = 1            # one GPU job at a time — never parallel on 24 GB
    job_timeout = settings.job_timeout_seconds
    keep_result = 3600      # keep job result in Redis for 1 hour
