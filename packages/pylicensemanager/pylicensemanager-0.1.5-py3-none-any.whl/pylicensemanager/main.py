import json
import random
import requests
from requests.auth import HTTPBasicAuth
from pylicensemanager.methods import HelperMethods, Key, Helpers
from pylicensemanager.internal import *

host = "https://example.com"  # for example, https://example.com using your wordpress site url here is probably best
consumer_key = "ck_pRkVRxe0h73HBF9pzNf2CICiv8It8rZy"  # the consumer_key given to you when you establish your API with License Manager
consumer_secret = "cs_pRkVRxe0h73HBF9pzNf2CICiv8It8rZy"  # the consumer_secret given to you when you establish your API with License Manager
license_key = "ECHOE-SILEN-PATIE-GRACE"
# license_key = "44C9-42VW-7WDP-44ZL-VDSX"
gen_id = "1"
product_id = '14'
valid_for = '368'
times_activated_max = '5'

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

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    pass


def retrieve_license():
    """Retrieves a single license key by the license key string itself. The response contains the queried license key
    data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/retrieve-a-license/
    # GET Request Url /wp-json/lmfwc/v2/licenses/FOO-FIGHTERS
    url = host + "/wp-json/lmfwc/v2/licenses/" + license_key

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))

    # Parse license information from json url
    license_request_status = json_response_dict["success"]
    license_request_id = json_response_dict["data"]["id"]
    license_request_orderid = json_response_dict["data"]["orderId"]
    license_request_productId = json_response_dict["data"]["productId"]
    license_request_userId = json_response_dict["data"]["userId"]
    license_request_licenseKey = json_response_dict["data"]["licenseKey"]
    license_request_expiresAt = json_response_dict["data"]["expiresAt"]
    license_request_validFor = json_response_dict["data"]["validFor"]
    license_request_source = json_response_dict["data"]["source"]
    license_request_status = json_response_dict["data"]["status"]
    license_request_timesActivated = json_response_dict["data"]["timesActivated"]
    license_request_timesActivatedMax = json_response_dict["data"]["timesActivatedMax"]
    license_request_createdAt = json_response_dict["data"]["createdAt"]
    license_request_updatedAt = json_response_dict["data"]["updatedAt"]
    license_request_updatedBy = json_response_dict["data"]["updatedBy"]

    # Print parsed results to stdout
    print("license_request_status : %s" % license_request_status)
    print("license_request_id : %s" % license_request_id)
    print("license_request_orderid : %r" % license_request_orderid)
    print("license_request_productId : %s" % license_request_productId)
    print("license_request_userId : %s" % license_request_userId)
    print("license_request_licenseKey : %s" % license_request_licenseKey)
    print("license_request_expiresAt : %s" % license_request_expiresAt)
    print("license_request_validFor : %r" % license_request_validFor)
    print("license_request_source : %s" % license_request_source)
    print("license_request_status : %s" % license_request_status)
    print("license_request_timesActivated : %s" % license_request_timesActivated)
    print("license_request_timesActivatedMax : %s" % license_request_timesActivatedMax)
    print("license_request_createdAt : %r" % license_request_createdAt)
    print("license_request_updatedAt : %s" % license_request_updatedAt)
    print("license_request_updatedBy : %s" % license_request_updatedBy)
    return json_response_dict
    pass


def create_license():
    """Creates a new license key with the given parameters from the request body. It is possible to leave out certain
    keys, or explicitly set them to “null”. The response will contain the newly created license key data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/create-a-license/
    # POST Request Url /wp-json/lmfwc/v2/licenses
    url = host + "/wp-json/lmfwc/v2/licenses"

    license_generated = Key()

    # Setup fallback if no license_key provided to generate one.
    key = license_key if bool(license_key) is not False else license_generated

    payload = {
        "product_id": str(product_id),
        "license_key": str(key),
        "valid_for": str(valid_for),
        "status": "active",
        "times_activated_max": str(times_activated_max)
    }

    payld = json.dumps(payload)

    json_response = requests.post(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret),
                                  headers=myjson_headers).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    # print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
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
        "product_id": str(product_id),
        "license_key": str(license_key),
        "valid_for": str(valid_for),
        "status": "active",
        "times_activated_max": str(times_activated_max)
    }

    payld = json.dumps(payload)
    json_response = requests.put(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret),
                                 headers=myjson_headers).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    # print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
    pass


