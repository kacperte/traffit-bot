import unittest
from agents.traffit_bot import TraffitBot
import os


class TestTraffitBot(unittest.TestCase):

    def setUp(self) -> None:
        print(f'setting up class...{cls.__name__}')
        bot = TraffitBot(login=os.environ.get("LOGIN"), password=os.environ.get("PASSWORD"))

    def tearDown(self) -> None:
        print(f'tearing down clas...{cls.__name__}')
        del self.bot



