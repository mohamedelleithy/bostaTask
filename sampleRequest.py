import requests

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
    "businessReference": "43535252",
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
