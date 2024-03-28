from rest_framework import serializers
from my_app.models import NewUser , TodoItems

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["username","first_name","last_name","email","Address","password","password_again"]
    

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["email","password"]


class PasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["password","password_again"]


class TodoItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItems
        fields = ["task_name","due_date","task_type"]