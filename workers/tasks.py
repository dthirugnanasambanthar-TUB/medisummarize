import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../rag'))

from workers.celery_app import celery_app
from rag.summariser import summarise_note

@celery_app.task(bind=True, max_retries=3)
def summarise_note_task(self, note_id: str):
    try:
        summary = summarise_note(note_id)
        return summary.model_dump()
    except Exception as e:
        raise self.retry(exc=e, countdown=5)