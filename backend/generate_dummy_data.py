import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from matcher.models import UserProfile, StudentUser
from django.contrib.auth.hashers import make_password

INDIAN_FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Aryan", "Krishna", "Ishaan", "Shaurya", "Atharva", "Dhruv", "Rudra", "Rishi", "Samar", "Kabir", "Aarush", "Ayush", "Ansh", "Anurag", "Siddharth", "Karan", "Rohit", "Vikram", "Neha", "Priya", "Rahul", "Sneha", "Kiran", "Aditi", "Isha", "Riya", "Aanya", "Aaradhya", "Ananya", "Diya", "Kavya", "Myra", "Navya", "Prisha", "Sara", "Shanaya", "Suhana", "Zara", "Ayesha", "Fatima", "Pooja", "Raj", "Vijay"]
INDIAN_LAST_NAMES = ["Sharma", "Patel", "Singh", "Kumar", "Gupta", "Desai", "Joshi", "Chawla", "Mehta", "Bose", "Das", "Reddy", "Verma", "Kapoor", "Chopra", "Chauhan", "Nair", "Iyer", "Rao", "Naidu", "Agarwal", "Mishra", "Pandey"]

COURSES = ['csai', 'csds', 'dsai', 'design', 'psych', 'bba']
GENDERS = ['male', 'female']
SLEEP_SCHEDULES = ['Night Owl', 'Early Bird', 'Regular']
PERSONALITIES = ['Introvert', 'Ambivert', 'Extrovert']
INTERESTS_LIST = ['coding', 'anime', 'football', 'music', 'reading', 'movies', 'gaming', 'traveling', 'gym', 'photography', 'art', 'cooking', 'cricket', 'dance']

def generate():
    for i in range(50):
        first_name = random.choice(INDIAN_FIRST_NAMES)
        last_name = random.choice(INDIAN_LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{i}@rishihood.edu.in"
        
        if not StudentUser.objects.filter(email=email).exists():
            StudentUser.objects.create(
                email=email,
                password=make_password('password123'),
                is_verified=True,
                has_submitted_form=True
            )
        
        if not UserProfile.objects.filter(email=email).exists():
            interests = ", ".join(random.sample(INTERESTS_LIST, k=random.randint(3, 6)))
            UserProfile.objects.create(
                email=email,
                full_name=full_name,
                sleep_schedule=random.choice(SLEEP_SCHEDULES),
                cleanliness=random.randint(1, 5),
                introvert_extrovert=random.choice(PERSONALITIES),
                interests=interests,
                is_submitted=True,
                gender=random.choice(GENDERS),
                course=random.choice(COURSES)
            )

if __name__ == "__main__":
    generate()
    print("50 Dummy profiles generated successfully!")
