import json
import requests
import urllib3

from time import time
from getpass import getpass



class BankApi(object):

    BASE_URL = 'https://bbva.es'
    LOGIN_URL = '/ASO/TechArchitecture/grantingTickets/V02'
    REFRESH_TSEC = '/ASO/grantingTicketActions/V01/refreshGrantingTicket/?customerId='
    CUSTOMER_DATA_URL = '/ASO/contextualData/V02/'
    FINANCIAL_DASHBOARD_URL = '/ASO/financialDashBoard/V03/?$customer.id='
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0'

    def __init__(self):
        self.create_session()
        urllib3.disable_warnings()

    def create_session(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': self.USER_AGENT,
            'Host': 'www.bbva.es'   
        })
    
    def save_tsec(self, response):
        self.session.headers['tsec'] = response.headers['tsec']
        self.last_tsec_time = time()

    def save_userid(self, response):
        self.userid = response['user']['id']

    def login(self, user, password):
        login_status = False
        payload = {
            'authentication':{
                'consumerID':'00000001',
                'authenticationType':'02',
                'userID':'0019-0' + user,
                'authenticationData':[
                    {
                        'authenticationData':[password],
                        'idAuthenticationData':'password'
                    }
                ]
            }
        }

        response = self.session.post(
            self.BASE_URL + self.LOGIN_URL,
            data=json.dumps(payload),
            verify=False
        )

        response_data = json.loads(response.text)

        # If it did not fail save tsec
        if 'http-status' not in response_data:
            self.save_tsec(response)
            self.save_userid(response_data)

        return response_data

    def refresh_tsec(self):
        response = self.session.post(
            self.BASE_URL + self.REFRESH_TSEC + self.userid,
            data=json.dumps({}),
            verify=False
        )
        self.save_tsec(response)
        return True

    def request(self, url, data=False):

        # Every 4 minutes we need a new tsec
        seconds_past = time() - self.last_tsec_time
        if seconds_past > 240:
            self.refresh_tsec()

        if data:
            response = self.session.post(
                url,
                data=json.dumps(data),
                verify=False
            )
        else:
            response = self.session.get(
                url,
                verify=False
            )

        return json.loads(response.text)


    def get_customer_data(self):
        '''
        Get your name, phone, email etc
        '''
        response = self.request(
            self.BASE_URL + self.CUSTOMER_DATA_URL + self.userid,
        )
        return response

    def get_financial_dashboard(self):
        '''
        Get balance on all contracted accounts, cards, securities etc
        '''
        response = self.request(
            self.BASE_URL + self.FINANCIAL_DASHBOARD_URL + self.userid,
        )
        return response


def main():
    DNI = input('Introduce tu DNI:')
    password = getpass('Introduce password:')
    ba = BankApi()
    ba.login(DNI, password)
    amount = ba.get_financial_dashboard()['assetBalance']['amount']
    print(f'Tienes un total de {round(amount, 2)} EUR en tu cuenta.')


if __name__ == '__main__':
    main()
   