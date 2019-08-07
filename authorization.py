import requests
import getpass

def get_bearer_token():
    #Request sign-in info from user
    user = input("Virtuous Username:")
    password = getpass.getpass()
    #Create request
    url = "https://api.virtuoussoftware.com/Token"
    payload = "grant_type=password&username=" + user + "&password=" + password
    response = requests.request("POST", url, data=payload)
    response_json = response.json()
    #Create bearer token
    bearer_token = "Bearer " + response_json["access_token"]
    return bearer_token

def main():
    pass

if __name__ == '__main__':
    main()