def activate_license():
    """Increases the “times_activated” value by one (1). The plugin will check if there is a “times_activated_max”
    value, if there is and if the “times_activated” value has not reached the limit set by “times_activated_max”,
    then the “times_activated” will be incremented by 1, and the updated license key data object will be returned.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/activate-a-license/
    # GET Request Url /wp-json/lmfwc/v2/licenses/activate/THE-PRETENDER
    url = host + "/wp-json/lmfwc/v2/licenses/activate/" + license_key

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
    pass


def activate_license_uuid():
    """Increases the “times_activated” value by one (1). The plugin will check if there is a “times_activated_max”
    value, if there is and if the “times_activated” value has not reached the limit set by “times_activated_max”,
    then the “times_activated” will be incremented by 1, and the updated license key data object will be returned. This adds json encoded uuid payload.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/activate-a-license/
    # https://www.licensemanager.at/docs/tutorials-how-to/additional-rest-api-validation/
    # GET Request Url /wp-json/lmfwc/v2/licenses/activate/THE-PRETENDER
    url = host + "/wp-json/lmfwc/v2/licenses/activate/" + license_key

    # json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    payload = {
        "uuid": str(Helpers.GetMachineCode())
    }

    payld = json.dumps(payload)

    json_response = requests.get(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret),
                                 headers=myjson_headers).text

    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
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

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
    pass


def validate_license():
    """Checks the current activation status of a license key. The response will contain the number of activations,
    the maximum activation count, and the remaining activations.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/validate-a-license/
    # GET Request Url /wp-json/lmfwc/v2/licenses/validate/THE-PRETENDER
    url = host + "/wp-json/lmfwc/v2/licenses/validate/" + license_key

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
    pass


def list_all_generators():
    """Retrieves all currently available generators. The response will contain an array of generator data objects.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/list-all-generators/
    # GET Request Url /wp-json/lmfwc/v2/generators
    url = host + "/wp-json/lmfwc/v2/generators"

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
    pass


def retrieve_generator():
    """Retrieves a single generator by its ID. The response contains the generator data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/retrieve-a-generator/
    # GET Request Url /wp-json/lmfwc/v2/generators/2
    url = host + "/wp-json/lmfwc/v2/generators/" + str(gen_id)

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response
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
        "chunk_length": 4,
        "times_activated_max": 2,
        "separator": "-",
        "prefix": "null",
        "suffix": "null",
        "expires_in": "null"
    }

    payld = json.dumps(payload)

    json_response = requests.post(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret),
                                  headers=myjson_headers).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    # print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response

    pass


def update_generator():
    """Updates a generator by its ID. The response contains the updated generator data object.
    """
    # https://www.licensemanager.at/docs/rest-api/developer-documentation/update-a-generator/
    # Put Request Url /wp-json/lmfwc/v2/generators/4
    url = host + "/wp-json/lmfwc/v2/generators/" + str(gen_id)

    payload = {
        "name": "Generator updated by the API",
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "chunks": 5,
        "chunk_length": 4,
        "times_activated_max": 5,
        "separator": "-",
        "prefix": "null",
        "suffix": "null",
        "expires_in": "null"
    }

    payld = json.dumps(payload)

    json_response = requests.post(url, data=payld, auth=HTTPBasicAuth(consumer_key, consumer_secret),
                                  headers=myjson_headers).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    # print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    return json_response

    pass


def verify_account_key(host, account_key_to_check):
    # original credits to: https://wordpress.org/support/users/processzip/ from
    # https://wordpress.org/support/topic/python-rest-api-example/
    url = host + "/wp-json/lmfwc/v2/licenses/validate/" + account_key_to_check

    json_response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).text
    # print(json_response)
    json_response_dict = json.loads(str(json_response))
    print(json_response_dict)
    print(json.dumps(json_response_dict, indent=4))
    try:
        if json_response_dict['success']:
            print('License verification Success :)')
            return True
    except:
        print('License verification failed!')
        return False


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

# Try some keys
verify_account_key(host, "")
verify_account_key(host, "")
