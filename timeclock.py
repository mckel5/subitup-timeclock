import requests
import logging

from datetime import datetime
import consts

def get_employee_info(employee_id: str) -> tuple[str, str]:
    url = "https://www.timetrackpay.com/API2/managers/timeclock_App_data.asmx/Online_authenticate_Employee"

    data = {
        "deviceKey": consts.deviceKey,
        "deviceSecret": consts.deviceSecret,
        "deviceUniqueID": consts.deviceUniqueID,
        "employee_email": "",
        "employee_password": "",
        "scanValue": employee_id,
        "phonenumber": employee_id,
        "isScan": True,
        "isPhoneAuth": False,
    }

    response = requests.post(url, data=data)
    logging.debug(response.json())

    employeekey = response.json()[0]["eid"]
    employeetoken = response.json()[0]["E_APIToken"]

    return employeekey, employeetoken


def is_clocked_in(employee_id: str) -> bool:
    employee_key = get_employee_info(employee_id)[0]
    return bool(get_timeclock_key(employee_key))


def get_timeclock_key(employeekey: str) -> str:
    url = "https://www.timetrackpay.com/API2/managers/timeclock_App_data.asmx/Online_ClockIn_Status"

    data = {
        "employeekey": employeekey,
        "deviceKey": consts.deviceKey,
        "deviceSecret": consts.deviceSecret,
        "deviceUniqueID": consts.deviceUniqueID,
    }

    response = requests.post(url, data=data)
    logging.debug(response.json())

    # ETC_ID only sent when employee is clocked in
    return response.json()[0]["ETC_ID"] if "ETC_ID" in response.json()[0] else ""


def get_api_token(employeetoken: str) -> str:
    url = "https://www.timetrackpay.com/API2/managers/timeclock_App_data.asmx/Online_Employee_PositionList"

    data = {
        "employeetoken": employeetoken,
        "deviceKey": consts.deviceKey,
        "deviceSecret": consts.deviceSecret,
        "deviceUniqueID": consts.deviceUniqueID,
    }

    response = requests.post(url, data=data)
    logging.debug(response.json())

    token = response.json()[0]["dm_apitoken"]

    return token


def request_clock_in(api_token: str, employeekey: str) -> None:
    deptkey = consts.deptkey
    time = (
        datetime.now().strftime("%m/%d/%Y %I:%M:%S ")
        + datetime.now().strftime("%p").lower()
    )

    url = (
        "https://www.timetrackpay.com/API2/managers/timeclock_data.asmx/clockin_withGPS"
    )

    data = {
        "token": api_token,
        "deptkey": deptkey,
        "employeekey": employeekey,
        "clockin": time,
        "shiftkey": "",
        "clockinNote": "Automated via Raspberry Pi",
        "editNote": "Device: Service%20Desk%20Timeclock",
        "clockin_lat": 0,
        "clockin_long": 0,
        "clockin_devicekey": consts.deviceKey,
        "datetime_Of_Edit": time,
    }

    response = requests.post(url, data=data)
    logging.debug(response.json())


def request_clock_out(api_token: str, employeekey: str, timeclockkey: str) -> None:
    deptkey = consts.deptkey
    time = (
        datetime.now().strftime("%m/%d/%Y %I:%M:%S ")
        + datetime.now().strftime("%p").lower()
    )

    url = "https://www.timetrackpay.com/API2/managers/timeclock_data.asmx/clockout_withGPS"

    data = {
        "token": api_token,
        "deptkey": deptkey,
        "employeekey": employeekey,
        "clockout": time,
        "shiftkey": "",
        "clockoutNote": "Automated via Raspberry Pi",
        "editNote": "Device: Service%20Desk%20Timeclock",
        "clockout_lat": 0,
        "clockout_long": 0,
        "clockout_devicekey": consts.deviceKey,
        "datetime_Of_Edit": time,
        "timeclockkey": timeclockkey,
    }

    response = requests.post(url, data=data)
    logging.debug(response.json())


def clock_in(employee_id: str) -> None:
    logging.info(f"Attempting to clock in employee {employee_id}.")
    try:
        employeekey, employeetoken = get_employee_info(employee_id)
        clocked_out = get_timeclock_key(employeekey) == ""
        if not clocked_out:
            logging.info(f"Employee {employee_id} is already clocked in. Exiting.")
            return
        api_token = get_api_token(employeetoken)
        request_clock_in(api_token, employeekey)
    except Exception:
        logging.exception("Exception occurred")
        return
    logging.info(f"Completed clocking in employee {employee_id}.")


def clock_out(employee_id: str) -> None:
    logging.info(f"Attempting to clock out employee {employee_id}.")
    try:
        employeekey, employeetoken = get_employee_info(employee_id)
        timeclockkey = get_timeclock_key(employeekey)
        if not timeclockkey:
            logging.info(f"Employee {employee_id} is already clocked out. Exiting.")
            return
        api_token = get_api_token(employeetoken)
        request_clock_out(api_token, employeekey, timeclockkey)
    except Exception:
        logging.exception("Exception occurred")
        return
    logging.info(f"Completed clocking out employee {employee_id}.")


if __name__ == "__main__":
    main()
