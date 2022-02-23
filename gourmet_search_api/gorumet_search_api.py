import pandas as pd
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import ast
from typing import Dict, List

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
url = os.environ.get("GOURMET_URI")
api_key = os.environ.get("API_KEY")


def get_restaurant_information(search_keyword: str) -> Dict:
    """
    Run Hot Pepper api to get restaurant information

    Args
    ------
    search_keyword: Information about the restaurant you want to search for

    Return
    -------
    result: Get information on restaurants that match your keywords

    Examples
    ---------
    >>> search_keyword = "沖縄"

    >>> result =
        {'results': {'api_version': '1.26',
        'results_available': 1989,
        'results_returned': '1',
        'results_start': 1,
        'shop': [{'name': 'restaurant',
            'wedding': '',
            ....
            'wifi': 'あり'}]}}

    """
    params = {"key": api_key, "keyword": search_keyword, "format": "json", "count": 100}
    res = requests.get(url, params)
    result = res.json()
    return result


def forming_restaurant_data(restaurant_dict: Dict) -> List:
    """
    Forming restaurant data of type dict

    Args
    ------
    restaurant_dict: See Examples

    Return
    -------
    result_df: See Examples

    Examples
    ---------
    >>> restaurant_dict =
        {'results': {'api_version': '1.26',
        'results_available': 1989,
        'results_returned': '1',
        'results_start': 1,
        'shop': [{'name': 'restaurant',
            'wedding': '',
            ....
            'wifi': 'あり'}]}}
    >>> forming_restaurant_data(get_restaurant_info)
        [
        {'name': 'restaurant',
        'address': '福岡県福岡市',
        'station_name': '天神',
        'average_price': '2001～3000円',
        'genre': '韓国料理',
        'urls': 'https://www.sample.jp/',
        'card': '利用可'}
        ]

    """
    result_df = pd.DataFrame(restaurant_dict["results"]["shop"])
    result_df = result_df[
        ["name", "address", "budget", "station_name", "sub_genre", "urls", "card"]
    ]
    result_df["average_price"] = result_df["budget"].apply(lambda x: x["name"])
    result_df["sub_genre"] = result_df["sub_genre"].fillna(
        "{'code': 'without code','name': 'not listed'}"
    )
    result_df["sub_genre"] = result_df["sub_genre"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    result_df["genre"] = result_df["sub_genre"].apply(lambda x: x["name"])
    result_df["urls"] = result_df["urls"].apply(lambda x: x["pc"])
    result_list = result_df[
        ["name", "address", "station_name", "average_price", "genre", "urls", "card"]
    ].to_dict(orient="records")
    return result_list


def search_price(restaurant_list: List, asking_price: int) -> List:
    """
    Receive restaurant information and display
    restaurants that match your price request

    Args
    ------
    restaurant_list: See Examples
    asking_price: Price you want to search for

    Return
    -------
    result_list: See Examples

    Examples
    ---------
    >>> restaurant_list = [
        {'name': 'restaurant1',
        'address': '福岡県福岡市',
        'station_name': '天神',
        'average_price': '2001～3000円',
        'genre': '韓国料理',
        'urls': 'https://www.sample.jp/',
        'card': '利用可'},
        {'name': 'restaurant2',
        'address': '福岡県福岡市',
        'station_name': '天神',
        'average_price': '3001～4000円',
        'genre': '韓国料理',
        'urls': 'https://www.sample.jp/',
        'card': '利用可'}
        ]

    >>> asking_price = 2500

    >>> search_price(restaurant_list, asking_price)
            name        address  station_name  average_price     genre                   urls   card
    0  restaurant1  福岡県福岡市         天神  2001～3000円  韓国料理  https://www.sample.jp/  利用可

    """
    restaurant_df = pd.DataFrame(restaurant_list)
    restaurant_df["average_lower_price"] = restaurant_df["average_price"].apply(
        lambda x: int(x.split("～")[0])
    )
    restaurant_df["average_upper_price"] = restaurant_df["average_price"].apply(
        lambda x: int(x.split("～")[1].split("円")[0])
    )
    result_df = restaurant_df[
        restaurant_df["average_lower_price"].apply(lambda x: x <= asking_price)
        & restaurant_df["average_upper_price"].apply(lambda x: asking_price <= x)
    ]
    result_list = result_df[
        ["name", "address", "station_name", "average_price", "genre", "urls", "card"]
    ]
    return result_list


def search_station(restaurant_list: List, search_station_name: str):
    """
    Receives restaurant information and displays the restaurants
    that match the station you want to search

    Args
    ------
    restaurant_list: See Examples
    search_station_name: Station you want to search for

    Return
    -------
    result_list: See Examples

    Examples
    ---------
    >>> restaurant_list = [
        {'name': 'restaurant1',
        'address': '福岡県福岡市',
        'station_name': '博多',
        'average_price': '2001～3000円',
        'genre': '韓国料理',
        'urls': 'https://www.sample.jp/',
        'card': '利用可'},
        {'name': 'restaurant2',
        'address': '福岡県福岡市',
        'station_name': '天神',
        'average_price': '3001～4000円',
        'genre': '韓国料理',
        'urls': 'https://www.sample.jp/',
        'card': '利用可'}
        ]

    >>> search_station_name = "博多"

    >>> search_price(restaurant_list, asking_price)
            name        address  station_name  average_price     genre                   urls   card
    0  restaurant1  福岡県福岡市         博多  2001～3000円  韓国料理  https://www.sample.jp/  利用可

    """
    restaurant_df = pd.DataFrame(restaurant_list)
    result_df = restaurant_df[
        restaurant_df["station_name"].apply(lambda x: x in search_station_name)
    ]

    return result_df


get_restaurant_info = get_restaurant_information("福岡")
forming_data = forming_restaurant_data(get_restaurant_info)
search_price(forming_data, asking_price=2500)
search_station(forming_data, search_station_name="博多")
