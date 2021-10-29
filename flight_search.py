import requests
from datetime import *
from flight_data import FlightData


class FlightSearch:

    def __init__(self):
        self.endpoint = "https://tequila-api.kiwi.com/"
        self.api_key = MY_API_KEY

    def get_destination_code(self, city):
        header = {"apikey": self.api_key}
        response = requests.get(url=f"{self.endpoint}locations/query?term={city}", headers=header)
        iata_code = response.json()["locations"][0]["code"]
        return iata_code

    def check_flights(self,  destination_city_code):
        header = {"apikey": self.api_key}

        params = {
            "fly_from": "LAX",
            "fly_to": destination_city_code,
            "date_from": (datetime.now() - timedelta(1)).strftime("%d/%m/%Y"),
            "date_to": (datetime.now() + timedelta(180)).strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(url=f"{self.endpoint}v2/search?", headers=header, params=params)

        try:
            flight_info = response.json()["data"][0]
        except IndexError:
            params = {
                "fly_from": "LAX",
                "fly_to": destination_city_code,
                "date_from": (datetime.now() - timedelta(1)).strftime("%d/%m/%Y"),
                "date_to": (datetime.now() + timedelta(180)).strftime("%d/%m/%Y"),
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "max_stopovers": 3,
                "curr": "USD"
            }

            response = requests.get(url=f"{self.endpoint}v2/search?", headers=header, params=params)
            flight_info = response.json()["data"][0]

            flight_data = FlightData(
                price=flight_info["price"],
                origin_city=flight_info["cityFrom"],
                origin_airport=flight_info["flyFrom"],
                destination_city=flight_info["cityTo"],
                destination_airport=flight_info["flyTo"],
                stop_overs=3,
                out_date=(flight_info["route"][0]["local_departure"]).split("T")[0],
                return_date=(flight_info["route"][1]["local_departure"]).split("T")[0],
                url=flight_info["deep_link"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=flight_info["price"],
                origin_city=flight_info["cityFrom"],
                origin_airport=flight_info["flyFrom"],
                destination_city=flight_info["cityTo"],
                destination_airport=flight_info["flyTo"],
                stop_overs=0,
                out_date=(flight_info["route"][0]["local_departure"]).split("T")[0],
                return_date=(flight_info["route"][1]["local_departure"]).split("T")[0],
                url=flight_info["deep_link"]
            )

            return flight_data

