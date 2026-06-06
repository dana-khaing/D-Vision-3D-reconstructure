api:    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
worker: python -m arq worker.settings.WorkerSettings
web:    cd frontend && npm run dev
