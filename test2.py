import time
from selenium import  webdriver
from selenium.webdriver.common.by import  By
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
today_staff = {}
CHROME_DRIVER_PATH = "C:\Work\Development\chromedriver.exe"

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.set_window_size(1920,1080)
driver.get(url="https://connect.treatwell.co.uk/login?route=%2Fcalendar%23venue%2F370180%2Fappointment%2Fday%2F2022-04-27%2F398937")
time.sleep(2)
email_path = driver.find_element(by=By.XPATH,value='//*[@id="login-page"]/div/div[2]/div[1]/form/div[1]/div/div/input')
password_path = driver.find_element(by=By.XPATH,value='//*[@id="login-page"]/div/div[2]/div[1]/form/div[2]/div/div/input')
email_path.send_keys(EMAIL)
password_path.send_keys(PASSWORD)
log_in_btn = driver.find_element(by=By.XPATH,value='//*[@id="login-page"]/div/div[2]/div[1]/form/button')
log_in_btn.click()
time.sleep(5)
jahan = driver.find_element(by=By.CSS_SELECTOR,value='#bcalendar-inst > div > div.wc-status-slots-container > div > table > tbody > tr.wc-day-column-container > td.wc-day-column.day-10 > div > div:nth-child(13)')
time.sleep(2)
jahan.click()
time.sleep(2)
name = jahan.find_element(by=By.XPATH,value='//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/form/div[2]/div[2]/div[2]/div[6]/div/div/div[1]/div/div/div/div')
print(name)
#react-root > div > div > div > div.ui-dialog.dialog2.react-dialog.calendar-item-editor.top > div > div > div:nth-child(3) > div > div > div.content-scroll > div.js-appointments.udv-appointments > div:nth-child(1) > form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div:nth-child(1) > div.appointment--content--item.float.for-max-select.js-employee.right > div > div > div.InputBorder--container--3f2d33 > div > div > div > div
#react-root > div > div > div > div.ui-dialog.dialog2.react-dialog.calendar-item-editor.top > div > div > div:nth-child(3) > div > div > div.content-scroll > div.js-appointments.udv-appointments > div:nth-child(1) > form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div:nth-child(2) > div.appointment--content--item.float.for-max-select.js-employee.right > div > div > div.InputBorder--container--3f2d33 > div > div > div > div
                          #react-root > div > div > div > div.ui-dialog.dialog2.react-dialog.calendar-item-editor.top > div > div > div:nth-child(3) > div > div > div.content-scroll > div.js-appointments.udv-appointments > div > form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div > div.appointment--content--item.float.for-max-select.js-employee.right > div > div > div.InputBorder--container--3f2d33 > div > div > div > div
#//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/form/div[2]/div[2]/div[1]/div[6]/div/div/div[1]/div/div/div/div
#//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/form/div[2]/div[2]/div[2]/div[6]/div/div/div[1]/div/div/div/div

#//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div[1]/form/div[2]/div[2]/div[1]/div[6]/div/div/div[1]/div/div/div/div
#//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div[1]/form/div[2]/div[2]/div[2]/div[6]/div/div/div[1]/div/div/div/div
#//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div   /form/div[2]/div[2]/div/div[5]/div/div/div[1]/div/div/div/div