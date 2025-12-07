from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from report_generator import scheduled_report_task
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Daily report at 6 AM
    scheduler.add_job(
        scheduled_report_task,
        CronTrigger(hour=6, minute=0),
        id='daily_report',
        name='Generate daily report'
    )
    
    scheduler.start()
    logger.info("Scheduler started. Daily reports at 6:00 AM")
    
    return scheduler
