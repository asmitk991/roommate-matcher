from django.shortcuts import render

from rest_framework import generics
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile, MatchResult
from .models import EmailOTP
from django.core.mail import send_mail
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.hashers import make_password
from .models import StudentUser 
import jwt # type: ignore
from django.conf import settings
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.parsers import JSONParser
from io import BytesIO



 
class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        print("🔥 Incoming data:", request.data)
        email = request.data.get('email', '').strip().lower()

        if not email.endswith('rishihood.edu.in'):
            print("❌ Email domain not allowed")
            return Response({"error": "Please use your college email."}, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(email=email, is_submitted=True).exists():
            print("❌ Profile already submitted")
            return Response({"error": "Profile already submitted and locked."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("❌ Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        print("✅ Created user successfully")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'email'

class MatchResultView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token missing'}, status=401)

        try:
            # Decode token to get email
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload.get('email')

            # Get UserProfile, not StudentUser
            profile = UserProfile.objects.get(email=email)

            try:
                # Match if student is in student1
                match = MatchResult.objects.get(student1=profile)
                matched_with = match.student2
            except MatchResult.DoesNotExist:
                # Try the reverse
                match = MatchResult.objects.get(student2=profile)
                matched_with = match.student1

            # Common interest logic
            common_interests = list(
                set(map(str.strip, profile.interests.lower().split(','))).intersection(
                    set(map(str.strip, matched_with.interests.lower().split(',')))
                )
            )

            data = {
                "you": profile.full_name,
                "matched_with": matched_with.full_name,
                "matched_email": matched_with.email,
                "score": match.score,
                "common_interests": common_interests
            }
            return Response(data)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)
        except MatchResult.DoesNotExist:
            return Response({'error': 'No match found yet'}, status=404)



class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email.endswith('rishihood.edu.in'):
            return Response({"error": "Invalid email domain"}, status=400)

        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(email=email, defaults={"otp": otp})

        if StudentUser.objects.filter(email=email).exists():
            return Response({"error": "Account already exists. Please log in."}, status=400)

        # Replace with your email backend setup
        send_mail(
            subject="Your Roommate Matcher OTP",
            message=f"Your OTP is: {otp}",
            from_email="noreply@roommatematcher.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent"}, status=200)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            record = EmailOTP.objects.get(email=email)
            if not record.is_valid():
                return Response({"error": "OTP expired"}, status=400)

            if record.otp == otp:
                # ✅ Create or update StudentUser
                user, created = StudentUser.objects.get_or_create(email=email)
                user.is_verified = True
                user.save()

                return Response({"verified": True, "email": email}, status=200)
            else:
                return Response({"error": "Invalid OTP"}, status=400)

        except EmailOTP.DoesNotExist:
            return Response({"error": "No OTP found for this email"}, status=404)

@csrf_exempt
def set_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            from .models import StudentUser
            user = StudentUser.objects.get(email=email, is_verified=True)
            from django.contrib.auth.hashers import make_password
            user.password = make_password(password)
            user.save()

            # 🔐 Generate JWT
            payload = {
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(days=7),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({'message': 'Password set successfully', 'token': token}, status=200)

        except StudentUser.DoesNotExist:
            return JsonResponse({'error': 'User not verified or does not exist'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

class GetMeView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Token missing"}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload.get('email', '').strip().lower()

            # Still fetch StudentUser to validate token
            StudentUser.objects.get(email=email)

            # Fetch UserProfile for form status
            profile = UserProfile.objects.filter(email=email).first()
            return Response({
                'email': email,
                'has_submitted_form': profile.is_submitted if profile else False
            })
        except (jwt.ExpiredSignatureError, jwt.DecodeError, StudentUser.DoesNotExist):
            return Response({'detail': 'Invalid or expired token'}, status=401)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = StudentUser.objects.get(email=email)
            if not user.is_verified:
                return Response({'error': 'Email not verified'}, status=status.HTTP_403_FORBIDDEN)

            if check_password(password, user.password):
                payload = {
                    'email': user.email,
                    'exp': datetime.utcnow() + timedelta(days=7),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({'token': token, 'email': user.email}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        except StudentUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
