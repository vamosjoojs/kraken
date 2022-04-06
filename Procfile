worker: celery --app celery_app.app worker -E -l info
beat: celery --app celery_app.app beat
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}


