# -*- coding: utf-8 -*-
"""
Functions related to data loading in Denmark.

"""

# Import all useful libraries
import pandas as pd
import numpy as np
import json
import urllib.parse

from datetime import datetime, timedelta

# For caching
from functools import lru_cache

# Loading data from Energinet
@lru_cache(maxsize=10)
def __dk_energinet_dataservice_call(sql_query, output_format="Dataframe"):

    # Determine the URL to use for the call
    url = (
        "https://www.energidataservice.dk/proxy/api/datastore_search_sql?sql="
        + urllib.parse.quote(sql_query)
    )

    # Read data in Json format
    api_data = pd.read_json(url)

    if any(api_data.success) == False:
        print("Failure in the API call")

    if output_format == "Dataframe":
        api_data = pd.DataFrame.from_records(api_data["result"].records)

    return api_data


def __date2api_format(datetime2use):
    return datetime2use.strftime("%Y-%m-%dT%H:%M:%SZ")


def __format_data_table(data, column_dict):
    if len(data) == 0:
        return data

    return data.rename(columns=column_dict).set_index("t")


def __format_data_table_co2_per_area(data):
    column_dict = {
        "HourUTC": "t",
        "Co2PerkWh": "co2_intensity",
        "PriceArea": "price_area",
    }
    return __format_data_table(data, column_dict=column_dict)


def __format_data_table_co2_per_distribution(data):
    column_dict = {
        "HourUTC": "t",
        "Co2PerkWh": "co2_intensity",
        "PriceArea": "price_area",
        "Co2PerkWh_200": "co2_intensity_200pc",
    }
    return __format_data_table(data, column_dict=column_dict)


def electricity_average_co2_intensity(
    area="",
    start_time=__date2api_format(datetime.now() - timedelta(hours=168)),
    end_time=__date2api_format(datetime.now()),
):

    if area == "DK1":
        condition2use = """WHERE "PriceArea" = 'DK1' AND"""

    elif area == "DK2":
        condition2use = """WHERE "PriceArea" = 'DK2' AND"""

    else:
        condition2use = """WHERE"""

    condition2use = (
        condition2use
        + """ "Minutes5UTC" >= '"""
        + start_time
        + """' AND "Minutes5UTC" <= '"""
        + end_time
        + "'"
    )

    query2use = (
        """SELECT "Minutes5UTC", "PriceArea", "CO2Emission" FROM "co2emis" """
        + condition2use
        + ' ORDER BY "Minutes5UTC" ASC'
    )

    co2_data = __dk_energinet_dataservice_call(
        sql_query=query2use, output_format="Dataframe"
    )
    return __format_data_table_co2_per_area(co2_data)


def electricity_average_co2_intensity_forecast(
    area="",
    start_time=__date2api_format(datetime.now()),
    end_time=__date2api_format(datetime.now() + timedelta(hours=24)),
):

    if area == "DK1":
        condition2use = """WHERE "PriceArea" = 'DK1' AND"""

    elif area == "DK2":
        condition2use = """WHERE "PriceArea" = 'DK2' AND"""

    else:
        condition2use = """WHERE"""

    condition2use = (
        condition2use
        + """ "Minutes5UTC" >= '"""
        + start_time
        + """' AND "Minutes5UTC" <= '"""
        + end_time
        + "'"
    )

    query2use = (
        """SELECT "Minutes5UTC", "PriceArea", "CO2Emission" FROM "co2emisprog" """
        + condition2use
        + ' ORDER BY "Minutes5UTC" ASC'
    )

    co2_data = __dk_energinet_dataservice_call(
        sql_query=query2use, output_format="Dataframe"
    )
    return __format_data_table_co2_per_area(co2_data)


def electricity_distribution_average_co2_intensity(
    start_time=__date2api_format(datetime.now() - timedelta(days=365)),
    end_time=__date2api_format(datetime.now()),
):

    condition2use = """WHERE "HourUTC">='{}' AND "HourUTC"<='{}' """.format(
        start_time, end_time
    )

    query2use = (
        """SELECT "HourUTC", "Co2PerkWh", "Co2PerkWh_200", "PriceArea" FROM "declarationemissionhour" """
        + condition2use
        + ' ORDER BY "HourUTC" ASC'
    )

    co2_data = __dk_energinet_dataservice_call(
        sql_query=query2use, output_format="Dataframe"
    )
    return __format_data_table_co2_per_distribution(co2_data)


