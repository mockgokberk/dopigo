from django.test import TestCase
from rest_framework.test import APIClient

from .models import Account, Customer


class TestModels(TestCase):

    def setUp(self):
        """
        Models setup. Creates customers and accounts
        """
        c1 = Customer.objects.create(**{"id": 1, "name": "Arisha Barron"})
        c2 = Customer.objects.create(**{"id": 2, "name": "Branden Gibson"})
        c3 = Customer.objects.create(**{"id": 3, "name": "Rhonda Church"})
        c4 = Customer.objects.create(**{"id": 4, "name": "Georgina Hazel"})

        customer_list = [c1, c2, c3, c4]

        for i in range(1, 5):
            for x in range(i):
                Account.objects.create(**{"deposit": i * 10 + x, "customer": customer_list[i - 1]})

    def test_get_users(self):
        """
        Customer models get method testing.
        """
        c1 = Customer.objects.get(id=1)
        self.assertEqual(c1.name, "Arisha Barron")

    def test_get_accounts(self):
        """
        Account models get method testing.
        """
        c1 = Account.objects.all()
        self.assertEqual(len(c1), 10)


class TestDrf(TestCase):
    """
    Api endpoints tests
    """

    def setUp(self):
        """
        Create customers and accounts using DRF.
        """
        self.factory = APIClient()
        self.factory.post('/api/customers', {"id": 1, "name": "Arisha Barron"})
        self.factory.post('/api/customers', {"id": 2, "name": "Branden Gibson"})

        self.accounts = [
            {"id": 1, "deposit": 100, "customer_id": 1},
            {"id": 2, "deposit": 10, "customer_id": 1},
            {"id": 3, "deposit": 150, "customer_id": 2},
            {"id": 4, "deposit": 15, "customer_id": 2}
        ]

        for a in self.accounts:
            self.factory.post('/api/accounts', a, format='json')

    def test_users(self):
        """
        DRF get customers method test
        """
        response = self.factory.get('/api/customers')
        self.assertEqual(len(response.json()), 2)

    def test_accounts(self):
        """
        DRF get accounts method test
        """
        response = self.factory.get('/api/accounts')
        self.assertEqual(len(response.json()), 4)

    def test_transfer(self):
        """
        DRF transfer balance method test

        Tests the transfer between accounts and checks if the history log is correct
        """
        amount = 50
        from_account = self.accounts[0]
        to_account = self.accounts[2]
        response = self.factory.post('/api/transfer_balance',
                                     {"amount": amount,
                                      "from_account": from_account["id"],
                                      "to_account": to_account["id"]},
                                     format='json')
        self.assertTrue(response.json()["Success"])
        response = self.factory.get('/api/accounts/' + str(from_account["id"]))
        self.assertEqual(
            response.json()["deposit"],
            from_account["deposit"] - amount)
        response = self.factory.get('/api/accounts/' + str(to_account["id"]))
        self.assertEqual(
            response.json()["deposit"],
            to_account["deposit"] + amount)
        response = self.factory.get('/api/history_balance/' + str(from_account["id"]))
        self.assertEqual(response.json()["value"], -amount)
        self.assertEqual(response.json()["account_id"], from_account["id"])

    def test_failed_transfer(self):
        """
        DRF transfer balance method fail test

        Tests the failed transfer between accounts and checks if the history log is correct
        """
        amount = 150
        from_account = self.accounts[0]
        to_account = self.accounts[2]
        response = self.factory.post('/api/transfer_balance',
                                     {"amount": amount,
                                      "from_account": from_account["id"],
                                      "to_account": to_account["id"]},
                                      format='json')

        self.assertFalse(response.json()["Success"])
        response = self.factory.get('/api/accounts/' + str(from_account["id"]))
        self.assertEqual(response.json()["deposit"], from_account["deposit"])
        response = self.factory.get('/api/accounts/' + str(to_account["id"]))
        self.assertEqual(response.json()["deposit"], to_account["deposit"])

        response = self.factory.get('/api/history_balance')
        self.assertEqual(response.json(), [])
