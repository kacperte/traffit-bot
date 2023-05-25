from agents.traffit_bot import TraffitBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mail_adapter.mail_connector import MailAdapter
from mail_adapter.messages_parser import TestsAlert
import os
import datetime


class TestTraffitBot(TraffitBot):
    def __init__(self, login, password):
        super(TestTraffitBot, self).__init__(login, password)
        self.login = login
        self.password = password
        self.random_project_id = None
        print("__Start Testing__")
        self.tests_output = {
            "logging_to_traffit": False,
            "get_id_of_all_active_project": False,
            "kanbas_class_name": False,
            "candidate_card_class_name": False,
            "candidate_name_class_name": False,
            "candidate_days_class_name": False,
            "etntire_class": False,
        }

    def test_logging_to_traffit(self):
        try:
            self.login_to_traffit()
            self.driver.delete_all_cookies()
            print("#Logging To Traffit__Success__")
            self.tests_output["logging_to_traffit"] = True
        except Exception as e:
            print(f"{e} #Logging To Traffit__Error__")

    def test_get_id_of_all_actvie_project(self):
        try:
            output = self.get_id_of_all_actvie_project()  # !
            self.random_project_id = output[0]
            if type(output) == list and len(output) > 0:
                self.driver.delete_all_cookies()
                print("#Get Id Of All Active Project__Success__")
                self.tests_output["get_id_of_all_active_project"] = True
            else:
                print("#Get Id Of All Active Project__Problem__")
        except Exception as e:
            print(f"{e} #Get Id Of All Active Project__Error__")

    def test_kanbans_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(
                f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}"
            )

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-hlnMnd"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Kanbas class Name__Success__")
                self.tests_output["kanbas_class_name"] = True
            else:
                print("#Kanbas Class Name__Problem__")
        except Exception as e:
            print(f"{e} #Kanbas Class Name__Error__")

    def test_candidate_card_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(
                f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}"
            )

            elements = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-cQIpJi fAgqyp"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Candidate Card Class Name__Success__")
                self.tests_output["candidate_card_class_name"] = True
            else:
                print("#Candidate Card Name__Problem__")
        except Exception as e:
            print(f"{e} #Candidate Card Name__Error__")

    def test_candidate_name_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(
                f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}"
            )

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-VcoSR"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Candidate Name Class Name__Success__")
                self.tests_output["candidate_name_class_name"] = True
            else:
                print("#Candidate Name Name__Problem__")
        except Exception as e:
            print(f"{e} #Candidate Name Name__Error__")

    def test_candidate_days_class_name(self):
        try:
            self.login_to_traffit()
            self.driver.get(
                f"https://hsswork.traffit.com/#/recruitments/recruitment/{self.random_project_id}"
            )

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-goMRkL"))
            )
            if elements:
                self.driver.delete_all_cookies()
                print("#Candidate Days Class Name__Success__")
                self.tests_output["candidate_days_class_name"] = True
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
                self.tests_output["etntire_class"] = True
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
        return self.tests_output


if __name__ == "__main__":
    output = TestTraffitBot(
        login=os.environ.get("LOGIN"), password=os.environ.get("PASSWORD")
    ).main()

    msg = TestsAlert()
    mailer = MailAdapter(
        host="poczta23110.e-kei.pl",
        port=465,
        username=os.getenv("L_MAIL"),
        password=os.getenv("P_MAIL"),
    )

    mailer.send_mail(
        recipient_email="kacper.trzepiecinski@hsswork.pl",
        subject="Status testów",
        content=msg.render(
            name="Kacper", content=output, date=datetime.datetime.now().date()
        ),
    )
