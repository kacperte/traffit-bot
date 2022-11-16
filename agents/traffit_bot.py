from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import re
import os


class TraffitBot:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.driver = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options
        )
        self.action = webdriver.ActionChains(self.driver)
        self.BASE_URL = "https://hsswork.traffit.com/"
        self.ALL_PROJECT_URL = "https://hsswork.traffit.com/#/recruitments/all/1"
        self.PROJECT_URL = "https://hsswork.traffit.com/#/recruitments/recruitment/"

    def login_to_traffit(self):
        self.driver.get(self.BASE_URL)
        time.sleep(2)
        self.driver.find_element(By.ID, "username").send_keys(self.login)
        time.sleep(2)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "password")
        time.sleep(2)
        self.driver.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div[1]/div[1]/form/div[3]/button"
        ).click()
        time.sleep(2)
        self.driver.get(self.ALL_PROJECT_URL)
        time.sleep(2)

    def get_id_of_all_actvie_project(self):
        self.login_to_traffit()
        projects_id = []
        try:
            pages_nav = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="recruitments_all"]/div[2]/div[1]/div[2]/div/div/div/div[2]/div[2]/table/tbody[11]/tr/td/div[2]/div',
                        )
                    )
                )
                .text.split(" ")
            )
        except NoSuchElementException:
            raise "We can not located this element. Try again."

        for i in pages_nav:
            self.driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f'//*[@id="recruitments_all"]/div[2]/div[1]/div[2]/div/div/div/div[2]/div[2]/table/tbody[11]/tr/td/div[2]/div/div[{i}]',
                        )
                    )
                ),
            )
            time.sleep(3)
            recruitment_projects = self.driver.find_elements(
                By.XPATH,
                "//div[@class='actions__action datagrid-checkbox ng-scope']/input",
            )
            for project in recruitment_projects:
                id_attribute = project.get_attribute("id")
                project_id = re.search("\d{2,3}", id_attribute).group()
                projects_id.append(project_id)
        return projects_id

    def get_info_about_project(self, id):
        # Open recruitment project
        self.driver.get(f"https://hsswork.traffit.com/#/recruitments/recruitment/{id}")
        # Locate details page button and click it
        try:
            details = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Szczegóły')]")
                )
            )
            self.driver.execute_script("arguments[0].click();", details)

        except NoSuchElementException:
            raise "We can not located details page element. Try again."

        except TimeoutException:
            raise "Loading details page element took too much time!"
        # Locate project owner info
        try:
            owner = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//div[@class='recruitment-owner-item ng-binding ng-scope']",
                        )
                    )
                )
                .text
            )

        except NoSuchElementException:
            raise "We can not located project owner element. Try again."

        except TimeoutException:
            raise "Loading project owner element took too much time!"
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
            raise "We can not located project info element. Try again."

        except TimeoutException:
            raise "Loading project info element took too much time!"

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
            raise "We can not located pipeline page button. Try again."

        except TimeoutException:
            raise "Loading pipeline page button took too much time!"
        self.driver.refresh()
        while True:
            new_stages = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-TRNrF"))
            )[0]
            num_of_candidates_in_stages = new_stages.find_elements(
                By.CLASS_NAME, "sc-jIAOiI"
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
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-TRNrF"))
                )[0]
                .find_elements(By.CLASS_NAME, "sc-jIAOiI")
            ):
                num_of_candidates_in_stages = new_stages.find_elements(
                    By.CLASS_NAME, "sc-jIAOiI"
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", num_of_candidates_in_stages[-1]
                )
                time.sleep(5)
            else:
                break
        while True:
            screen_stages = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-TRNrF"))
            )[1]
            num_of_candidates_in_stages = screen_stages.find_elements(
                By.CLASS_NAME, "sc-jIAOiI"
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
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-TRNrF"))
                )[0]
                .find_elements(By.CLASS_NAME, "sc-jIAOiI")
            ):
                num_of_candidates_in_stages = screen_stages.find_elements(
                    By.CLASS_NAME, "sc-jIAOiI"
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", num_of_candidates_in_stages[-1]
                )
                time.sleep(5)
            else:
                break
            break

        # Locate project stages kanbans
        try:
            stages = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-TRNrF"))
            )

        except NoSuchElementException:
            raise "We can not located project stages kanbans. Try again."

        except TimeoutException:
            raise "Loading project stages kanbans took too much time!"

        # Left only "New" and "Screen" stages
        new_stages, screen_stages = stages[0], stages[1]

        output = {
            "Project Owner": owner,
            "Project": project_name,
            "Client": project_client,
            "Project ID": id,
            "Candidate": dict(),
        }

        for candidate, days in zip(
            new_stages.find_elements(By.CLASS_NAME, "sc-zsjhC"),
            new_stages.find_elements(By.CLASS_NAME, "sc-eoXOpV"),
        ):
            if self.does_it_need_feedback(days.text):
                output["Candidate"].update({candidate.text: days.text})

        for candidate, days in zip(
            screen_stages.find_elements(By.CLASS_NAME, "c-zsjhC"),
            screen_stages.find_elements(By.CLASS_NAME, "sc-eoXOpV"),
        ):
            if self.does_it_need_feedback(days.text):
                output["Candidate"].update({candidate.text: days.text})
        return output

    def get_info_about_all_active_project(self):
        final_info = list()
        for id in self.get_id_of_all_actvie_project():
            project_info = self.get_info_about_project(id)
            if project_info["Candidate"]:

                final_info.append(project_info)
            self.driver.refresh()

        return final_info

    @staticmethod
    def does_it_need_feedback(days):
        if len(days.split()) == 1:
            return False
        if int(days.split()[0]) >= 5:
            return True
        else:
            return False
