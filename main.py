import json
import time
from selenium import  webdriver
from selenium.webdriver.common.by import  By
import os


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CHROME_DRIVER_PATH = "C:\Work\Development\chromedriver.exe"

today_staffs = {}
today_staffs["staffs"] = {}
today_staff = today_staffs["staffs"]
counter = 0

def opening_chrome_window(userUrl):

    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    driver.set_window_size(1920,1080)
    driver.get(url=userUrl)
    time.sleep(2)
    return driver
def sign_in_to_treatwell():
    email_path = driver.find_element(by=By.XPATH,
                                     value='//*[@id="login-page"]/div/div[2]/div[1]/form/div[1]/div/div/input')
    password_path = driver.find_element(by=By.XPATH,
                                        value='//*[@id="login-page"]/div/div[2]/div[1]/form/div[2]/div/div/input')
    email_path.send_keys(EMAIL)
    password_path.send_keys(PASSWORD)
    log_in_btn = driver.find_element(by=By.XPATH, value='//*[@id="login-page"]/div/div[2]/div[1]/form/button')
    log_in_btn.click()
    time.sleep(5)

def get_date_from_treatwell():
    date = driver.find_element(by=By.XPATH,value='//*[@id="calendar-holder"]/div[2]/div[1]/div[1]/div[3]/div/ul/li[2]/span')
    today_staffs["date"] = date.text
def get_all_staffs_name_from_treatwell():
    staff_name_lists = driver.find_elements(by=By.XPATH,value='//*[@id="bcalendar-inst"]/div/div[1]/table/tbody/tr/td')
    for staff in staff_name_lists:
        class_name = staff.get_attribute("class")

        if staff.text != ' ':
            if staff.text != '':
                index = int(class_name.split(" ")[1].split("-")[2])
                split_name_arr = staff.text.split("\n")
                if(len(split_name_arr)>1):
                    staff_name = staff.text.split("\n")[1]
                    today_staff[f"{index}"] = {
                        "name" : staff_name,
                        "bookings":[]
                    }
                else:
                    staff_name = staff.text.split("\n")[0]
                    today_staff[f"{index}"] = {
                        "name": staff_name,
                        "bookings": []
                    }

def saveResultToFile():
    with open(f"{today_staffs['date']}.json","w") as data_file:
        json.dump(today_staffs,data_file,indent=4)
    # print(today_staff)
    print("Done")
# https://connect.treatwell.co.uk/calendar#venue/370180/appointment/day/2022-06-15/199300
#https://connect.treatwell.co.uk/login?route=%2Fcalendar%23venue%2F370180%2Fappointment%2Fday%2F2022-05-01%2F398937
driver = opening_chrome_window("https://connect.treatwell.co.uk/calendar#venue/370180/appointment/day/2022-06-29/199300")
sign_in_to_treatwell()
staff_bookings_lists = driver.find_elements(by=By.XPATH, value='//*[@id="bcalendar-inst"]/div/div[2]/div/table/tbody/tr[2]/td')
get_date_from_treatwell()
get_all_staffs_name_from_treatwell()

for staff_col in staff_bookings_lists:
    bookings = staff_col.find_elements(by=By.CLASS_NAME,value='wc-cal-event')
    if bookings!=[]:
        print(bookings)
        for appointment in bookings:
            if appointment.text != "":
                customer_booking_data_list = appointment.text.split("\n")
                appointment.click()
                time.sleep(2)
                customer_pop_up_treatments_lists = driver.find_elements(by=By.XPATH,value='//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div')
                for treatment in customer_pop_up_treatments_lists:
                    name = treatment.find_element(by=By.CSS_SELECTOR,value='form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div > div.appointment--content--item.float.for-max-select.js-employee.right > div > div > div.InputBorder--container--3f2d33 > div > div > div > div')
                    if today_staff[f'{counter}']["name"] in name.text:
                        customer_booking_dict = {}
                        customer_name_obj = treatment.find_element(by=By.XPATH,value='//*[@id="react-root"]/div/div/div/div[2]/div/div/div[1]')
                        start_time_obj = treatment.find_element(by=By.CSS_SELECTOR,value='form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div > div.appointment--content--item.float.for-small-select.no-label.js-startTime.is-react > div > div.InputBorder--container--3f2d33 > div > div > div > div')
                        end_time_obj = treatment.find_element(by=By.CSS_SELECTOR,value='form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div > div.appointment--content--item.clear.extra-padding > span > span')
                        customer_booking_dict["time"] = f"{start_time_obj.text} - {end_time_obj.text}"
                        treatment_type = treatment.find_element(by=By.CSS_SELECTOR,value='form > div.appointment--item--content.clearfix > div.appointment--content--item')
                        price = treatment.find_element(by=By.CSS_SELECTOR,value='form > div.appointment--item--footer.clearfix > span > span')
                        personOrTreatwellBook = treatment.find_element(by=By.CSS_SELECTOR,value='div > div > div.content-scroll > div.js-appointments.udv-appointments > div > form > div.appointment--source')
                        paidOrUnpaid = treatment.find_element(by=By.CSS_SELECTOR,value='form > div.appointment--item--footer.clearfix > span')
                        # react-root > div > div > div > div.ui-dialog.dialog2.react-dialog.calendar-item-editor.top > div > div > div:nth-child(3) > div > div > div.content-scroll > div.js-appointments.udv-appointments > div > form > div.appointment--item--footer.clearfix > span
                        # react-root > div > div > div > div.ui-dialog.dialog2.react-dialog.calendar-item-editor.top > div > div > div:nth-child(3) > div > div > div.content-scroll > div.js-appointments.udv-appointments > div:nth-child(2) > form > div.appointment--item--footer.clearfix > span
                        note_container = treatment.find_element(by=By.CSS_SELECTOR, value='form > div.js-notes.textarea-container')
                        customer_booking_dict["note"] = note_container.text
                        customer_booking_dict["price"] = price.text.strip("£")
                        customer_booking_dict["treatment"] = treatment_type.text.split("\n")[0]
                        customer_booking_dict["personOrTreatwellBook"] = personOrTreatwellBook.text
                        customer_booking_dict["paidOrUnpaid"] = paidOrUnpaid.text.replace("£",'')
                        try:
                            duration_obj = treatment.find_element(by=By.CSS_SELECTOR,value='form > div.appointment--item--content.clearfix > div.appointment--content--item > div.js-skuId.extra-top-margin.is-react > div')
                            customer_booking_dict["duration"] = duration_obj.text
                        except:
                            customer_booking_dict["duration"] = "Invalid"
                        if customer_booking_dict not in today_staff[f'{counter}']['bookings']:
                            today_staff[f'{counter}']['bookings'].append(customer_booking_dict)
                        print(f'This is {name.text}')
                close_pop_up_btn = driver.find_element(by=By.XPATH,value='//*[@id="react-root"]/div/div/div/div[2]/div/div/span')
                close_pop_up_btn.click()
                print(today_staff)
                time.sleep(2)


    counter+=1

#react-root > div > div > div > div.ui-dialog.dialog2.react-dialog.calendar-item-editor.top > div > div > div:nth-child(3) > div > div > div.content-scroll > div.js-appointments.udv-appointments > div > form > div.appointment--source
#react-root > div > div > div > div.ui-dialog.dialog2.react-dialog.calendar-item-editor.top > div > div > div:nth-child(3) > div > div > div.content-scroll > div.js-appointments.udv-appointments > div > form > div.appointment--source
saveResultToFile()

# driver.close()