from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from ..helpers.settings import get_settings
from pymongo import MongoClient
from uuid import uuid4
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.base import BaseTrigger
from typing import Dict, Any


environment = get_settings()
client = MongoClient(environment.MONGO_URI.strip())
scheduler = BackgroundScheduler(
    jobstores={
        "default": MongoDBJobStore(
            database=environment.MONGO_DB, collection="scheduling_jobs", client=client
        )
    }
)

def create_job(
    func: callable,
    func_args: Dict[str, Any],
    trigger_type: IntervalTrigger | CronTrigger | DateTrigger = IntervalTrigger,
):
    """
    Create a job in the scheduler.

    :param func: The function to be scheduled.
    :param trigger_type: The type of trigger for the job (default is interval).
    """
    job_id = str(uuid4())
    scheduler.add_job(func, trigger_type, kwargs=func_args, id=job_id, replace_existing=True)
    return job_id


def remove_job(job_id: str):
    """
    Remove a job from the scheduler.

    :param job_id: The ID of the job to be removed.
    """
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        return True
    return False
