# mock task demonastrating use of the bosta api
# we will assume the user has a list of orders to be shipped and we will use the bosta api to ship them,
# we will also assume that the user is not registered with bosta and we will use the api to register them

import requests
import json
import time
import datetime

headers = {"Content-Type": "application/json"}

firstName = "firstName"
lastName = "lastName"
email = "email@mail.com"
password = "password"
phoneNum = "0111111111"
countryId = "60e4482c7cb7d4bc4849c4d5"
businessId = ""


# function to register the user with bosta using a POST request
def register():
    url = "https://app.bosta.co/api/v2/users/business/admin"
    payload = (
        {
            "email": email,
            "password": password,
            "profile": {
                "firstName": firstName,
                "lastName": lastName,
                "phone": phoneNum,
            },
            "heardAboutUsFrom": "Facebook",
            "monthlyShipmentVolume": "LITE",
            "countryId": countryId,
        },
    )

    request = requests.post(
        "https://app.bosta.co/api/v2/users/business/admin",
        json=payload,
        headers=headers,
    )
    response = request.json()
    if response["success"] == True:
        print("User registered successfully")
        # we should proceed with verifying the user's phone number
        verify_phone()
    else:
        print("User registration failed")
        print(response["message"])


def verify_phone():
    OTP = input("Enter OTP that was sent to your phone: ")
    url = "https://app.bosta.co/api/v2/users/business-admin/phone/confirm"
    payload = {"phone": phoneNum, "token": OTP}
    request = requests.post(url, json=payload, headers=headers)
    response = request.json()
    if response["success"] == True:
        print("User phone number verified successfully")
    else:
        print("User phone number verification failed")
        print(response["message"])


def get_auth_token():
    url = "https://app.bosta.co/api/v2/users/login"
    payload = {
        "email": email,
        "password": password,
    }
    request = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    response = request.json()
    if response["success"] == True:
        print("User authenticated successfully")
        return response["data"]
    else:
        print("User authentication failed")
        print(response["message"])


def set_business_information():
    url = "https://app.bosta.co/api/v2/businesses"
    payload = {
        "name": "yourBusinessName",
        "salesChannel": "FACEBOOK_SELLER",
        "website": "yourStoreURL",
        "industry": "Electronics",
        "interestedInServices": ["Products Shipments"],
    }
    request = requests.post(url, json=payload, headers=headers)
    response = request.json()
    if response["success"] == True:
        print("Business info set successfully")
        return response["data"]["_id"]
    else:
        print("Business info setting failed")
        print(response["message"])


def get_district_id():
    url = (
        "https://app.bosta.co/api/v2/cities/getAllDistricts?countryId="
        + countryId
        + "&context=pickup"
    )
    request = requests.get(url, headers=headers)
    response = request.json()
    if response["success"] == True:
        print("Districts retrieved successfully")
        return response["data"][0]["_id"]
    else:
        print("Districts retrieval failed")
        print(response["message"])


def set_pickup_location():
    url = "https://app.bosta.co/api/v2/businesses/" + loginDataReceived["businessId"]
    # define district id before sending the request
    districtId = get_district_id()
    payload = {
        "pickupAddress": [
            {
                "locationName": "yourLocationName",
                "districtId": districtId,  # You have to get districtId of your address through the below API
                "firstLine": "Your address first line details",
                "buildingNumber": "1",
                "floor": "2",
                "apartment": "3",
                "secondLine": "Your address second line details like: landmarks",
            }
        ]
    }
    request = requests.put(url, json=payload, headers=headers)
    response = request.json()
    if response["success"] == True:
        print("Pickup location set successfully")
    else:
        print("Pickup location setting failed")
        print(response["message"])


def initiate_delivery():
    url = "http://app.bosta.co/api/v2/deliveries"

    payload = {
        "type": 25,  # must be 25 if it's a customer return
        "specs": {
            "packageType": "Parcel",
            "size": "MEDIUM",
            "packageDetails": {"itemsCount": 2, "description": "Desc."},
        },
        "notes": "Welcome Note",
        "cod": 50,  # specify the value here
        "dropOffAddress": {
            "city": "Helwan",
            "zoneId": "NQz5sDOeG",
            "districtId": "aiJudRHeOt",
            "firstLine": "Helwan street x",
            "secondLine": "Near to Bosta school",
            "buildingNumber": "123",
            "floor": "4",
            "apartment": "2",
        },
        "pickupAddress": {
            "city": "Helwan",
            "zoneId": "NQz5sDOeG",
            "districtId": "aiJudRHeOt",
            "firstLine": "Helwan street x",
            "secondLine": "Near to Bosta school",
            "buildingNumber": "123",
            "floor": "4",
            "apartment": "2",
        },
        "returnAddress": {
            "city": "Helwan",
            "zoneId": "NQz5sDOeG",
            "districtId": "aiJudRHeOt",
            "firstLine": "Maadi",
            "secondLine": "Nasr  City",
            "buildingNumber": "123",
            "floor": "4",
            "apartment": "2",
        },
        "businessReference": loginDataReceived["businessId"],
        "receiver": {
            "firstName": "Sasuke",
            "lastName": "Uchiha",
            "phone": "01065685435",
            "email": "ahmed@ahmed.com",
        },
        "webhookUrl": "https://www.google.com/",  # edit this to your configured endpoint for updates about your deliveries
    }
    headers = {"Content-Type": "application/json", "Authorization": "Bearer undefined"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


def set_pickup():
    url = "http://app.bosta.co/api/v2/pickups"

    payload = {
        "businessLocationId": "6044b12f463cb700137fc9f9",
        "notes": "test",
        "scheduledDate": "2021-06-10",
        "contactPerson": {
            "name": "Test Name",
            "phone": "01001001000",
            "email": "test@email.coom",
        },
        "repeatedData": {
            "repeatedType": "Weekly",
            "days": ["Sunday"],
            "startDate": "2021-06-10",
            "endDate": "2021-10-10",
        },
    }
    headers = {"Content-Type": "application/json", "Authorization": "Bearer undefined"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


# run the program
print("Welcome to Bosta")
register()
print(
    "Now we have registered you with Bosta and verified your phone number, \n we will now obtain an auth token to use in our requests"
)
loginDataReceived = get_auth_token()
print("Now we will set your pickup location")
set_business_information()
set_pickup_location()

# now we have the account ready, we can work on the deliveries
initiate_delivery()
set_pickup()
