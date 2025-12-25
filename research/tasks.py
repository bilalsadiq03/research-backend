import time
from celery import shared_task
from django.db import transaction
from .models import ResearchSession



@shared_task(bind=True)
def run_research_task(self, research_id: int):
    try:
        with transaction.atomic():
            research = ResearchSession.objects.select_for_update().get(id=research_id)
            research.status = 'RUNNING'
            research.save()

        # Simulate a long-running research task
        time.sleep(5)

        #Mock Reserach Result
        research.final_report = "This is a mock research report generated asynchronously."
        research.status = 'COMPLETED'
        research.trace_id = self.request.id
        research.save()


    except Exception as e:
        research = ResearchSession.objects.filter(id=research_id).update(
            status='FAILED',
        )
        raise e