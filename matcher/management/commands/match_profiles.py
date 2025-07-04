from django.core.management.base import BaseCommand
from matcher.models import UserProfile, MatchResult
from itertools import combinations

TECH_COURSES = {'csai', 'csds', 'dsai'}
NON_TECH_COURSES = {'design', 'psych', 'bba'}

def get_domain(course):
    return 'tech' if course in TECH_COURSES else 'non-tech'

def calculate_score(p1, p2):
    score = 0
    if p1.sleep_schedule == p2.sleep_schedule:
        score += 1
    score += (5 - abs(int(p1.cleanliness) - int(p2.cleanliness))) * 0.3
    if p1.introvert_extrovert == p2.introvert_extrovert:
        score += 1

    interests1 = set(p1.interests.lower().replace(" ", "").split(","))
    interests2 = set(p2.interests.lower().replace(" ", "").split(","))
    common = interests1.intersection(interests2)
    score += 0.5 * len(common)

    return round(score, 2)

class Command(BaseCommand):
    help = "Matches students based on compatibility and saves MatchResult."

    def handle(self, *args, **kwargs):
        MatchResult.objects.all().delete()
        profiles = list(UserProfile.objects.filter(is_submitted=True))
        matched_ids = set()

        def get_valid_pairs(profile_list, course_strict=True, domain_fallback=False):
            pairs = []
            for a, b in combinations(profile_list, 2):
                if a.id in matched_ids or b.id in matched_ids:
                    continue
                if a.gender != b.gender:
                    continue
                if course_strict and a.course != b.course:
                    continue
                if domain_fallback and not course_strict:
                    if get_domain(a.course) != get_domain(b.course):
                        continue
                score = calculate_score(a, b)
                pairs.append((score, a, b))
            return sorted(pairs, reverse=True, key=lambda x: x[0])

        # Phase 1: Same gender + same course
        pairs = get_valid_pairs(profiles, course_strict=True)
        # Phase 2: Same gender + same domain (tech vs non-tech)
        pairs += get_valid_pairs(profiles, course_strict=False, domain_fallback=True)
        # Phase 3: Same gender + any course (final fallback)
        pairs += get_valid_pairs(profiles, course_strict=False, domain_fallback=False)

        for score, a, b in pairs:
            if a.id in matched_ids or b.id in matched_ids:
                continue
            MatchResult.objects.create(student1=a, student2=b, score=score)
            matched_ids.add(a.id)
            matched_ids.add(b.id)
            self.stdout.write(self.style.SUCCESS(f"✅ Matched {a.email} 🤝 {b.email} (Score: {score})"))

        # Final unmatched check (odd-number case)
        for p in profiles:
            if p.id not in matched_ids:
                self.stdout.write(self.style.WARNING(f"⚠️ No match for {p.email}"))
