from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# userdata
df = pd.read_excel("student.xlsx", sheet_name="student_info")
data = df.to_dict(orient='records')

def is_logged_in():
    # if there is a login button, then we haven't logged in yet
    try:
        login_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-cmn.btn-login")
        return False
    except:
        return True
    
# check if student have already uploaded that project
def uploaded_project():
    try:
        image_uploaded_section = driver.find_element(By.XPATH, "//*[normalize-space()='Hình ảnh sản phẩm']")
        return True
    except:
        return False

def logout():
    try:
        profile_info_click = driver.find_element(By.XPATH, "//*[@id='header']/div[2]/div[2]/div/div[1]/div/figure/a").click()
        logout_click = driver.find_element(By.XPATH, "//*[@id='header']/div[2]/div[2]/div/div[2]/ul[2]/li[5]/a").click()
    except:
        print("User haven't logged in yet")

def go_home_screen():
    time.sleep(1)
    driver.get("https://teky.edu.vn/")
    
def go_login_page():
    login_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-cmn.btn-login"))
    )
    login_button.click()
    
    # find if we have to click 'Sử dụng tài khoản khác'
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".b-grid__title.choose_account__link"))
        )
        new_account_button = driver.find_element(By.XPATH, "//a[.//text()[contains(normalize-space(), 'Sử dụng tài khoản khác')]]")
        new_account_button.click()
        print("Clicked 'Choose other account' button")
    except:
        print("Didn't find 'Choose other account' button")

# From home screen to Log in
def login(username, password):
    username_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "user_username"))
    )
    username_element.send_keys(username)

    password_element = driver.find_element(By.ID, "user_password")
    password_element.send_keys(password)

    login_button = driver.find_element(By.XPATH, """//*[@id="devise_sign_in_form"]/input[2]""")
    login_button.click()

# Choose student
def choose_student(student_name):
    parent_button = driver.find_element(By.XPATH, f"//div[@class='groupItems b-student__item'][.//h3[normalize-space()='{student_name}']]/div/div/div/div[3]")
    select_student_button = parent_button.find_element(By.TAG_NAME, "svg")
    select_student_button.click()
    continue_sign_in = driver.find_element(By.ID, "btn-submit-choose-student")
    continue_sign_in.click()

# Choose course
def choose_course(course_name):
    course_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f"//div[@class='c-content-myclass__detail' and @data-course='{course_name}']"))
    )
    course_button.click()

# Choose lesson
def choose_lesson(level, lesson_num):
    lesson_num = int(lesson_num)
    level_div = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'c-timeline-lesson__item')][.//span[normalize-space()='Học phần {level}']]/div[2]/ul/li[{lesson_num}]/div/a"))
    )
    level_div.click()

def upload_project(image_name):
    if uploaded_project():
        print("Project uploaded")
        return
    else:
        print("Project isn't uploaded yet")
    # Go to project session
    upload_project_session = WebDriverWait(driver, 15).until( 
        EC.presence_of_element_located((By.XPATH, "//*[@id='sesison_projects_link_tab']"))
    )
    upload_project_session.click()

    # Fill title and description
    title_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/b/span[2]"))
    ).text
    description_text = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/ul/div/p[2]").text
    print(f"Before: {description_text}")
    while len(description_text) <= 50: # description must have more than 50 char
        description_text = description_text + "\r" + description_text
    print(f"After: {description_text}")

    title_element = driver.find_element(By.XPATH, "//*[@id='js-countformtext']")
    title_element.send_keys(title_text)
    description_element = driver.find_element(By.XPATH, "//*[@id='form_upload_project']/div[3]/trix-editor")
    description_element.send_keys(description_text)

    image_rel_path = "images/" + image_name
    image_abs_path = os.path.abspath(image_rel_path)
    image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='form_upload_project']/div[4]/a/input"))
    )
    image_element.send_keys(image_abs_path)
    
    # click upload
    upload_button = driver.find_element(By.XPATH, "//*[@id='button_create_project_form']")
    #upload_button.click()
    
def main_upload():
    print("\nBắt đầu đăng sản phẩm học sinh...")
    for student_data in data[::-1]:
        go_home_screen()
        logout()
        go_login_page()
        login(student_data['username'], student_data['password'])
        choose_student(student_data['student_name'])
        choose_course(student_data['course'])
        choose_lesson(student_data['level'], student_data['lesson_num'])
        upload_project(student_data['image_name'])
        
def tutorial():
    print("Hãy đọc hướng dẫn trong file README.md")
    have_filled_info = ''
    while have_filled_info.lower() not in ['y', 'yes']:
        have_filled_info = input("1. Bạn đã điền đầy đủ thông tin của học sinh trong file student.xlsx chưa? (Y/N): ")
    have_uploaded_image = ''
    while have_uploaded_image.lower() not in ['y', 'yes']:
        have_uploaded_image = input("2. Bạn đã bỏ hình ảnh sản phẩm vào thư mục images chưa? (Y/N): ")
    have_checked_image_name = ''
    while have_checked_image_name.lower() not in ['y', 'yes']:
        have_checked_image_name = input("3. Kiểm tra lại xem tên hình ảnh trong file student.xlsx đã giống với tên hình ảnh trong thư mục images chưa? (Y/N): ")
    return True
    
def main():
    tutorial()
    main_upload()

if __name__ == "__main__":
    main()

time.sleep(200)
driver.quit()