worker: celery --app celery_app.app worker -B -E -l info
worker_auxiliar: celery --app celery_app.app worker -E -l info
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
