import requests


class DataManager:

    def __init__(self):
        self.endpoint = "https://api.sheety.co/..."
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.endpoint)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_data(self):
        for city in self.destination_data:
            params = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(url=f"{self.endpoint}/{city['id']}", json=params)

