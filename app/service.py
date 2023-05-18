import requests

VEHICLE_API_FIELDS_REQUIRED = [
    26,  # make
    28,  # model
    29,  # model_year
    5,  # body_class
]


def get_vehicle_raw_data(vin: str):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        # raise API Error
        return None


def extract_vehicle_data_required(data: dict):
    # Ugly but quick
    return {
        item["Variable"].lower().replace(" ", "_"): item["Value"]
        for item in data["Results"]
        if item["VariableId"] in VEHICLE_API_FIELDS_REQUIRED
    }


def get_vehicle_data(vin: str):
    raw_data = get_vehicle_raw_data(vin)
    if raw_data:
        return extract_vehicle_data_required(raw_data)
    # raise No Data


# Example usage
if __name__ == "__main__":
    vin = "1XPWD40X1ED215307"
    vin_data = get_vehicle_data(vin)

    if vin_data:
        # Displaying relevant information
        for item in vin_data:
            print(item, vin_data[item])
    else:
        print("Failed to retrieve VIN data.")
