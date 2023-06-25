from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_chrome = webdriver.Chrome(ChromeDriverManager().install())
login = "kacper.trzepiecinski@hsswork.pl"
password = "KAcper2022!"
id = "415"
candidate_url = "https://hsswork.traffit.com/#/employees/employee/"


def login_to_traffit(driver, login, password):
    driver_chrome.get("https://hsswork.traffit.com")
    driver.find_element(By.ID, "username").send_keys(login)
    time.sleep(2)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password")
    time.sleep(2)
    driver.find_element(
        By.XPATH, "/html/body/div/div[2]/div/div[1]/div[1]/form/div[3]/button"
    ).click()
    time.sleep(2)


def get_id_of_all_candidates(
    driver=driver_chrome, login=login, password=password, project_id=id
):
    login_to_traffit(
        driver=driver,
        login=login,
        password=password,
    )

    driver.get(f"https://hsswork.traffit.com/#/recruitments/recruitment/{project_id}")

    time.sleep(5)

    cards = driver.find_elements(By.XPATH, "//div[@class='sc-fEVxLL fgitZN']")
    candidates_id = list()
    for i in range(len(cards)):
        card = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"(//div[@class='sc-fEVxLL fgitZN'])[{i + 1}]")
            )
        )
        driver.execute_script("arguments[0].click();", card)
        id = driver.current_url.split("/")[-1]
        candidates_id.append(id)

        WebDriverWait(driver_chrome, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='stage-prev__header--align-center stage-prev__header--el "
                    "stage-prev__header--el-close']",
                )
            )
        ).click()

    return candidates_id


def get_stages_history(candidate_id):
    output = {key: [] for key in candidate_id}
    for id in candidate_id:
        driver_chrome.get(candidate_url + id)
        driver_chrome.refresh()

        while True:
            try:
                button = WebDriverWait(driver_chrome, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'button[data-track="Timeline-LoadMore"]')
                    )
                )
                button.click()
                time.sleep(2)
            except:
                break

        time.sleep(2)

        containers = driver_chrome.find_elements(
            By.XPATH, "//div[@class='sc-czShuu eDgyIB']"
        )
        stages_containters = [
            con
            for con in containers
            if con.find_element(By.XPATH, "//div[@class='sc-jwBhTO bUsgEG']")
        ]
        stages_label = [
            el.find_element(By.XPATH, "//div[@class='sc-jwBhTO bUsgEG']").text
            for el in stages_containters
        ]
        stages_project_name = [
            el.find_element(By.XPATH, "//div[@class='sc-jNXgPE iEtfWf']").text
            for el in stages_containters
        ]
        print(stages_project_name)
        # for label, projet_name in zip(stages_label, stages_project_name):
        #     print(label.split("→")[0].replace("\n", ''), label.split("→")[1].replace("\n", ''), projet_name.replace("\n", ''), "\n----")
        break

        # timeline = WebDriverWait(driver_chrome, 10).until(
        #         EC.visibility_of_element_located((By.XPATH, "//div[@class='sc-liaBrn gTpfqt']"))
        #     )
        #
        # stages = [el.text for el in timeline.find_elements(By.XPATH, "//div[@class='sc-jwBhTO bUsgEG']")]
        #
        # to_add = [(el.split("→")[0].replace("\n", ''), el.split("→")[1].replace("\n", '')) for el in
        #           stages]
        #
        # output[id] = to_add

    return output


ids = get_id_of_all_candidates()
print(get_stages_history(ids))
