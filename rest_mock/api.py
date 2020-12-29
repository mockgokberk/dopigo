from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone as dt
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from .models import Account, BalanceHistory, Customer
from .serializers import (AccountSerializer, BalanceHistorySerializer,
                          CustomerSerializer)



class CustomerViewSet(viewsets.ViewSet):
    """
    Customer Api endpoint.
    """
    def list(self, request):
        """
        Returns a list of all customers in the system.

        [ref]: GET http://127.0.0.1/api/customers
        """
        queryset = Customer.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        """
        Returns selected customer.

        [ref]: GET http://127.0.0.1/api/customers/{id}
        """
        queryset = Customer.objects.all()
        customer = get_object_or_404(queryset, id=id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request):
        """
        Creates customer.

        [ref]: POST http://127.0.0.1/api/customers/
               Parameters:
                   name : str
        """
        serializer = CustomerSerializer(request.data)
        Customer(**serializer.data).save()
        return Response(data="Success")


class AccountsViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Returns a list of all accounts in the system.

        [ref]: GET http://127.0.0.1/api/accounts
        """
        queryset = Account.objects.all()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        """
        Returns selected account.

        [ref]: GET http://127.0.0.1/api/accounts/{id}
        """
        queryset = Account.objects.all()
        account = get_object_or_404(queryset, id=id)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def create(self, request):
        """
        Creates account.

        [ref]: POST http://127.0.0.1/api/customers/
               Parameters:
                   customer_id(FK): Integer
                   depozit: Float
        """
        print(request.data)
        serializer = AccountSerializer(request.data)
        Account(**serializer.data).save()

        return Response(data="Success")


class BalanceHistoryViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Returns a list of all account transfer history.

        [ref]: GET http://127.0.0.1/api/history_balance
        """
        queryset = BalanceHistory.objects.all()
        serializer = BalanceHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        """
        Returns a list of one account transfer history.

        [ref]: GET http://127.0.0.1/api/history_balance/{account_id}
        """
        queryset = BalanceHistory.objects.all()
        balance_history = get_object_or_404(queryset, account_id=id)
        serializer = BalanceHistorySerializer(balance_history)
        return Response(serializer.data)


class TransferBalance(views.APIView):

    def post(self, request, *args, **kwargs):
        """
        Transfer Balances 'from account' to 'to_account'
        if has enough balance

        [ref]: POST http://127.0.0.1/api/transfer_balance
                Parameters:
                    amount : Float
                    from_account(FK): Integer
                    to_account(FK): Integer

        """

        serializer = TransferBalance(data=request.data)
        from_account = Account.objects.get(id=serializer.data["from_account"])
        to_account = Account.objects.get(id=serializer.data["to_account"])
        amount = serializer.data["amount"]

        # Check if has enough balance
        if (from_account.deposit >= amount):

            from_account.deposit = from_account.deposit - amount
            to_account.deposit = to_account.deposit + amount

            from_account.save(update_fields=['deposit'])
            to_account.save(update_fields=['deposit'])

            #Log transfer history
            BalanceHistory(
                timeslot=dt.now(),
                account=from_account,
                value=-amount).save()
            BalanceHistory(
                timeslot=dt.now(),
                account=to_account,
                value=amount).save()

            return Response({"Success": True})
        else:
            return Response({"Success": False, "Reason": "Not enough Balance"})
