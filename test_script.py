import requests
import json

# Login request : POST
print("Trying to Login")
print("*\n"*3)
url_ = "https://fyle-assignment101.herokuapp.com"
data_ = {
    "username" : "admin",
    "password" : "admin"
}
login = requests.post(url= str(url_ + "/login"), json= data_).json()
token = login['access_token']

print("Token Generated.")
print("*\n"*3)


# /getall request : GET (authorization is required)
print("Get all banks with offset 20 & limit 2")
print("*"*15)
response = requests.get(url=str(url_ + "/getall?limit=2&offset=20"), headers={'Authorization': 'Bearer {}'.format(str(token))})
pretty_json = json.dumps(response.json(), indent=2)
print(pretty_json)

# /get/<IFSC> request : GET (authorization is required)
print("\n\nGet bank by IFSC <WBSC0KPCB01>")
print("*"*15)
response = requests.get(url=str(url_ + "/get/WBSC0KPCB01"), headers={'Authorization': 'Bearer {}'.format(str(token))})
pretty_json = json.dumps(response.json(), indent=2)
print(pretty_json)

# /get/<IFSC> request : GET (authorization is required) Validation check
print("\n\nGet bank by IFSC <WBSC0KPCB0111111>")
print("*"*15)
response = requests.get(url=str(url_ + "/get/WBSC0KPCB0111111"), headers={'Authorization': 'Bearer {}'.format(str(token))})
pretty_json = json.dumps(response.json(), indent=2)
print(pretty_json)

# /get?name=<>&city=<> request: GET (authorization is required)
print("\n\nGet bank by name=ABHYUDAYA COOPERATIVE BANK LIMITED & city=mumbai")
print("*"*15)
response = requests.get(url=str(url_ + "/get?name=ABHYUDAYA COOPERATIVE BANK LIMITED&city=mumbai&limit=2"), headers={'Authorization': 'Bearer {}'.format(str(token))})
pretty_json = json.dumps(response.json(), indent=2)
print(pretty_json)

# /get?city=<>,<>,.. request: GET (authorization is required)
print("\n\nGet bank by only city=mumbai,new delhi limit 2 offset 75&limit=2")
print("*"*15)
response = requests.get(url=str(url_ + "/get?city=mumbai,new delhi&limit=2&offset=75"), headers={'Authorization': 'Bearer {}'.format(str(token))})
pretty_json = json.dumps(response.json(), indent=2)
print(pretty_json)


print("*"*15)
print("*"*15)
print("*"*15)
