from django.contrib.auth.models import Group, User
from rest_framework import serializers

from . import models
from .models import Account, BalanceHistory, Customer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name']


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'deposit', 'customer_id']


class BalanceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BalanceHistory
        fields = ['id', 'timeslot', 'account_id', 'value']


class TransferBalance(serializers.Serializer):
    from_account = serializers.IntegerField(
        source='from_account', read_only=True)
    to_account = serializers.IntegerField(source='to_account', read_only=True)
    amount = serializers.IntegerField(source='amount', read_only=True)
