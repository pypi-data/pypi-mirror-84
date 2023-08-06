# -*- coding: utf-8 -*-
"""
Functions related to data loading in Denmark.

API specification is found on:
    https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111

functions:

    * get_weather_stations - loads the list of all Danish weather stations
    * get_weather_station_data - loads historical data for a given station
    * get_closest_weather_station - identifies the closest weather station
    * get_data_for_coordinates - loads historical data from the closest station
        to a set of coordinates

"""

# Import all useful libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

from seedftw.exceptions import MissingApiKeyError
from seedftw.environment.geography import distance_between_coordinates

# For caching
from functools import lru_cache


def _get_api_key():
    api_key_field = "SEEDFTW:API_KEY:DK:DMI"
    dmi_api_key = os.getenv(api_key_field)
    if dmi_api_key is None:
        e = MissingApiKeyError(
            message="Missing API key for DMI service.",
            environment_variable=api_key_field,
            create_at_url="https://confluence.govcloud.dk/display/FDAPI",
        )
        raise e

    return dmi_api_key


def _datetime_to_microepoch(datetimes2use):
    return int(datetimes2use.timestamp() * 1e6)


def _microepoch_to_datetime_index(microepoch):
    t = pd.DatetimeIndex(np.round(microepoch).astype("datetime64[us]"))
    # t = t.replace(tzinfo=pytz.UTC)
    return t.tz_localize("UTC")


def _microepoch_to_local_datetime(microepoch):
    t = pd.Datetime(np.round(microepoch).astype("datetime64[us]"))
    # t = t.replace(tzinfo=pytz.UTC)
    return t.tz_localize("Europe/Copenhagen")


def __format_data_table(data):
    return data.rename(columns={"Minutes5UTC": "t"}).set_index("t")


# Loading data from DMI's API
@lru_cache(maxsize=10)
def __dmi_api_call(address):

    api_key_part = "api-key=" + _get_api_key()

    query_url = "https://dmigw.govcloud.dk/" + address
    if "?" in query_url:
        binding_sym = "&"
    else:
        binding_sym = "?"

    ur_2_call = query_url + binding_sym + api_key_part

    # Read data in Json format
    result = pd.read_json(ur_2_call)

    return result


@lru_cache(maxsize=1)
def get_weather_stations():
    """Loads the list of the Danish weather stations

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    stations : pandas.DataFrame(height,latitude,longitude,name,type,stationId)
        Details of the weather stations
    """
    T = __dmi_api_call("metObs/v1/station?country=DNK")

    stations = T["location"].apply(pd.Series)
    stations["name"] = T["name"]
    stations["type"] = T["type"]
    stations["stationId"] = T["stationId"]

    return stations


def get_weather_station_data(
    station=6031,
    start_date=(datetime.now() - timedelta(days=3)),
    end_date=datetime.now(),
    resolution="hour",
):
    """Loads historical data for a given weather station

    Parameters
    ----------
    station : int or str
        stationId of the station for which data is to be loaded
    start_date : datetime
        Time for the start of the historical period
    end_date: datetime
        Time for the end of the historical period
    resolution: str
        Resolution of the data to load (raw,hour,day)

    Raises
    ------
    None

    Returns
    -------
    data : pandas.DataFrame(t,ambient_temperature)
        Timetable of the ambient temperature [degrees C]
    """

    if isinstance(station, str):
        station_string = station
    else:
        station_string = str(station).zfill(5)

    start_microepoch = _datetime_to_microepoch(start_date)
    end_microepoch = _datetime_to_microepoch(end_date)
    limit2use = 30000
    query_url = "metObs/v1/observation?from={}&to={}&stationId={}&parameterId=temp_dry&limit={}".format(
        str(start_microepoch),
        str(end_microepoch),
        station_string,
        str(limit2use),
    )

    dmi_raw_data = __dmi_api_call(query_url)
    t = _microepoch_to_datetime_index(dmi_raw_data["timeObserved"])
    t.name = "t"

    data = pd.DataFrame({"ambient_temperature": dmi_raw_data["value"]})
    data.index = t
    data = data.sort_index(ascending=True)

    if resolution == "raw":
        # Do nothing
        None
    elif resolution == "hour":
        data = data.resample("H").mean()
    elif resolution == "day":
        # Averaging per day is made in local timezone
        data.index = data.index.tz_convert("Europe/Copenhagen")
        data = data.resample("D").mean()
        data.index = data.index.tz_convert("UTC")
    else:
        print("Error: invalid resolution:" + resolution)

    return data


def get_closest_weather_station(latitude, longitude):
    """Identifies the closest weather station for a set geographical coordinates

    Parameters
    ----------
    latitude : float
        Latitude [degrees]
    longitude : float
        Longitude [degrees]

    Raises
    ------
    None

    Returns
    -------
    closest_station : pandas.Series(height,latitude,longitude,name,type,stationId)
        Details of the closest location
    """

    # Get all DMI locations
    dmi_stations = get_weather_stations()

    # Selecting the ones with all weather data available
    selected_stations = dmi_stations.loc[dmi_stations["type"] == "Synop", :]

    distance_to_stations = selected_stations.apply(
        lambda row: distance_between_coordinates(
            [latitude, longitude], [row["latitude"], row["longitude"]]
        ),
        axis=1,
    )

    closest_index = selected_stations.index[np.argmin(distance_to_stations)]
    closest_station = selected_stations.loc[closest_index, :]

    return closest_station


def get_data_for_coordinates(
    latitude,
    longitude,
    start_date=(datetime.now() - timedelta(days=3)),
    end_date=datetime.now(),
    resolution="hour",
):
    """Loads historical data from the closest weather station to a set of coordinates

    Parameters
    ----------
    latitude : float
        Latitude [degrees]
    longitude : float
        Longitude [degrees]
    start_date : datetime
        Time for the start of the historical period
    end_date: datetime
        Time for the end of the historical period
    resolution: str
        Resolution of the data to load (raw,hour,day)

    Raises
    ------
    None

    Returns
    -------
    data : pandas.DataFrame(t,ambient_temperature)
        Timetable of the ambient temperature [degrees C]
    """

    closest_station = get_closest_weather_station(latitude, longitude)
    data = get_weather_station_data(
        station=closest_station["stationId"],
        start_date=start_date,
        end_date=end_date,
        resolution=resolution,
    )
    return data
