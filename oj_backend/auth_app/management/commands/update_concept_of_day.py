from django.core.management.base import BaseCommand
from django.utils import timezone
from auth_app.models import ConceptOfDay


class Command(BaseCommand):
    help = 'Update Concept of the Day (rotates daily)'

    def handle(self, *args, **options):
        concepts = [
            {
                'title': 'Dynamic Programming',
                'description': (
                    'Dynamic Programming is a method for solving complex problems by breaking them down into '
                    'simpler subproblems and reusing solutions.'
                ),
                'example_code': 'def fib(n):\n    dp = [0, 1]\n    for i in range(2, n+1):\n        dp.append(dp[-1]+dp[-2])\n    return dp[n]'
            },
            {
                'title': 'Binary Search',
                'description': (
                    'Binary Search efficiently finds an element position in a sorted array by halving the search '
                    'space each step (O(log n)).'
                ),
                'example_code': 'def bs(a,x):\n    l,r=0,len(a)-1\n    while l<=r:\n        m=(l+r)//2\n        if a[m]==x:return m\n        if a[m]<x:l=m+1\n        else:r=m-1\n    return -1'
            },
            {
                'title': 'Two Pointers Technique',
                'description': (
                    'Use two indices moving over the data structure to solve problems in linear time, such as '
                    'pair sums, deduplication, and palindrome checks.'
                ),
                'example_code': 'def two_sum_sorted(a,t):\n    i,j=0,len(a)-1\n    while i<j:\n        s=a[i]+a[j]\n        if s==t:return i,j\n        if s<t:i+=1\n        else:j-=1\n    return -1,-1'
            },
            {
                'title': 'Sliding Window',
                'description': (
                    'Maintain a moving subarray/substring window to compute aggregates in O(n) by expanding '
                    'and shrinking the window.'
                ),
                'example_code': 'def max_sum_k(a,k):\n    cur=sum(a[:k]);ans=cur\n    for i in range(k,len(a)):\n        cur+=a[i]-a[i-k];ans=max(ans,cur)\n    return ans'
            },
            {
                'title': 'Graph Traversal (BFS/DFS)',
                'description': 'Explore graph nodes using BFS (level-order) or DFS (depth-first) for reachability and paths.',
                'example_code': 'from collections import deque\n\ndef bfs(g,s):\n    vis=set([s]);q=deque([s])\n    while q:\n        u=q.popleft()\n        for v in g[u]:\n            if v not in vis: vis.add(v); q.append(v)'
            },
        ]

        today = timezone.now().date()
        idx = today.timetuple().tm_yday % len(concepts)
        selected = concepts[idx]

        concept, created = ConceptOfDay.objects.get_or_create(
            id=1,
            defaults={
                'title': selected['title'],
                'description': selected['description'],
                'example_code': selected.get('example_code', ''),
            }
        )

        if not created:
            concept.title = selected['title']
            concept.description = selected['description']
            concept.example_code = selected.get('example_code', '')
            concept.save()

        self.stdout.write(self.style.SUCCESS(f"Concept of the Day set to: {selected['title']}"))