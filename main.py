from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# userdata
data = {
    "student_name": "Phan Quốc Hưng",
    "username": "84937285555",
    "password": "Teky@123",
    "course": "Bé làm Game",
    "level": "7",
    "lesson_num": 5,
}

driver.get("https://teky.edu.vn/")

# From home screen to Log in
driver.find_element(By.CSS_SELECTOR, "a.btn.btn-cmn.btn-login").click()

# Log in
username_element = driver.find_element(By.ID, "user_username")
username_element.send_keys(data["username"])

password_element = driver.find_element(By.ID, "user_password")
password_element.send_keys(data["password"])

login_button = driver.find_element(By.XPATH, """//*[@id="devise_sign_in_form"]/input[2]""")
login_button.click()

# Choose student
parent_button_path = f"//div[@class='groupItems b-student__item'][.//h3[normalize-space()='{data['student_name']}']]/div/div/div/div[3]"
parent_button = driver.find_element(By.XPATH, parent_button_path)
select_student_button = parent_button.find_element(By.TAG_NAME, "svg")
select_student_button.click()
continue_sign_in = driver.find_element(By.ID, "btn-submit-choose-student")
continue_sign_in.click()

# Choose course
course_button = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, f"//div[@class='c-content-myclass__detail' and @data-course='Bé làm Game']"))
)
course_button.click()

# Choose lesson
level_div = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'c-timeline-lesson__item')][.//span[normalize-space()='Học phần {data['level']}']]/div[2]/ul/li[{data['lesson_num']}]/div/a"))
)
level_div.click()

# Fill the lesson info

time.sleep(200)

driver.quit()