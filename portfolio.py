import requests
import pandas as pd
from datetime import datetime
import gifts
import parse_gifts
import authorization

def portfolio_query(owner, auth_token, take=10):
    url = "https://api.virtuoussoftware.com/api/Contact/Query"
    querystring = {"take":str(take)}

    payload = {"groups": [
                {"conditions": [
                    {"parameter":"Owner", "operator":"IsAnyOf",
                    "values":[owner]}
                    ]
                 }
                 ]
                }
    headers = {
        'Content-Type': "application/json",
        'Authorization': auth_token
        }
    response = requests.request("POST", url, data=str(payload), headers=headers, params=querystring)
    return response

def get_all_portfolio_contacts(owner, auth_token):
    response = portfolio_query(owner, auth_token)
    j = response.json()
    if j["total"] > 10:
#        print "Getting portfolio contacts..."
        response = portfolio_query(owner,auth_token,take=j["total"])
    return response

def amount_by_contact(df, contact_type):
    gift_amounts = df[[contact_type, "amount"]]
    return gift_amounts.groupby([contact_type]).sum()

class Portfolio(object):
    """docstring for Portfolio."""
    def __init__(self, owners=["Sherri's Portfolio", "Kelly's Portfolio"]):
        super(Portfolio, self).__init__()
        self.owners = owners
        self.bearer_token = authorization.get_bearer_token()
        self.response_0 = get_all_portfolio_contacts(owners[0],self.bearer_token)
        self.response_1 = get_all_portfolio_contacts(owners[1],self.bearer_token)
        self.passthrough = None
        self.direct = None
################################
    def contact_df(self):
        """Returns pandas DataFrame of all contacts in Portfolio"""
        sherri_contacts = self.response_0.json()["list"]
        sherri_contacts_df = pd.DataFrame(sherri_contacts)
        sherri_contacts_df["owner"] = "Sherri's Portfolio"
        kelly_contacts = self.response_1.json()["list"]
        kelly_contacts_df = pd.DataFrame(kelly_contacts)
        kelly_contacts_df["owner"] = "Kelly's Portfolio"
        return pd.concat([sherri_contacts_df,kelly_contacts_df],ignore_index=True)
################################
    def contact_ids(self):
        """Returns list of contact ids in Portfolio"""
        return self.contact_df()["id"].tolist()
################################
    def all_passthrough_gifts_response(self):
        """Returns all passthrough gifts by those in portfolio as request response"""
        if self.passthrough == None:
            self.passthrough = gifts.get_all_passthrough(self.contact_ids(),self.bearer_token)
        return self.passthrough
################################
    def all_passthrough_gifts(self):
        """Returns pandas DataFrame of response from all_passthrough_gifts"""
        response = self.all_passthrough_gifts_response()
        return pd.DataFrame(response.json()["list"])
################################
    def passthrough_gifts_last_year(self):
        """Returns pandas DataFrame of last year to date passthrough gifts"""
        all_passthrough_gifts = self.all_passthrough_gifts()
        return parse_gifts.get_last_year_gifts(all_passthrough_gifts)
################################
    def passthrough_gifts_lytd(self):
        """Returns pandas DataFrame of last year to date passthrough gifts"""
        all_passthrough_gifts = self.all_passthrough_gifts()
        return parse_gifts.get_lytd_gifts(all_passthrough_gifts)
################################
    def passthrough_gifts_ytd(self):
        """Returns pandas DataFrame of year to date passthrough gifts"""
        all_passthrough_gifts = self.all_passthrough_gifts()
        return parse_gifts.get_ytd_gifts(all_passthrough_gifts)
################################
    def all_direct_gifts_response(self):
        """Returns all direct gifts by those in portfolio as request response"""
        if self.direct == None:
            self.direct = gifts.get_all_direct(self.contact_ids(),self.bearer_token)
        return self.direct
################################
    def all_direct_gifts(self):
        """Returns pandas DataFrame of response from all_direct_gifts"""
        response = self.all_direct_gifts_response()
        return pd.DataFrame(response.json()["list"])
################################
    def direct_gifts_last_year(self):
        """Returns pandas DataFrame of last year to date passthrough gifts"""
        all_direct_gifts = self.all_direct_gifts()
        return parse_gifts.get_last_year_gifts(all_direct_gifts)
################################
    def direct_gifts_lytd(self):
        """Returns pandas DataFrame of last year to date direct gifts"""
        all_direct_gifts = self.all_direct_gifts()
        return parse_gifts.get_lytd_gifts(all_direct_gifts)
################################
    def direct_gifts_ytd(self):
        """Returns pandas DataFrame of year to date direct gifts"""
        all_direct_gifts = self.all_direct_gifts()
        return parse_gifts.get_ytd_gifts(all_direct_gifts)
################################
    def comparison_by_contact(self, contact_fields=["id", "contactName", "owner"]):
        """Returns pandas DataFrame of contact info and ytd vs lytd"""
        #Filter for gifts by type
        passthrough_last_year = self.passthrough_gifts_last_year()
        passthrough_lytd = self.passthrough_gifts_lytd()
        passthrough_ytd = self.passthrough_gifts_ytd()
        direct_last_year = self.direct_gifts_last_year()
        direct_lytd = self.direct_gifts_lytd()
        direct_ytd = self.direct_gifts_ytd()
        #Sum gift amounts by contact
        passthrough_last_year_by_contact = amount_by_contact(passthrough_last_year,"contactPassthroughId")
        passthrough_lytd_by_contact = amount_by_contact(passthrough_lytd,"contactPassthroughId")
        passthrough_ytd_by_contact = amount_by_contact(passthrough_ytd,"contactPassthroughId")
        direct_last_year_by_contact = amount_by_contact(direct_last_year,"contactId")
        direct_lytd_by_contact = amount_by_contact(direct_lytd,"contactId")
        direct_ytd_by_contact = amount_by_contact(direct_ytd,"contactId")
        #Get full contact list
        contacts = self.contact_df()[contact_fields]
        #Join all dataframes on contact id / passthrough contact id
        contacts = contacts.join(passthrough_last_year_by_contact, on="id",rsuffix="_passthrough_last_year")
        contacts = contacts.join(direct_last_year_by_contact, on="id",rsuffix="_direct_last_year")
        contacts = contacts.join(passthrough_lytd_by_contact, on="id",rsuffix="_passthrough_lytd")
        contacts = contacts.join(direct_lytd_by_contact, on="id",rsuffix="_direct_lytd")
        contacts = contacts.join(passthrough_ytd_by_contact, on="id",rsuffix="_passthrough_ytd")
        contacts = contacts.join(direct_ytd_by_contact, on="id",rsuffix="_direct_ytd")
        #Some clean up
        contacts.columns = ["Id","Contact Name","Owner","Last Year Passthrough","Last Year Direct","LYTD Passthrough","LYTD Direct","YTD Passthrough","YTD Direct"]
        contacts.fillna(0,inplace=True)
        contacts["Last Year Total"] = contacts["Last Year Passthrough"] + contacts["Last Year Direct"]
        contacts["LYTD Total"] = contacts["LYTD Passthrough"] + contacts["LYTD Direct"]
        contacts["YTD Total"] = contacts["YTD Passthrough"] + contacts["YTD Direct"]
        return contacts[["Id","Contact Name","Owner","Last Year Total","LYTD Total","YTD Total"]]

def main():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    filename = "Archive/Portfolio Giving Comparison " + today + ".csv"
    p = Portfolio()
    p.comparison_by_contact().to_csv(filename,index=False)

if __name__ == '__main__':
    main()
