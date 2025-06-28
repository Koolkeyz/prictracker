from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class SchedulerTiggerType(str, Enum):
    date = "date"
    interval = "interval"
    cron = "cron"