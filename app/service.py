from tempfile import mkstemp
import requests
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session_maker
from exceptions import VPICAPIException, VehicleNotFoundException

######################
#
# Vehicle API
#
######################

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
        raise VPICAPIException


async def get_vehicle_data(vin: str):
    raw_data = get_vehicle_raw_data(vin)

    result = {}
    errors = 0
    for item in raw_data["Results"]:
        if item["VariableId"] in VEHICLE_API_FIELDS_REQUIRED:
            result[item["Variable"].lower().replace(" ", "_")] = item["Value"]
            # When a Vehicle is not found, their values are None
            if item["Value"] is None:
                errors += 1

    print(result)
    if errors >= 3:
        raise VehicleNotFoundException

    return result


######################
#
# Export
#
######################


def pandas_query(session):
    """This function is to isolate the normal sync operation of Pandas.

    Pandas has a magic method `read_sql_table` that convert a DB table into DataFrame

    Args:
        session (Session): SQLAlchemy session

    Returns:
        DataFrame: The table `vehicles` converted into Pandas dataframe
    """
    conn = session.connection()
    return pd.read_sql_table("vehicles", conn)


async def export_to_parquet():
    """While Pandas doesn't accept Async connections, I'm using `async_session_maker` directly
    and isolating the pandas method to read from database

    Returns:
        file_path (str): Creates a temporary file in the most secure manner possible
    """
    fd, file_path = mkstemp()
    async with async_session_maker() as session:
        df = await session.run_sync(pandas_query)
        df.to_parquet(file_path, compression="gzip")
    return file_path


# API Example usage
if __name__ == "__main__":
    vin = "1XPWD40X1ED215307"
    vin_data = get_vehicle_data(vin)

    if vin_data:
        # Displaying relevant information
        for item in vin_data:
            print(item, vin_data[item])
    else:
        print("Failed to retrieve VIN data.")
