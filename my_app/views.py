from django.shortcuts import render
from my_app.models import NewUser , TodoItems
from rest_framework.views import APIView
from my_app.serializers import NewUserSerializer,LoginSerializer,PasswordUpdateSerializer, TodoItemsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import jwt,datetime
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed



class SignUp(APIView):
    
    def post(self,request):
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            
            if not request.data:
                return Response({"Message":"Request Body is Empty Can Not Post Empty Body!"})
            
            #Get All Fields and Check Validity....
            username = serializer.validated_data.get("username")
            f_name = serializer.validated_data.get("first_name")
            l_name = serializer.validated_data.get("last_name")
            email =  serializer.validated_data.get("email")
            address = serializer.validated_data.get("Address")
            password = serializer.validated_data.get("password")
            pass2 = serializer.validated_data.get("password_again")
            
            if username is None:
                return Response("UserName Required!")
            if f_name is None:
                return Response("First Name Required!")
            
            if l_name is None:
                return Response("Last Name Required!")
            if email is None:
                return Response("Email is Required!")
            if address is None:
                return Response("Address is Required!")
            if password is None:
                return Response("Password is Required!")
            if pass2 is None:
                return Response("Confirmation Password Not Provided")
            
            if password != pass2:
                return Response("Password and Confirmation Password Doesnt Match!")
            else:
                serializer.save()
                return Response({"New User Added SuccessFully!":serializer.data})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            
            if not request.data:
                return Response("No Credentials Provided!")
            if email is None:
                return Response("Email is Required!")
            if password is None:
                return Response("Password is Required!")
            else:
                user = NewUser.objects.filter(email=email, password=password).first()    
                if user:
                    serializer = NewUserSerializer(user)
                    if serializer:
                        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                        payload = jwt_payload_handler(user)
                        token = jwt_encode_handler(payload)
                        response = Response()
                        response.set_cookie(key='jwt',value=token,httponly=True)
                        response.data = {
                            "jwt" : token,  
                            "User" : serializer.data
                        }
                        # return Response({"Login Success": "Welcome", "User": serializer.data, "Token": token,"respone":response})
                        return response
                else:
                    return Response("Wrong Credentials")
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GetUser(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        
        if token:
            try:
                payload = api_settings.JWT_DECODE_HANDLER(token)
                user_id = payload['user_id']
                user = NewUser.objects.get(id=user_id)
                serializer = NewUserSerializer(user)
                return Response({"Authenticated Successfully Here is The Data:":serializer.data})
            except jwt.ExpiredSignature:
                return Response({"error": "Token has expired"}, status=status.HTTP_403_FORBIDDEN)
            except jwt.DecodeError:
                return Response({"error": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Token not provided,Unauthenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class LogoutUser(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "Message" : "Logout Success! Token Deleted!"
        }
        
        return response
    


class GetEmail(APIView):
    def get(self,request):
        token = request.COOKIES.get("jwt")
        if token:
            payload = api_settings.JWT_DECODE_HANDLER(token)
            id = payload["user_id"]
            user = NewUser.objects.filter(id = id).first()
            if user:
                serializer  = NewUserSerializer(user)
                my_Email = serializer.data["email"]
                return Response({"User Authenticated Here is The Email":my_Email})
            else:
                return Response("No User Found!")
        
        else:
            return Response("No Token Provided!")



class UpdatePassword(APIView):
    def post(self, request):
        token = request.COOKIES.get("jwt")
        passSerializer = PasswordUpdateSerializer(data=request.data)
        
        if passSerializer.is_valid():
            pass1 = passSerializer.validated_data.get("password")
            pass2 = passSerializer.validated_data.get("password_again")
        
            if token:
                payload = api_settings.JWT_DECODE_HANDLER(token)
                my_id = payload["user_id"]
                user = NewUser.objects.filter(id=my_id).first()
                
                if user:
                    user.password = pass1
                    user.password_again = pass2
                    user.save()
                    serializer = NewUserSerializer(user)
                    # serializer.data["password"] = pass1
                    # serializer.data["password_again"] = pass2
                    # user.save()
                    return Response({"New Password Saved": serializer.data})
                else:
                    return Response("No User Found!")
            else:
                return Response("No Token Found!")
        else:
            return Response(passSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



########## API for adding New Todo Task ############
class AddTask(APIView):
    def post(self,request):
        token = request.COOKIES.get("jwt")
        if token:
            my_serializer = TodoItemsSerializer(data=request.data)
            if not request.data:
                return Response("Request Body is Empty!")
            elif my_serializer.is_valid():
                task_name = my_serializer.validated_data.get("task_name")   
                if not task_name:
                    return Response("Task Name Required!")
                due_date = my_serializer.validated_data.get("due_date")
                if not due_date:
                    return Response("Due Date Required!")
                task_type = my_serializer.validated_data.get("task_type")
                if not task_type:
                    return Response("Task Type Required!")
                
                else:
                    my_serializer.save()
                    return Response({"Message":"News Task Added","Information":my_serializer.data})
                    
            else:
                return Response(my_serializer.errors)
        
        else:
            return Response("Session Ended! Login to add New Tasks!")
        

class GetTodoItems(APIView):
    def get(self,request):
        token = request.COOKIES.get("jwt")
        if token:
            payload = api_settings.JWT_DECODE_HANDLER(token)
            my_id = payload.get("user_id")
            if my_id:
                items = TodoItems.objects.all()
                if items:
                    serializer = TodoItemsSerializer(items,many=True)
                    return Response({"Todo Items": serializer.data})
                else:
                    return Response("No Todo Items Available!")
            else:
                return Response("No user_Id Available!")
        
        else:
            return Response({"Message":"Session Expired Login Again to Fetch todo Items!"})