from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

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


def format_date(date_string):
    polish_to_english_months = {
        'stycznia': 'January',
        'lutego': 'February',
        'marca': 'March',
        'kwietnia': 'April',
        'maja': 'May',
        'czerwca': 'June',
        'lipca': 'July',
        'sierpnia': 'August',
        'września': 'September',
        'października': 'October',
        'listopada': 'November',
        'grudnia': 'December',
    }

    for polish, english in polish_to_english_months.items():
        date_string = date_string.replace(polish, english)

    date = datetime.strptime(date_string, '%A, %d %B %Y')

    return date.strftime('%d/%m/%Y')


def get_stages_history(candidate_id):
    data = {key: [] for key in candidate_id}
    for id in candidate_id:
        driver_chrome.get(candidate_url + id)
        driver_chrome.refresh()

        candidate_name = WebDriverWait(driver_chrome, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="info__primary-info"]')
            )
        ).text

        while True:
            try:
                button = WebDriverWait(driver_chrome, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'button[data-track="Timeline-LoadMore"]')
                    )
                )
                button.click()
            except:
                break

        timeline = driver_chrome.find_element(By.XPATH, "//div[@class='sc-liaBrn gTpfqt']")
        all_divs = timeline.find_elements(By.XPATH, "./div")
        results = []
        current_date = None

        for div in all_divs:
            class_name = div.get_attribute("class")
            if class_name == "sc-hpDagy jOmuKE":
                current_date = div.text
                continue

            if div.find_elements(By.XPATH, ".//div[@class='sc-jwBhTO bUsgEG']"):
                stage_labels = div.find_element(By.XPATH, ".//div[@class='sc-jwBhTO bUsgEG']").text.split("→")
                project_info = div.find_element(By.XPATH, ".//div[@class='sc-jNXgPE iEtfWf']").text.split("\n")

                result = {
                    'candidate_name': candidate_name,
                    'date': format_date(current_date),
                    'from': stage_labels[0].replace("\n", ""),
                    'to': stage_labels[1].replace("\n", ""),
                    'project_name': project_info[0].replace("(", "").replace(")", ""),
                    'client': project_info[1]
                }

                results.append(result)

        data[id] = results

    return data


ids = get_id_of_all_candidates()
print(get_stages_history(ids))
