from agents.traffit_bot import TraffitBot
from selenium.webdriver.common.by import By
import os


class TestTraffitBot(TraffitBot):
    def __init__(self, login, password):
        super(TestTraffitBot, self).__init__(login, password)
        self.login = login
        self.password = password
        self.random_project_id = None
        print("__Start Testing__")

    def test_login_to_traffit(self):
        try:
            self.login_to_traffit()
            self.driver.delete_all_cookies()
            print("#Login__Success__")
        except Exception as e:
            print(f"{e} #Login__Error__")

    def test_get_id_of_all_actvie_project(self):
        try:
            output = self.get_id_of_all_actvie_project()
            self.random_project_id = output[0]
            if type(output) == list and len(output) > 0:
                print("#Get Id Of All Active Project__Success__")
            else:
                print("#Get Id Of All Active Project__Problem__")
        except Exception as e:
            print(f"{e} #Get Id Of All Active Project__Error__")

    def test_kanbans_class_name(self):
        try:
            self.driver.get(f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}")
            elements = self.driver.find_element(By.CLASS_NAME, "sc-jOhDuK")
            if elements:
                print("#Kanbas Class Name__Success__")
            else:
                print("#Kanbas Class Name__Problem__")
        except Exception as e:
            print(f"{e} #Kanbas Class Name__Error__")

    def main(self):
        self.test_login_to_traffit()
        self.test_get_id_of_all_actvie_project()


if __name__ == '__main__':
    TestTraffitBot(
        login=os.environ.get("LOGIN"),
        password=os.environ.get("PASSWORD")
    ).main()
