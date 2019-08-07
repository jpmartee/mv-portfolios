import requests
import pandas as pd
import portfolio
import authorization

def create_query_payload(id_list, parameter):
    payload = {"groups":[]}
    for id in id_list:
        group = {"conditions":[
                    {"parameter":parameter,
                    "operator":"Is", "value":id}
                    ]
                }
        payload["groups"].append(group)
    return payload

def query(id_list,parameter,auth_token,take=10):
    url = "https://api.virtuoussoftware.com/api/Gift/Query/FullGift" + "?take=" + str(take)
    payload = str(create_query_payload(id_list,parameter))
    headers = {
    'Content-Type': "application/json",
    'Authorization': auth_token
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def get_all_passthrough(id_list,auth_token):
    response = query(id_list,parameter="Passthrough Contact Id",auth_token=auth_token)
    j = response.json()
    if j["total"] > 10:
#        print "Getting all passthrough gifts..."
        response = query(id_list,parameter="Passthrough Contact Id",auth_token=auth_token,take=j["total"])
    return response

def get_all_direct(id_list,auth_token):
    response = query(id_list,parameter="Contact Id",auth_token=auth_token)
    j = response.json()
    if j["total"] > 10:
#        print "Getting all direct gifts..."
        response = query(id_list,parameter="Contact Id",auth_token=auth_token,take=j["total"])
    return response

def main():
    pass

if __name__ == '__main__':
    main()
