import requests
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


# ---------------- ADD USERS TO FLIGHT CLUB ------------------------------ #
USERS_ENDPOINT = "https://api.sheety.co/..."
print("Welcome to WB Flight Club!")
FIRST_NAME = input("Please enter your first name: ")
LAST_NAME = input("Please enter your last name: ")
EMAIL = input("Please enter your email address: ")
VERI_EMAIL = input("Please enter your email address again: ")

response = requests.get(url=USERS_ENDPOINT)
users_data = response.json()["users"]

if not users_data:
    if EMAIL == VERI_EMAIL:
        params = {
            "user": {
                "firstName": FIRST_NAME,
                "lastName": LAST_NAME,
                "email": EMAIL,
            }
        }
        response = requests.post(url=USERS_ENDPOINT, json=params)
        response.raise_for_status()
else:
    for user in users_data:
        if user["email"] == EMAIL:
            print(f"The email {user['email']} already exist.")
            break
        else:
            params = {
                "user": {
                    "firstName": FIRST_NAME,
                    "lastName": LAST_NAME,
                    "email": EMAIL,
                }
            }

            response = requests.post(url=USERS_ENDPOINT, json=params)
            response.raise_for_status()

# ----------------- UPDATE GOOGLE SHEET WITH IATA CODES ------------------ #
google_sheet = DataManager()
google_sheet_data = google_sheet.get_destination_data()
flight_search = FlightSearch()

for row in google_sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])

google_sheet.destination_data = google_sheet_data
google_sheet.update_destination_data()

# ---------------- SEARCH FLIGHTS FROM LONDON TO DESTINATION ON GOOGLE SHEET -------------- #
for destination in google_sheet_data:
    flight = flight_search.check_flights(destination["iataCode"])

    # ---------------- SEND TEXT USING TWILIO ---------------------------- #
    notification_manager = NotificationManager()
    if flight.price < destination["lowestPrice"]:
        link = flight.url.format(link=flight.url, text="Please click here to book your flight!")
        if flight.stop_overs == 0:
            notification_manager.send_text(
                message=f"\n\nLow Flight Alert!\n\n"f"Pay ${flight.price} for a direct flight from "
                        f"{flight.origin_city}-{flight.origin_airport} to "
                        f"{flight.destination_city}-{flight.destination_airport}, "
                        f"from {flight.out_date} to {flight.return_date}."
                        f"{link}")

            for user in users_data:
                notification_manager.send_emails(
                    recipient_email=user["email"],
                    msg=f"Subject: Low Flight Alert!\n\n"f"Pay ${flight.price} for a direct flight from "
                        f"{flight.origin_city}-{flight.origin_airport} to "
                        f"{flight.destination_city}-{flight.destination_airport}, "
                        f"from {flight.out_date} to {flight.return_date}."
                        f"{link}")
        else:
            notification_manager.send_text(
                message=f"\n\nLow Flight Alert!\n\n"f"Pay ${flight.price} for a flight from "
                        f"{flight.origin_city}-{flight.origin_airport} to "
                        f"{flight.destination_city}-{flight.destination_airport}, with {flight.stop_overs} stops, "
                        f"from {flight.out_date} to {flight.return_date}."
                        f"{link}")

            for user in users_data:
                notification_manager.send_emails(
                    recipient_email=user["email"],
                    msg=f"Subject: Low Flight Alert!\n\n"f"Pay ${flight.price} for a flight from "
                        f"{flight.origin_city}-{flight.origin_airport} to "
                        f"{flight.destination_city}-{flight.destination_airport}, with {flight.stop_overs} stops, "
                        f"from {flight.out_date} to {flight.return_date}."
                        f"{link}")

    else:
        notification_manager.send_text(
            message=f"Sorry, based on your currently chosen lowest flight price, we could not find a"
                    f"match. Please alter your information or try again later. Thanks!.")

        for user in users_data:
            notification_manager.send_emails(
                recipient_email=user["email"],
                msg=f"Subject: Flight Alert\n\nSorry, based on your currently chosen lowest flight price, "
                    f"we could not find a match. Please alter your information or try again later. Thanks!.")
