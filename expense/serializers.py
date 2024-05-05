from rest_framework import serializers
from .models import UserModel, Expense

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'first_name', 'last_name', 'last_login']

class ExpenseSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()  # Nested serializer for the user field

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'date', 'text', "transtype", 'category', 'subcategory', 'payment_mode']
