import json
import datetime
import pandas as pd
import calendar

staff_dict = None
shop_summary = {
    "cash": 0.00,
    "card": 0.00,
    "twCash": 0.00,
    "twCard": 0.00,
    "grossIncome": 0.00,
    "netIncome": 0.00
}


def open_and_load_data_to_dict(filename):
    with open(filename) as json_file:
        staff_dict = json.load(json_file)
    return staff_dict


def fee_deducted_from_treatwell(treatment):
    fee = treatment["personOrTreatwellBook"].split()[6].replace("(", '').replace("%",
                                                                                 '')  # Remove any character before and after fee usually ( and %
    if (fee == "Order"):
        return 0
    return int(fee)


def update_shop_summary(currencyType):
    percentage_shop_income_after_TWfee_deducted = ((100 - fee_deducted_from_treatwell(booking)) / 100)
    shop_summary[currencyType] += float(booking["price"])
    shop_summary["grossIncome"] += float(booking["price"])
    shop_summary["netIncome"] += (float(booking["price"]) * percentage_shop_income_after_TWfee_deducted)


def get_day_of_the_week(dateFromTreatwell):
    return calendar.day_name[datetime.datetime.strptime(dateFromTreatwell, "%d %b, %Y").weekday()]

def treatment_not_pay():
    if "card" in booking["note"]:
        update_shop_summary("card")
    elif "cash" in booking["note"]:
        update_shop_summary("twCash")

    else:
        print(booking["price"])
        print(f"Please specify cash or card in the note section @ {booking}")
        print("Exit program..")
        raise ValueError(f"Please specify cash or card on note section @ {booking}")

def treatment_by_calling():
    print("Customer call")
    if "card" in booking["note"]:
        update_shop_summary("card")
    elif "cash" in booking["note"]:
        update_shop_summary("cash")
    else:
        print(booking["price"])
        print(f"Please specify cash or card in the note section @ {booking}")
        print("Exit program..")
        raise ValueError(f"Please specify cash or card on note section @ {booking}")

def treatment_by_treatwell_or_google():

    print("Treatwell book")
    if "UNPAID" in booking["paidOrUnpaid"]:
        treatment_not_pay()
    else:
        update_shop_summary("twCard")

staff_dict = open_and_load_data_to_dict("29 Jun, 2022.json")
time_remove_list = ["(1 h)","(45 min)"]

def remove_extra_time_in_staff_duration():
    for _, staff in staff_dict["staffs"].items():
        if len(staff["bookings"]) > 0:
            for booking in staff["bookings"]:

                for remove_item in time_remove_list:
                    print(booking["duration"])
                    booking["duration"] = booking["duration"].replace(remove_item, '')
                    print(booking["duration"])
# pd.Timedelta("2 hours")
remove_extra_time_in_staff_duration()
for _, staff in staff_dict["staffs"].items():
    if len(staff["bookings"]) > 0:
        # Initialise total hrs of staff work
        staff["dailyHrsWork"] = pd.Timedelta("0 hours")
        for booking in staff["bookings"]:
            staff["dailyHrsWork"] += pd.Timedelta(booking["duration"])
            if "voucher" in booking["note"].lower() or "course" in booking["note"].lower():
                continue
            if "Booked" in booking["personOrTreatwellBook"]:
                treatment_by_treatwell_or_google()
            else:
                treatment_by_calling()
        # print(staff["dailyHrsWork"]/pd.Timedelta("1 hours"))

# print(calendar.day_name[datetime.datetime.strptime(staff_dict["date"], "%d %b, %Y").weekday()])

print(shop_summary)
