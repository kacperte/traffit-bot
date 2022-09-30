from agents.traffit_bot import TraffitBot
import os


class TestTraffitBot(TraffitBot):
    def __init__(self, login, password):
        super(TestTraffitBot, self).__init__(login, password)
        self.login = login
        self.password = password

    def test_login(self):
        try:
            self.login_to_traffit()
            print("#Login success")
        except Exception as e:
            print(f"{e} #Login error")

    def main(self):
        self.test_login()


if __name__ == '__main__':
    TestTraffitBot(
        login=os.environ.get("LOGIN"),
        password=os.environ.get("PASSWORD")
    ).main()
