from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationSerializer, SigninSerializer
from users.models import User
from SubscriptionPlan.models import SubscriptionPlan
from django.urls import get_resolver
from django.http import JsonResponse


def home_page(request):
    return redirect('/admin/')
    # return render(request, 'homePage/home.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data.get('password', None)
        print(f"Registering user: {username}, Phone: {phone_number}")

        # Retrieve the default subscription plan
        try:
            default_plan = SubscriptionPlan.objects.get(id=1)
            print(f"Default subscription plan: {default_plan}")
        except SubscriptionPlan.DoesNotExist:
            return Response(
                {'error': 'Default subscription plan not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the new user using the custom manager
        new_user = User.objects.create_user(
            phone_number=phone_number,
            username=username,
            password=password,
            subscription_plan=default_plan
        )
        print(f"User created: {new_user}")

        # Generate a token for the new user
        token, created = Token.objects.get_or_create(user=new_user)
        print(f"Token: {token.key}, Created: {created}")

        return Response(
            {
                'success': 'Registration successful! Now you can sign in.',
                'user': {
                    'username': new_user.username,
                    'phone_number': new_user.phone_number,
                    'subscription_plan': new_user.subscription_plan.name,
                    'token': token.key
                }
            },
            status=status.HTTP_201_CREATED
        )

    print(f"Registration errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    serializer = SigninSerializer(data=request.data)

    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        password = request.data.get('password', None)
        print(f"Signing in user with phone: {phone_number}")

        # Retrieve the user based on phone number
        try:
            user = User.objects.get(phone_number=phone_number)
            print(f"User found: {user}")
        except User.DoesNotExist:
            return Response(
                {'error': 'User does not exist. Please register first.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate password if provided
        if password:
            if not user.check_password(password):
                return Response(
                    {'error': 'Incorrect password.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Generate or retrieve the token for the user
        token, created = Token.objects.get_or_create(user=user)
        print(f"Token: {token.key}, Created: {created}")

        return Response(
            {
                'success': 'Sign in successful!',
                'user': {
                    'username': user.username,
                    'phone_number': user.phone_number,
                    'subscription_plan': user.subscription_plan.name,
                    'token': token.key
                }
            },
            status=status.HTTP_200_OK
        )

    print(f"Sign-in errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({f'User {request.user.username} logged out successfully!'}, status=status.HTTP_200_OK)
