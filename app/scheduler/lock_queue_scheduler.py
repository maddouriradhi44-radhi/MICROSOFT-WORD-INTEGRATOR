from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.services.document_lock_queue_service import (
    DocumentLockQueueService,
)


scheduler = BackgroundScheduler()

queue_service = DocumentLockQueueService()


def check_expired_lock_requests():
    """
    Check expired document lock notifications.
    """

    db: Session = SessionLocal()

    try:
        queue_service.expire_old_requests(
            db
        )

    finally:
        db.close()



def start_scheduler():

    scheduler.add_job(
        check_expired_lock_requests,
        trigger="interval",
        seconds=30,
        id="lock_queue_expiration",
        replace_existing=True,
    )

    scheduler.start()
    print("Scheduler started")



def stop_scheduler():

    scheduler.shutdown()