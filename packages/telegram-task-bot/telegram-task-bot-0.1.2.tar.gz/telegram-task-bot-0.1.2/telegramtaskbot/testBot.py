import unittest

from unittest import mock

from telegramtaskbot.Tasks.Task import Task
from telegramtaskbot.Bot import TelegramTaskBot

class TestTask(Task):
    job_name = 'test_task'

class TestBot(unittest.TestCase):
    

    def setUp(self) -> None:
        self.testTaks = TestTask()
        # self.bot = TelegramTaskBot([self.testTaks])

    @mock.patch('telegramtaskbot.Tasks.Task.Task')
    def test_init(self, mock_task)-> None:
        bot = TelegramTaskBot([mock_task])

        self.assertTrue(mock_task._start.called)
