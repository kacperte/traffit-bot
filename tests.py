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

    def test_get_info_about_all_active_project(self):
        self.assertEqual(type(self.bot.get_info_about_all_active_project()), list)


if __name__ == '__main__':
    result = unittest.main().result.wasSuccessful()



