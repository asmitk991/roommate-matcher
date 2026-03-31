from rest_framework import generics
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile, MatchResult, COURSE_CHOICES
from .models import EmailOTP
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password, check_password
from .models import StudentUser
import jwt  # type: ignore
from django.conf import settings
from datetime import datetime, timedelta, timezone
from rest_framework import status
import logging



 
class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        print("🔥 Incoming data:", request.data)

        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Authentication required. Please log in.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            token_email = payload.get('email', '').strip().lower()
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return Response({'error': 'Invalid or expired token. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)

        email = request.data.get('email', '').strip().lower()

        if email != token_email:
            return Response({"error": "You can only submit the profile for your own registered email."}, status=status.HTTP_403_FORBIDDEN)

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

            similarities = []
            if profile.sleep_schedule.lower() == matched_with.sleep_schedule.lower():
                similarities.append(f"You are both {profile.sleep_schedule}s")
            
            if profile.cleanliness == matched_with.cleanliness:
                similarities.append(f"You both have a cleanliness rating of {profile.cleanliness}")
            
            if profile.introvert_extrovert.lower() == matched_with.introvert_extrovert.lower():
                similarities.append(f"You are both {profile.introvert_extrovert}s")

            if profile.course.lower() == matched_with.course.lower():
                course_display = dict(COURSE_CHOICES).get(profile.course, profile.course)
                similarities.append(f"You are both studying {course_display}")

            data = {
                "you": profile.full_name,
                "matched_with": matched_with.full_name,
                "matched_email": matched_with.email,
                "score": match.score,
                "common_interests": common_interests,
                "similarities": similarities
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



import logging
logger = logging.getLogger(__name__)

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        logger.info(f"SendOTP called with email: {email}")
        
        if not email or not email.endswith('rishihood.edu.in'):
            logger.info("Failed domain check")
            return Response({"error": "Invalid email domain"}, status=400)

        if StudentUser.objects.filter(email=email).exists():
            logger.info("Account already exists")
            return Response({"error": "Account already exists. Please log in."}, status=400)

        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(email=email, defaults={"otp": otp})

        try:
            send_mail(
                subject="Your Roommate Matcher OTP",
                message=f"Your OTP is: {otp}",
                from_email=settings.EMAIL_HOST_USER,  # Use the authenticated email
                recipient_list=[email],
                fail_silently=False,
            )
            logger.info("Email sent successfully")
        except Exception as e:
            logger.error(f"send_mail failed: {e}")
            return Response({"error": f"Email sending failed: {str(e)}"}, status=400)

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
                # Create or update StudentUser
                user, created = StudentUser.objects.get_or_create(email=email)
                user.is_verified = True
                user.save()

                # Clean up the OTP record once it's used
                record.delete()

                return Response({"verified": True, "email": email}, status=200)
            else:
                return Response({"error": "Invalid OTP"}, status=400)

        except EmailOTP.DoesNotExist:
            return Response({"error": "No OTP found for this email"}, status=404)

class SetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': 'Password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = StudentUser.objects.get(email=email, is_verified=True)
            user.password = make_password(password)
            user.save()

            # Generate JWT
            payload = {
                'email': user.email,
                'exp': datetime.now(timezone.utc) + timedelta(days=7),
                'iat': datetime.now(timezone.utc),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({'message': 'Password set successfully', 'token': token}, status=status.HTTP_200_OK)

        except StudentUser.DoesNotExist:
            return Response({'error': 'User not verified or does not exist'}, status=status.HTTP_404_NOT_FOUND)

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
                    'exp': datetime.now(timezone.utc) + timedelta(days=7),
                    'iat': datetime.now(timezone.utc),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({'token': token, 'email': user.email}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        except StudentUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
