from treatwelldriver import TreatwellDriver
date_to_generate_report = [
    "2022-04-27",
    "2022-04-26"
]
valid_urls = []
def create_valid_url(date):
    report_urls = f"https://connect.treatwell.co.uk/login?route=%2Fcalendar%23venue%2F370180%2Fappointment%2Fday%2F{date}%2F398937"
    return report_urls
driver = TreatwellDriver()
for date in date_to_generate_report:
    valid_urls.append(create_valid_url(date))

driver.generate_multiple_day_report(valid_urls)
