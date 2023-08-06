api_token = ""
api_url = ""
webhook_secret = ""


def use_staging():
    global api_url
    api_url = "https://api.digimon.arivo.fun"


def use_production():
    global api_url
    api_url = "https://api.parken.arivo.app"


use_production()
