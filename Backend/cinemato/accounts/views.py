# cookieapp/views.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from twilio.rest import Client
# from cinemato import settings as project_settings
import cinemato.settings as project_settings





from .serializers import RequestOTPSerializer,VerifyOTPSerializer
from .models import User, OTP
from django.core.mail import send_mail


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
        

class HomeView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    def get(self, request, format=None):
        # Your logic here
        return Response({"message": "Welcome to the home page!"}, status=status.HTTP_200_OK)
    

class RequestOTPView(APIView):

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.create_otp(serializer.validated_data)

            # Send OTP via email or SMS based on the provided data
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')

            if email:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp_code}. It will expire in 20 seconds.',
                    project_settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
            elif phone:
                client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
                message = client.messages.create(
                    body=f'Your OTP is: {otp_code}',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=f'{settings.COUNTRY_CODE}{phone}'
                )
            print("success")
            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        print("Received Data:", request.data)
        
        if serializer.is_valid():
            print("Serializer is valid")
            user = serializer.create_user(serializer.validated_data)
            
            if user is not None:
                if user.is_active:
                    response = Response()
                    data = get_tokens_for_user(user)
                    response.set_cookie(
                        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                        value=data["access"],
                        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                    )
                    response.set_cookie(
                        key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
                        value=data["refresh"],
                        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                        httponly=True,
                        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                    )
                    csrf.get_token(request)
                    response.data = {"Success": "Login successfully", "data": data}
                    return response
                else:
                    return Response({"No active": "This account is not active!"}, status=status.HTTP_404_NOT_FOUND)
            else:
                print("User creation failed")
        else:
            print("Serializer errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ResentOtpView(APIView):
    def post(self, request):
            serializer = RequestOTPSerializer(data=request.data)
            if serializer.is_valid():
                otp_code = serializer.create_otp(serializer.validated_data)

                # Send OTP via email or SMS based on the provided data
                email = serializer.validated_data.get('email')
                phone = serializer.validated_data.get('phone')

                if email:
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp_code}. It will expire in 20 seconds.',
                        project_settings.DEFAULT_FROM_EMAIL,
                        [email],
                    )
                elif phone:
                    client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
                    message = client.messages.create(
                        body=f'Your OTP is: {otp_code}',
                        from_=settings.TWILIO_PHONE_NUMBER,
                        to=f'{settings.COUNTRY_CODE}{phone}'
                    )
                print("success")
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




