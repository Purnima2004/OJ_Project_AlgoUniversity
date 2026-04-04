from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from accounts.models import UserProfile
from judge.models import Problem, Contest, Submission
from .models import ConceptOfDay


def ensure_concept_of_day_current():
    """Ensure ConceptOfDay entry reflects today's concept.
    This runs quickly on each dashboard load so the concept rotates daily
    even if the background task isn't scheduled.
    """
    concepts = [
        {
            'title': 'Dynamic Programming',
            'description': (
                'Dynamic Programming solves complex problems by breaking them into '
                'overlapping subproblems and reusing results.'
            ),
            'example_code': 'def fib(n):\n    dp=[0,1]\n    for _ in range(2,n+1): dp.append(dp[-1]+dp[-2])\n    return dp[n]'
        },
        {
            'title': 'Binary Search',
            'description': 'Find target in sorted data by halving the search space (O(log n)).',
            'example_code': 'def bs(a,x):\n    l,r=0,len(a)-1\n    while l<=r:\n        m=(l+r)//2\n        if a[m]==x:return m\n        if a[m]<x:l=m+1\n        else:r-=1\n    return -1'
        },
        {
            'title': 'Two Pointers Technique',
            'description': 'Use two indices to scan arrays/strings in linear time for pair problems.',
            'example_code': 'def two_sum_sorted(a,t):\n    i,j=0,len(a)-1\n    while i<j:\n        s=a[i]+a[j]\n        if s==t:return i,j\n        if s<t:i+=1\n        else:j-=1\n    return -1,-1'
        },
        {
            'title': 'Sliding Window',
            'description': 'Maintain a moving subarray/substring to compute aggregates in O(n).',
            'example_code': 'def max_sum_k(a,k):\n    cur=sum(a[:k]);ans=cur\n    for i in range(k,len(a)):\n        cur+=a[i]-a[i-k];ans=max(ans,cur)\n    return ans'
        },
        {
            'title': 'Graph Traversal (BFS/DFS)',
            'description': 'Explore graph nodes for reachability and shortest paths.',
            'example_code': 'from collections import deque\n\ndef bfs(g,s):\n    vis=set([s]);q=deque([s])\n    while q:\n        u=q.popleft()\n        for v in g[u]:\n            if v not in vis: vis.add(v); q.append(v)'
        },
    ]

    today = timezone.now().date()
    index = today.timetuple().tm_yday % len(concepts)
    selected = concepts[index]

    # Single row with id=1 acts as the current concept
    concept, created = ConceptOfDay.objects.get_or_create(
        id=1,
        defaults={
            'title': selected['title'],
            'description': selected['description'],
            'example_code': selected.get('example_code', ''),
        }
    )
    if not created and (
        concept.title != selected['title'] or
        concept.description != selected['description'] or
        concept.example_code != selected.get('example_code', '')
    ):
        concept.title = selected['title']
        concept.description = selected['description']
        concept.example_code = selected.get('example_code', '')
        concept.save()


def home(request):
    # If user is not authenticated, show landing page
    if not request.user.is_authenticated:
        return render(request, 'landing/landing.html')

    # If user is authenticated, show dashboard
    ensure_concept_of_day_current()
    now = timezone.now()
    active_contests = Contest.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    )[:3]
    active_contests_count = Contest.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).count()
    concept_of_day = ConceptOfDay.objects.first()

    context = {
        'contests': active_contests,
        'active_contests_count': active_contests_count,
        'total_contests': active_contests_count,
        'concept_of_day': concept_of_day,
        'total_problems': Problem.objects.count(),
        'total_users': User.objects.count(),
        'total_submissions': Submission.objects.count(),
    }
    return render(request, 'home/home.html', context)
