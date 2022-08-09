from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

DRIVER_PATH = r"C:\Users\kacpe\OneDrive\Pulpit\Python\Projekty\chromedriver.exe"
LOGIN = "kacper.trzepiecinski@hsswork.pl"
PASSWORD = "KAcper2016!"


class TraffitBot:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.action = webdriver.ActionChains(self.driver)
        self.BASE_URL = "https://hsswork.traffit.com/"
        self.ALL_PROJECT_URL = "https://hsswork.traffit.com/#/recruitments/all/1"
        self.PROJECT_URL = "https://hsswork.traffit.com/#/recruitments/recruitment/"

    def login_to_traffit(self):
        self.driver.get(self.BASE_URL)
        time.sleep(2)
        self.driver.find_element(By.ID, "username").send_keys(LOGIN)
        time.sleep(2)
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "password").send_keys("\n")
        time.sleep(2)
        self.driver.get(self.ALL_PROJECT_URL)

    def get_id_of_all_actvie_project(self):
        self.login_to_traffit()
        projects_id = []
        pages_nav = []
        try:
            pages_nav = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="recruitments_all"]/div[2]/div[1]/div[2]/div/div/div/div[2]/div[2]/table/tbody['
                            "11]/tr/td/div[2]/div",
                        )
                    )
                )
                .text.split(" ")
            )
        except NoSuchElementException:
            print("We can not located this element. Try again.")

        for i in pages_nav:
            self.driver.find_element(
                By.XPATH,
                f'//*[@id="recruitments_all"]/div[2]/div[1]/div[2]/div/div/div/div[2]/div[2]/table/tbody['
                f"11]/tr/td/div[2]/div/div[{i}] ",
            ).click()
            time.sleep(3)
            recruitment_projects = self.driver.find_elements(
                By.XPATH,
                "//div[@class='actions__action datagrid-checkbox ng-scope']/input",
            )

            for project in recruitment_projects:
                id_attribute = project.get_attribute("id")
                project_id = re.search("\d{1,2,3}", id_attribute).group()
                projects_id.append(project_id)

        return projects_id

    def get_info_about_project(self):
        # Log to Traffit account
        self.login_to_traffit()
        self.driver.get("https://hsswork.traffit.com/#/recruitments/recruitment/280")

        # Locate details page button and click it
        try:
            details = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Szczegóły')]")
                )
            )
            self.driver.execute_script("arguments[0].click();", details)

        except NoSuchElementException:
            print("We can not located details page element. Try again.")

        # Locate project owner info
        try:
            owner = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='pad-top-8 ng-binding']")
                    )
                )
                .text.split("-")[1]
                .strip()
            )

        except NoSuchElementException:
            print("We can not located project owner element. Try again.")

        # Locate project info (project name and client)
        try:
            project_info = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='traffit-h1']")
                    )
                )
                .text.split("\n")
            )

        except NoSuchElementException:
            print("We can not located project info element. Try again.")

        project_name, project_client = project_info[0], project_info[1]

        # Locate pipeline page button and click it
        try:
            pipeline = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Pipeline')]")
                )
            )
            self.driver.execute_script("arguments[0].click();", pipeline)

        except NoSuchElementException:
            print("We can not located details page element. Try again.")

        while True:
            new_stages = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-jONnzC"))
            )[0]
            num_of_candidates_in_stages = new_stages.find_elements(
                By.CLASS_NAME, "sc-eZuRTN"
            )
            if len(num_of_candidates_in_stages) <= 2:
                break
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", num_of_candidates_in_stages[-1]
            )
            time.sleep(5)

            if len(num_of_candidates_in_stages) != len(
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-jONnzC"))
                )[0]
                .find_elements(By.CLASS_NAME, "sc-eZuRTN")
            ):
                num_of_candidates_in_stages = new_stages.find_elements(
                    By.CLASS_NAME, "sc-eZuRTN"
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", num_of_candidates_in_stages[-1]
                )
                time.sleep(5)
            else:
                break

        while True:
            screen_stages = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-jONnzC"))
            )[1]
            num_of_candidates_in_stages = screen_stages.find_elements(
                By.CLASS_NAME, "sc-eZuRTN"
            )
            if len(num_of_candidates_in_stages) <= 2:
                break
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", num_of_candidates_in_stages[-1]
            )
            time.sleep(5)

            if len(num_of_candidates_in_stages) != len(
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-jONnzC"))
                )[0]
                .find_elements(By.CLASS_NAME, "sc-eZuRTN")
            ):
                num_of_candidates_in_stages = screen_stages.find_elements(
                    By.CLASS_NAME, "sc-eZuRTN"
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", num_of_candidates_in_stages[-1]
                )
                time.sleep(5)
            else:
                break
            break

        # Locate project stages kanbans
        stages = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-jONnzC"))
        )

        # Left only "Nowy" and "Screen" stages
        new_stages, screen_stages = stages[0], stages[1]

        output = {}

        for candidate, days in zip(
            new_stages.find_elements(By.CLASS_NAME, "sc-eZuRTN"),
            new_stages.find_elements(By.CLASS_NAME, "sc-bgXqIY"),
        ):
            output[candidate.text] = days.text

        for candidate, days in zip(
            screen_stages.find_elements(By.CLASS_NAME, "sc-eZuRTN"),
            screen_stages.find_elements(By.CLASS_NAME, "sc-bgXqIY"),
        ):
            output[candidate.text] = days.text

        print(f"{owner}\n{project_name}\n{project_client}\n{output}")


bot = TraffitBot(login=LOGIN, password=PASSWORD)
print(bot.get_info_about_project())