def electricity_balance(
    area="",
    start_time=__date2api_format(datetime.now() - timedelta(days=15)),
    end_time=__date2api_format(datetime.now()),
):

    if area == "DK1":
        condition2use = """ "PriceArea" = 'DK1' AND"""

    elif area == "DK2":
        condition2use = """ "PriceArea" = 'DK2' AND"""

    else:
        condition2use = ""

    condition2use = """WHERE{} "HourUTC">='{}' AND "HourUTC"<='{}' """.format(
        condition2use, start_time, end_time
    )

    query2use = (
        """SELECT "HourUTC", "GrossCon", "ElectricBoilerCon", "NetCon","""
        + """ "LocalPowerProd", "ExchangeGreatBelt","OffshoreWindPower","""
        + """ "CentralProd","ExchangeNordicCountries",	"ExchangeContinent","""
        + """ "PriceArea",	"OnshoreWindPower",	"SolarPowerProd" """
        + """FROM "electricitybalance" """
        + condition2use
        + ' ORDER BY "HourUTC" ASC'
    )

    dict2use = {
        "HourUTC": "t",
        "GrossCon": "gross_demand",
        "ElectricBoilerCon": "electric_boiler_demand",
        "NetCon": "net_demand",
        "LocalPowerProd": "local_power_generation",
        "ExchangeGreatBelt": "exchange_great_belt",
        "OffshoreWindPower": "offshore_wind_generation",
        "CentralProd": "central_generation",
        "ExchangeNordicCountries": "exchange_nordics",
        "ExchangeContinent": "exchange_continent",
        "OnshoreWindPower": "onshore_wind_generation",
        "SolarPowerProd": "solar_generation",
        "PriceArea": "price_area",
    }

    data = __dk_energinet_dataservice_call(
        sql_query=query2use, output_format="Dataframe"
    )
    return __format_data_table(data, column_dict=dict2use)


def electricity_production_and_exchange(
    area="",
    start_time=__date2api_format(datetime.now() - timedelta(days=2)),
    end_time=__date2api_format(datetime.now()),
):

    if area == "DK1":
        condition2use = """ "PriceArea" = 'DK1' AND"""

    elif area == "DK2":
        condition2use = """ "PriceArea" = 'DK2' AND"""

    else:
        condition2use = ""

    condition2use = """WHERE{} "Minutes5UTC">='{}' AND "Minutes5UTC"<='{}' """.format(
        condition2use, start_time, end_time
    )

    query2use = (
        """SELECT "Minutes5UTC", "PriceArea", "ProductionLt100MW", "ProductionGe100MW","""
        + """ "OffshoreWindPower", "OnshoreWindPower", "SolarPower","""
        + """ "ExchangeGreatBelt", "ExchangeGermany","ExchangeNetherlands", "ExchangeNorway","""
        + """ "ExchangeSweden",	"BornholmSE4" """
        + """FROM "electricityprodex5minrealtime" """
        + condition2use
        + ' ORDER BY "Minutes5UTC" ASC'
    )

    dict2use = {
        "Minutes5UTC": "t",
        "PriceArea": "price_area",
        "ProductionLt100MW": "generation_under_100MW",
        "ProductionGe100MW": "generation_over_100MW",
        "OffshoreWindPower": "offshore_wind_generation",
        "OnshoreWindPower": "onshore_wind_generation",
        "SolarPower": "solar_generation",
        "ExchangeGreatBelt": "exchange_great_belt",
        "ExchangeGermany": "exchange_germany",
        "ExchangeNetherlands": "exchange_netherlands",
        "ExchangeNorway": "exchange_norway",
        "ExchangeSweden": "exchange_sweden",
        "BornholmSE4": "exchange_bornholm_sweden",
    }

    data = __dk_energinet_dataservice_call(
        sql_query=query2use, output_format="Dataframe"
    )
    return __format_data_table(data, column_dict=dict2use)


def electricity_spot_price(
    area="",
    start_time=__date2api_format(datetime.now() - timedelta(days=15)),
    end_time=__date2api_format(datetime.now()),
):

    if area == "DK1":
        condition2use = """ "PriceArea" = 'DK1' AND"""

    elif area == "DK2":
        condition2use = """ "PriceArea" = 'DK2' AND"""

    else:
        condition2use = ""

    condition2use = """WHERE{} "HourUTC">='{}' AND "HourUTC"<='{}' """.format(
        condition2use, start_time, end_time
    )

    query2use = (
        """SELECT "HourUTC", "SpotPriceEUR", "SpotPriceDKK", "PriceArea" FROM "elspotprices" """
        + condition2use
        + ' ORDER BY "HourUTC" ASC'
    )

    dict2use = {
        "HourUTC": "t",
        "SpotPriceEUR": "spot_price_eur",
        "SpotPriceDKK": "spot_price_dkk",
        "PriceArea": "price_area",
    }

    data = __dk_energinet_dataservice_call(
        sql_query=query2use, output_format="Dataframe"
    )
    return __format_data_table(data, column_dict=dict2use)
