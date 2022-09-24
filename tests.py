import unittest
from agents.traffit_bot import TraffitBot
import os


class TestTraffitBot(unittest.TestCase):

    def setUp(self) -> None:
        print(f'setting up class...{self.cls.__name__}')
        self.bot = TraffitBot(login=os.environ.get("LOGIN"), password=os.environ.get("PASSWORD"))

    def tearDown(self) -> None:
        print(f'tearing down clas...{self.cls.__name__}')
        del self.bot

    def test_1_logging(self):
        self.assertEqual(self.bot.login, "Success")




