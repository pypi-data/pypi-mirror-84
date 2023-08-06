api_token = ""
api_url = ""
webhook_secret = ""

from .const import *


def use_staging():
    global api_url
    api_url = const.staging_api_url


def use_production():
    global api_url
    api_url = const.prod_api_url


use_production()
