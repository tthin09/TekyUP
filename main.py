from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# userdata
data = {
    "student_name": 'Phan Quốc Hưng',
    "username": "84937285555",
    "password": "Teky@123"
}

driver.get("https://teky.edu.vn/")

driver.find_element(By.CSS_SELECTOR, "a.btn.btn-cmn.btn-login").click()

username_element = driver.find_element(By.ID, "user_username")
username_element.send_keys(data["username"])

password_element = driver.find_element(By.ID, "user_password")
password_element.send_keys(data["password"])

login_button = driver.find_element(By.XPATH, """//*[@id="devise_sign_in_form"]/input[2]""")
login_button.click()

#student_choose_area = driver.find_element()
select_student_path = f"/html/body/div[2]/div/div/div[2]/form/div/div[1]"
select_student_button = driver.find_element(By.XPATH, select_student_path)
print(select_student_button.get_attribute("innerHTML"))
# for i in range(10):
#     select_student_button.click()
#     time.sleep(0.5)


time.sleep(120)

driver.quit()