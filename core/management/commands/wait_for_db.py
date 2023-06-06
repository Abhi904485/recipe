"""
Django Command to wait for the database to be available
"""
import time

from django.core.management import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as psycopg2Error


class Command(BaseCommand):
    """
    Django Command to Wait for the database.
    """

    def handle(self, *args, **options):
        self.stdout.write("Waiting For The Database")
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2Error, OperationalError):
                self.stderr.write(self.style.ERROR(
                    'Database Unavailable Sleeping For 1 Second...'))
                time.sleep(1)
        self.stderr.write(self.style.SUCCESS('Database Available...'))
