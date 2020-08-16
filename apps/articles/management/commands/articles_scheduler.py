import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand

from apps.articles.tasks import fetch_new_articles
from conf.settings import DRAMMATIQ_TASK_SCHEDULE


class Command(BaseCommand):
    """Command to start drammatiq tasks"""

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(
            fetch_new_articles.send, DRAMMATIQ_TASK_SCHEDULE.get("fetch_new_articles"),
        )
        try:
            logging.info("Starting task scheduler")
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            logging.info("Task scheduler stopped")
