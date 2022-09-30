from agents.traffit_bot import TraffitBot
import os


class TestTraffitBot(TraffitBot):
    def __init__(self, login, password):
        super(TestTraffitBot, self).__init__(login, password)
        self.login = login
        self.password = password

    def test_login_to_traffit(self):
        try:
            self.login_to_traffit()
            self.driver.close()
            print("#Login__Success__")
        except Exception as e:
            print(f"{e} #Login__Error__")

    def test_get_id_of_all_actvie_project(self):
        try:
            output = self.get_id_of_all_actvie_project()
            if type(output) == list and len(output) > 0:
                print("#Get Id Of All Active Project__Success__")
            else:
                print("#Get Id Of All Active Project__Problem__")
        except Exception as e:
            print(f"{e} #Get Id Of All Active Project__Error__")

    def main(self):
        self.test_login_to_traffit()
        self.test_get_id_of_all_actvie_project()


if __name__ == '__main__':
    TestTraffitBot(
        login=os.environ.get("LOGIN"),
        password=os.environ.get("PASSWORD")
    ).main()
