import json
import time

from selenium import  webdriver
from selenium.webdriver.common.by import  By
import os
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CHROME_DRIVER_PATH = "C:\Work\Development\chromedriver.exe"
class TreatwellDriver():
    def __init__(self):
        self.chromedriver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

    def generate_single_day_report(self,url):
        while True:
            try:
                self.chromedriver.set_window_size(1920, 1080)
                self.chromedriver.get(url)
                self.today_staff = {}
                self.staffs_booking_lists = []
                time.sleep(2)
                self.log_in_to_treatwell()
                self.get_all_treament_lists()
                self.get_date_from_treatwell()
                self.get_staff_names_from_treatwell()
                self.generate_today_treatments_data()
                self.save_current_staff_info_to_json()
                break
            except Exception as e:
                print(e)
                print("Invalid error, trying again.")
        print("Job completed!")
    def generate_multiple_day_report(self, url_lists):
        for url in url_lists:
            self.generate_single_day_report(url)

    def log_in_to_treatwell(self):
        email_path = self.chromedriver.find_element(by=By.XPATH,value='//*[@id="login-page"]/div/div[2]/div[1]/form/div[1]/div/div/input')
        password_path = self.chromedriver.find_element(by=By.XPATH,
                                            value='//*[@id="login-page"]/div/div[2]/div[1]/form/div[2]/div/div/input')
        email_path.send_keys(EMAIL)
        password_path.send_keys(PASSWORD)
        log_in_btn = self.chromedriver.find_element(by=By.XPATH, value='//*[@id="login-page"]/div/div[2]/div[1]/form/button')
        log_in_btn.click()
        time.sleep(5)

    def get_all_treament_lists(self):
        self.staffs_booking_lists = self.chromedriver.find_elements(by=By.XPATH,
                                                    value='//*[@id="bcalendar-inst"]/div/div[2]/div/table/tbody/tr[2]/td')

    def get_date_from_treatwell(self):
        date = self.chromedriver.find_element(by=By.XPATH,
                                   value='//*[@id="calendar-holder"]/div[2]/div[1]/div[1]/div[3]/div/ul/li[2]/span')
        self.today_staff["date"] = date.text

    def get_staff_names_from_treatwell(self):
        self.staff_name_lists = self.chromedriver.find_elements(by=By.XPATH,
                                                value='//*[@id="bcalendar-inst"]/div/div[1]/table/tbody/tr/td')
        for staff in self.staff_name_lists:
            staff_class_name = staff.get_attribute("class")
            if staff.text != ' ' and staff.text!='':
                staff_column_position = int(staff_class_name.split(" ")[1].split("-")[2])
                staff_name = staff.text.split("\n")[1]
                self.today_staff[f"{staff_column_position}"] = {
                    "name": staff_name,
                    "bookings": []
                }
    def save_current_staff_info_to_json(self):
        with open(f"{self.today_staff['date']}.json", "w") as data_file:
            json.dump(self.today_staff, data_file, indent=4)
        print("Successfully saved to file.")
    def generate_today_treatments_data(self):
        counter =0
        for staff_col in self.staffs_booking_lists:
            bookings = staff_col.find_elements(by=By.CLASS_NAME, value='wc-cal-event')
            if bookings != []:
                for booking in bookings:
                    if booking.text != "":
                        booking.click()
                        time.sleep(2)
                        customer_pop_up_treatments_lists = self.chromedriver.find_elements(by=By.XPATH,
                                                                                value='//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div')
                        for treatment in customer_pop_up_treatments_lists:

                            name = treatment.find_elements(by=By.CSS_SELECTOR,value='form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div > div.appointment--content--item.float.for-max-select.js-employee.right > div > div > div.InputBorder--container--3f2d33 > div > div > div > div')
                            if name==[]:
                                name = treatment.find_element(by=By.XPATH,
                                                              value='//*[@id="react-root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/form/div[2]/div[2]/div[2]/div[6]/div/div/div[1]/div/div/div/div')
                            else:
                                name = name[0]
                            if self.today_staff[f'{counter}']["name"] in name.text:
                                treatment_dict = self.extract_treatment_detail_from_treatwell(treatment)
                                self.add_new_treatment_in_staff_data(treatment_dict,counter)
                                print(f'This is {name.text}')

                        self.find_and_close_pop_up_button()
                        time.sleep(2)

            counter += 1
    def add_new_treatment_in_staff_data(self,new_treatment_dict,counter):
        if (new_treatment_dict not in self.today_staff[f'{counter}']['bookings']):
            self.today_staff[f'{counter}']['bookings'].append(new_treatment_dict)
    def find_and_close_pop_up_button(self):
        close_pop_up_btn = self.chromedriver.find_element(by=By.XPATH,
                                                          value='//*[@id="react-root"]/div/div/div/div[2]/div/div/span')
        close_pop_up_btn.click()
    def extract_treatment_detail_from_treatwell(self,treatment):
        treatment_dict = {}
        customer_name_obj = treatment.find_element(by=By.XPATH,
                                                   value='//*[@id="react-root"]/div/div/div/div[2]/div/div/div[1]')
        #Need to fix this error for when there is two data on a single treatment.
        start_time_obj = treatment.find_element(by=By.CSS_SELECTOR,
                                                value='form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div > div.appointment--content--item.float.for-small-select.no-label.js-startTime.is-react > div > div.InputBorder--container--3f2d33 > div > div > div > div')
        end_time_obj = treatment.find_element(by=By.CSS_SELECTOR,
                                              value='form > div.appointment--item--content.clearfix > div.js-appointment-data-rows > div > div.appointment--content--item.clear.extra-padding > span > span')
        treatment_type = treatment.find_element(by=By.CSS_SELECTOR,
                                                value='form > div.appointment--item--content.clearfix > div.appointment--content--item')

        price = treatment.find_element(by=By.CSS_SELECTOR,
                                       value='form > div.appointment--item--footer.clearfix > span > span')
        note_container = treatment.find_element(by=By.CSS_SELECTOR,
                                                value='form > div.js-notes.textarea-container')
        treatment_dict["customer_name"] = customer_name_obj.text
        treatment_dict["time"] = f"{start_time_obj.text} - {end_time_obj.text}"
        treatment_dict["note"] = note_container.text
        treatment_dict["price"] = price.text
        treatment_dict["treatment"] = treatment_type.text.split("\n")[0]
        try:
            duration_obj = treatment.find_element(by=By.CSS_SELECTOR,
                                                  value='form > div.appointment--item--content.clearfix > div.appointment--content--item > div.js-skuId.extra-top-margin.is-react > div')
            treatment_dict["duration"] = duration_obj.text
        except:
            treatment_dict["duration"] = "Invalid"
        return treatment_dict