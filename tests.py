import unittest
from agents.traffit_bot import TraffitBot
import os


class TestTraffitBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print(f'setting up class...{cls.__name__}')
        cls.bot = TraffitBot(login=os.environ.get("LOGIN"), password=os.environ.get("PASSWORD"))

    @classmethod
    def tearDownClass(cls) -> None:
        print(f'tearing down clas...{cls.__name__}')
        del cls.bot

    def test_1_logging(self):
        self.assertEqual(self.bot.login, "Success")





