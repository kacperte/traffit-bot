from agents.traffit_bot import TraffitBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os


class TestTraffitBot(TraffitBot):
    def __init__(self, login, password):
        super(TestTraffitBot, self).__init__(login, password)
        self.login = login
        self.password = password
        self.random_project_id = None
        print("__Start Testing__")

    def test_logging_to_traffit(self):
        try:
            self.login_to_traffit()
            self.driver.delete_all_cookies()
            print("#Logging To Traffit__Success__")
        except Exception as e:
            print(f"{e} #Logging To Traffit__Error__")

    def test_get_id_of_all_actvie_project(self):
        try:
            output = self.get_id_of_all_actvie_project()
            self.random_project_id = output[0]
            if type(output) == list and len(output) > 0:
                self.driver.delete_all_cookies()
                print("#Get Id Of All Active Project__Success__")
            else:
                print("#Get Id Of All Active Project__Problem__")
        except Exception as e:
            print(f"{e} #Get Id Of All Active Project__Error__")

    def test_kanbans_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}")

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-jOhDuK"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Kanbas Class Name__Success__")
            else:
                print("#Kanbas Class Name__Problem__")
        except Exception as e:
            print(f"{e} #Kanbas Class Name__Error__")

    def test_candidate_card_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}")

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-jIAOiI"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Candidate Card Class Name__Success__")
            else:
                print("#Candidate Card Name__Problem__")
        except Exception as e:
            print(f"{e} #Candidate Card Name__Error__")

    def test_candidate_name_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}")

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-bgrGEg"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Candidate Name Class Name__Success__")
            else:
                print("#Candidate Name Name__Problem__")
        except Exception as e:
            print(f"{e} #Candidate Name Name__Error__")

    def test_candidate_days_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}")

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-erPKsr"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Candidate Days Class Name__Success__")
            else:
                print("#Candidate Days Name__Problem__")
        except Exception as e:
            print(f"{e} #Candidate Days Name__Error__")

    def test_entire_class(self):
        try:
            output = self.get_info_about_all_active_project()
            if type(output) == list and len(output) > 0:
                self.driver.delete_all_cookies()
                print("#Entire Project__Success__")
            else:
                print("#Candidate Days Name__Problem__")
        except Exception as e:
            print(f"{e} #Candidate Days Name__Error__")

    def main(self):
        self.test_logging_to_traffit()
        self.test_get_id_of_all_actvie_project()
        self.test_kanbans_class_name()
        self.test_candidate_card_class_name()
        self.test_candidate_name_class_name()
        self.test_candidate_days_class_name()
        self.test_entire_class()
        print("__End Testing__")


if __name__ == '__main__':
    TestTraffitBot(
        login=os.environ.get("LOGIN"),
        password=os.environ.get("PASSWORD")
    ).main()
