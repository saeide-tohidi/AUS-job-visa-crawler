from celery import Celery

app = Celery(
    "AUS_job_visa_crawler",
    broker="redis://localhost:6379",
    backend="redis://localhost:6379",
    include=["tasks"],
)

app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
