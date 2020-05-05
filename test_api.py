import os
import time
from unittest import TestCase, skip

from api import BankApi



class ApiTestNewObject(TestCase):
    def test_create_api_object(self):
        ba = BankApi()
        self.assertEqual('/ASO/TechArchitecture/grantingTickets/V02', ba.LOGIN_URL)

    def test_requests_session_creation(self):
        ba = BankApi()
        self.assertEqual(ba.session.headers['Content-Type'], 'application/json')


#@skip('No login test required now')
class ApiTestLogin(TestCase):
    def test_login_wrong_credentials_403(self):
        test_user = '93847582K'
        test_password = '1234'
        ba = BankApi()
        response_data = ba.login(test_user, test_password)
        self.assertEqual(403, response_data['http-status'])

    def test_login_system_credentials_200_and_saves_info(self):
        user = os.environ['B_AC']
        password = os.environ['B_AP']
        ba = BankApi()
        response_data = ba.login(user, password)
        self.assertEqual('OK', response_data['authenticationState'])
        # Tsec header and user id needed for every other call
        self.assertTrue(ba.session.headers['tsec'])
        self.assertTrue(ba.userid)
        self.assertTrue(len(ba.userid) > 10)


class ApiTestGetRequests(TestCase):
    def setUp(self):
        user = os.environ['B_AC']
        password = os.environ['B_AP']
        self.ba = BankApi()
        self.ba.login(user, password)

    def test_get_customer_data(self):
        customer_data = self.ba.get_customer_data()
        self.assertTrue(customer_data['customer']['isCustomer'])

    def test_get_financial_dashboard(self):
        dashboard_data = self.ba.get_financial_dashboard()
        self.assertTrue(dashboard_data['assetBalance']['amount'] > -1)

