import requests
from datetime import datetime
import smtplib

MY_LAT = 52.5162494077299
MY_LNG = 13.377701674153512
my_coordinates = (MY_LAT, MY_LNG)
destiny = "user@outlook.com"


def split_time(input_string):
    output = ""
    remove_t = input_string.split("T")
    remove_dots = remove_t[1].split(":")
    for i in remove_dots[0:2]:
        if len(i) == 1:
            output += "0" + i
        else:
            output += i
    return int(output)


def fetch_sun():
    parameters = {"lat": MY_LAT, "lng": MY_LNG, "formatted": 0}
    # response = requests.get(url=f"https://api.sunrise-sunset.org/json?lat={parameters['lat']}&lng={parameters['lng']}&formatted=0")
    # or
    response = requests.get(
        url=f"https://api.sunrise-sunset.org/json", params=parameters
    )
    response.raise_for_status()
    results = response.json()["results"]
    return results


def get_time():
    time_now = [datetime.now().hour, datetime.now().minute]
    time_standard = ""
    for i in time_now:
        if len(str(i)) == 1:
            time_standard += "0" + str(i)
        else:
            time_standard += str(i)
    return int(time_standard)


def get_pos():
    print("request sent")
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    print(response.status_code)
    data = response.json()["iss_position"]
    print("Data is fetched")
    location_iss = (float(data["latitude"]), float(data["longitude"]))
    # location_iss = ((data["longitude"]), (data["latitude"]))
    print(location_iss)
    return location_iss


def send_email(message):
    my_email = "***@gmail.com"
    my_pass = "***"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_pass)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=destiny,
            msg=f"Subject:ISS in range\n\n{message}",
        )


sunrise_set = fetch_sun()
sunrise = split_time(sunrise_set["sunrise"])
sunset = split_time(sunrise_set["sunset"])
time_present = get_time()
iss_coordinates = get_pos()
message = "ISS is in range at the moment. Look to the sky!"


if time_present > sunset or time_present < sunrise:
    # since it is night, it would be possible to see
    # print("sky is dark")
    if (my_coordinates[0] - 5) <= iss_coordinates[0] <= (my_coordinates[0] + 5) and (
        my_coordinates[1] - 5
    ) <= iss_coordinates[1] <= (my_coordinates[1] + 5):
        # iss in range, send email
        # print("iss in range, send email")
        send_email(message)
