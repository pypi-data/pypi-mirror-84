import json
import requests
from requests.auth import HTTPBasicAuth

host = "https://test.wizardassistant.com"
consumer_key = "ck_pRkVRxe0h73HBF9pzNf2CICiv8It8rZy"
consumer_secret = "cs_pRkVRxe0h73HBF9pzNf2CICiv8It8rZy"
license_key = "ECHOE-SILEN-PATIE-GRACE"
gen_id = "1"
# license_key = "ECHOE-SILEN-PATIE-GRACE"

myjson_headers = {'Content-Type': 'application/json'}


# https://www.licensemanager.at/docs/rest-api/developer-documentation/

def list_all_licenses():
    """This route is used to retrieve all license keys from the database. Be very careful, if you do not need to use
    this API route in your productive environment then it is best to disable the route altogether via the settings
    page. The response contains an array of license key data objects.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/list-all-licenses/
    # GET Request URL /wp-json/lmfwc/v2/licenses
    url = host + "/wp-json/lmfwc/v2/licenses"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(response.text.encode('utf8'))
    pass


def retrieve_license():
    """Retrieves a single license key by the license key string itself. The response contains the queried license key
    data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/retrieve-a-license/
    # GET Request Url /wp-json/lmfwc/v2/licenses/FOO-FIGHTERS
    url = host + "/wp-json/lmfwc/v2/licenses/" + license_key
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(response.text.encode('utf8'))
    pass


def create_license():
    """Creates a new license key with the given parameters from the request body. It is possible to leave out certain
    keys, or explicitly set them to “null”. The response will contain the newly created license key data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/create-a-license/
    # POST Request Url /wp-json/lmfwc/v2/licenses
    url = host + "/wp-json/lmfwc/v2/licenses"

    payload = {
        "product_id": "14",
        "license_key": "ECHOE-SILEN-PATIE-GRACE",
        "valid_for": "365",
        "status": "active",
        "times_activated_max": 3
    }

    payld = json.dumps(payload)
    response = requests.post(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret), headers=myjson_headers)
    print(response.text.encode('utf8'))
    pass


def update_license():
    """Performs an update of the license key. The request will not update key values that aren’t present in the
    request body, however if they are present their value will be updated, even if it’s a null value. The request
    will return the updated license key data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/update-a-license/
    # Put Request Url /wp-json/lmfwc/v2/licenses/THE-PRETENDER
    url = host + "/wp-json/lmfwc/v2/licenses/" + license_key

    payload = {
        "product_id": "14",
        "license_key": "ECHOE-SILEN-PATIE-GRACE",
        "valid_for": "null",
        "status": "active",
        "times_activated_max": 999
    }

    payld = json.dumps(payload)
    response = requests.put(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret), headers=myjson_headers)
    print(response.text.encode('utf8'))
    pass


def activate_license():
    """Increases the “times_activated” value by one (1). The plugin will check if there is a “times_activated_max”
    value, if there is and if the “times_activated” value has not reached the limit set by “times_activated_max”,
    then the “times_activated” will be incremented by 1, and the updated license key data object will be returned.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/activate-a-license/
    # GET Request Url /wp-json/lmfwc/v2/licenses/activate/THE-PRETENDER
    url = host + "/wp-json/lmfwc/v2/licenses/activate/" + license_key
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(response.text.encode('utf8'))
    pass


def deactivate_license():
    """Decreases the “times_activated” value by one (1). The plugin will check if the current value of
    “times_activated” is one (1) or greater. If so, the plugin will decrement the “times_activated” value by one and
    the updated license key will be returned. It is not possible to deactivate a license key whose “times_activated”
    is null or already zero (0). The response will contain the updated license key data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/deactivate-a-license/
    # GET Request Url /wp-json/lmfwc/v2/licenses/deactivate/THE-PRETENDER
    url = host + "/wp-json/lmfwc/v2/licenses/deactivate/" + license_key
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(response.text.encode('utf8'))
    pass


def validate_license():
    """Checks the current activation status of a license key. The response will contain the number of activations,
    the maximum activation count, and the remaining activations.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/validate-a-license/
    # GET Request Url /wp-json/lmfwc/v2/licenses/validate/THE-PRETENDER
    url = host + "/wp-json/lmfwc/v2/licenses/validate/" + license_key
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(response.text.encode('utf8'))
    pass


def list_all_generators():
    """Retrieves all currently available generators. The response will contain an array of generator data objects.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/list-all-generators/
    # GET Request Url /wp-json/lmfwc/v2/generators
    url = host + "/wp-json/lmfwc/v2/generators"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(response.text.encode('utf8'))
    pass


def retrieve_generator():
    """Retrieves a single generator by its ID. The response contains the generator data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/retrieve-a-generator/
    # GET Request Url /wp-json/lmfwc/v2/generators/2
    url = host + "/wp-json/lmfwc/v2/generators/" + str(gen_id)
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(response.text.encode('utf8'))
    pass


def create_generator():
    """Creates a new generator. The response contains the newly created generator data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/create-a-generator/
    # POST Request Url /wp-json/lmfwc/v2/generators
    url = host + "/wp-json/lmfwc/v2/generators"

    payload = {
        "name": "Generator created by the API",
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "chunks": 5,
        "chunk_length": 5,
        "times_activated_max": 2,
        "separator": "-",
        "prefix": "null",
        "suffix": "null",
        "expires_in": "null"
    }

    payld = json.dumps(payload)
    response = requests.post(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret), headers=myjson_headers)
    print(response.text.encode('utf8'))
    pass


def update_generator():
    """Updates a generator by its ID. The response contains the updated generator data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/update-a-generator/
    # Put Request Url /wp-json/lmfwc/v2/generators/4
    url = host + "/wp-json/lmfwc/v2/generators/" + str(gen_id)

    payload = {
        "name": "Generator created by the API",
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "chunks": 4,
        "chunk_length": 5,
        "times_activated_max": 5,
        "separator": "-",
        "prefix": "null",
        "suffix": "null",
        "expires_in": "null"
    }

    payld = json.dumps(payload)
    response = requests.put(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret), headers=myjson_headers)
    print(response.text.encode('utf8'))
    pass

# How to call a function and test.
# list_all_licenses()
# retrieve_license()
# create_license()
# update_license()
# activate_license()
# deactivate_license()
# validate_license()
# list_all_generators()
# retrieve_generator()
# create_generator()
# update_generator()
