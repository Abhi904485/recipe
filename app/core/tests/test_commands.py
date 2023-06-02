"""
Test Custom Django management Commands
"""
from unittest.mock import patch, Mock

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as psycopg2Error


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Test Commands
    """

    def test_wait_for_db_ready(self, patched_check: Mock):
        """
        Test Waiting For Database if DB is ready
        :return:
        """
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep: Mock, patched_check: Mock):
        """
        Test Waiting For Database if getting Operational Error or psycopg2Error
        :return:
        """
        patched_check.side_effect = [psycopg2Error] * 2 + [
            OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
