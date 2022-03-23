worker: celery --app celery_app.app worker -E -l info --pool=solo
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
