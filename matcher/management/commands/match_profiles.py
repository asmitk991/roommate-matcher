import networkx as nx
from django.core.management.base import BaseCommand
from matcher.models import UserProfile, MatchResult
from itertools import combinations
from django.core.mail import send_mail

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
    help = "Matches students based on compatibility using Maximum Weight Graph Matching."

    def handle(self, *args, **kwargs):
        MatchResult.objects.all().delete()
        profiles = list(UserProfile.objects.filter(is_submitted=True))
        
        G = nx.Graph()
        for p in profiles:
            G.add_node(p.id, profile=p)

        for a, b in combinations(profiles, 2):
            if a.gender != b.gender:
                continue 
            
            base_score = calculate_score(a, b)
            
            # Artificial weight boosts ensure the algorithm prefers matching the same course/domain
            # before it degrades the pair simply because they have compatible hobbies!
            if a.course == b.course:
                weight = base_score + 100 
            elif get_domain(a.course) == get_domain(b.course):
                weight = base_score + 50  
            else:
                weight = base_score      
                
            G.add_edge(a.id, b.id, weight=weight, score=base_score)

        # Core optimization: Instead of greedy, we run Edmonds' Blossom algorithm!
        matching = nx.max_weight_matching(G, maxcardinality=True)
        
        matched_ids = set()
        
        for u, v in matching:
            p1 = G.nodes[u]['profile']
            p2 = G.nodes[v]['profile']
            edge_data = G.get_edge_data(u, v)
            actual_score = edge_data['score']
            
            MatchResult.objects.create(student1=p1, student2=p2, score=actual_score)
            matched_ids.add(u)
            matched_ids.add(v)
            self.stdout.write(self.style.SUCCESS(f"✅ Graph Matched {p1.email} 🤝 {p2.email} (Score: {actual_score})"))

            # Notify users that their match is ready
            email_subject = "🎉 Your Roommate Match is Ready!"
            email_body = (
                f"Great news!\n\n"
                f"The admin has just finished running the matchmaking algorithm and your roommate profile has been paired!\n"
                f"Log into the Roommate Matcher dashboard to check out who you've been matched with and see your shared habits.\n\n"
                f"- The Roommate Matcher Team"
            )
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email="noreply@roommatematcher.com",
                recipient_list=[p1.email, p2.email],
                fail_silently=True,
            )

        for p in profiles:
            if p.id not in matched_ids:
                self.stdout.write(self.style.WARNING(f"⚠️ Odd profile out: No mathematical pair for {p.email}"))
