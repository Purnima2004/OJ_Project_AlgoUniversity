from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from auth_app.models import ConceptOfDay

class Command(BaseCommand):
    help = 'Update concept of the day with daily changing programming topics'

    def handle(self, *args, **options):
        # Daily programming concepts with explanations
        concepts = [
            {
                'title': 'Dynamic Programming',
                'content': 'Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems. It stores the results of subproblems to avoid redundant calculations.\n\nKey concepts:\n• Memoization: Storing results of expensive function calls\n• Tabulation: Building solutions bottom-up\n• Optimal substructure: Optimal solution contains optimal solutions to subproblems\n\nCommon applications:\n• Fibonacci sequence\n• Longest Common Subsequence\n• Knapsack problem\n• Edit distance',
                'difficulty': 'Advanced'
            },
            {
                'title': 'Binary Search',
                'content': 'Binary Search is an efficient algorithm for finding an element in a sorted array. It works by repeatedly dividing the search interval in half.\n\nTime Complexity: O(log n)\nSpace Complexity: O(1)\n\nKey points:\n• Array must be sorted\n• Compare target with middle element\n• Eliminate half of the array in each step\n• Handle edge cases carefully\n\nVariations:\n• Finding insertion point\n• Finding first/last occurrence\n• Search in rotated array',
                'difficulty': 'Intermediate'
            },
            {
                'title': 'Graph Algorithms',
                'content': 'Graph algorithms are used to solve problems involving relationships between objects represented as nodes and edges.\n\nCommon algorithms:\n• BFS (Breadth-First Search): Level-by-level traversal\n• DFS (Depth-First Search): Explore as far as possible\n• Dijkstra: Shortest path in weighted graphs\n• Kruskal/Prim: Minimum spanning tree\n\nApplications:\n• Social networks\n• Navigation systems\n• Network routing\n• Dependency resolution',
                'difficulty': 'Advanced'
            },
            {
                'title': 'Two Pointers Technique',
                'content': 'Two Pointers is a technique where two pointers traverse an array or linked list to solve problems efficiently.\n\nCommon patterns:\n• Opposite ends: Pointers start from both ends\n• Same direction: Both pointers move in same direction\n• Fast and slow: Different speeds\n\nApplications:\n• Two Sum in sorted array\n• Remove duplicates\n• Palindrome checking\n• Merge sorted arrays\n\nTime Complexity: Usually O(n)',
                'difficulty': 'Intermediate'
            },
            {
                'title': 'Sliding Window',
                'content': 'Sliding Window is a technique for solving problems involving arrays/strings by maintaining a subset of elements.\n\nTypes:\n• Fixed size window\n• Variable size window\n• Dynamic window\n\nKey concepts:\n• Window: Subset of elements being considered\n• Expand: Add elements to window\n• Contract: Remove elements from window\n\nApplications:\n• Maximum/minimum subarray sum\n• Longest substring with k distinct characters\n• Anagrams\n• Subarray with given sum',
                'difficulty': 'Intermediate'
            },
            {
                'title': 'Recursion',
                'content': 'Recursion is a programming technique where a function calls itself to solve problems by breaking them into smaller subproblems.\n\nKey components:\n• Base case: Stopping condition\n• Recursive case: Function calls itself\n• Recursive tree: Visualization of calls\n\nTypes:\n• Linear recursion: One recursive call\n• Tree recursion: Multiple recursive calls\n• Tail recursion: Recursive call is last operation\n\nApplications:\n• Tree traversals\n• Divide and conquer\n• Backtracking\n• Dynamic programming',
                'difficulty': 'Intermediate'
            },
            {
                'title': 'Sorting Algorithms',
                'content': 'Sorting algorithms arrange elements in a specific order (ascending/descending).\n\nComparison-based sorts:\n• Bubble Sort: O(n²) - Simple but inefficient\n• Selection Sort: O(n²) - Find minimum and swap\n• Insertion Sort: O(n²) - Build sorted array\n• Merge Sort: O(n log n) - Divide and conquer\n• Quick Sort: O(n log n) average - Partition around pivot\n• Heap Sort: O(n log n) - Use heap data structure\n\nNon-comparison sorts:\n• Counting Sort: O(n+k) - Count occurrences\n• Radix Sort: O(d(n+k)) - Sort by digits\n• Bucket Sort: O(n+k) - Distribute into buckets',
                'difficulty': 'Intermediate'
            },
            {
                'title': 'Hash Tables',
                'content': 'Hash Tables are data structures that store key-value pairs with average O(1) time complexity for insertions and lookups.\n\nKey concepts:\n• Hash function: Maps keys to array indices\n• Collision resolution: Handle multiple keys mapping to same index\n• Load factor: Ratio of elements to array size\n\nCollision resolution methods:\n• Chaining: Linked list at each index\n• Open addressing: Find next available slot\n• Linear probing: Check next consecutive slot\n• Quadratic probing: Check slots with quadratic spacing\n\nApplications:\n• Dictionary/map implementations\n• Database indexing\n• Caching\n• Duplicate detection',
                'difficulty': 'Intermediate'
            },
            {
                'title': 'Tree Data Structures',
                'content': 'Trees are hierarchical data structures with nodes connected by edges.\n\nTypes of trees:\n• Binary Tree: Each node has at most 2 children\n• Binary Search Tree: Left subtree < root < right subtree\n• AVL Tree: Self-balancing BST\n• Red-Black Tree: Self-balancing with color properties\n• B-Tree: Multi-way search tree\n• Trie: Prefix tree for strings\n\nTree traversals:\n• Inorder: Left → Root → Right\n• Preorder: Root → Left → Right\n• Postorder: Left → Right → Root\n• Level order: Level by level (BFS)\n\nApplications:\n• File systems\n• Database indexing\n• Expression evaluation\n• Huffman coding',
                'difficulty': 'Advanced'
            },
            {
                'title': 'Greedy Algorithms',
                'content': 'Greedy algorithms make locally optimal choices at each step to find a global optimum.\n\nKey characteristics:\n• Makes best choice at current moment\n• Doesn\'t reconsider previous choices\n• May not always give optimal solution\n• Often efficient and simple\n\nCommon greedy problems:\n• Activity Selection: Choose maximum non-overlapping activities\n• Fractional Knapsack: Take items with highest value/weight ratio\n• Huffman Coding: Build optimal prefix code\n• Dijkstra\'s Algorithm: Find shortest path\n• Kruskal\'s Algorithm: Find minimum spanning tree\n\nWhen to use:\n• Problem has optimal substructure\n• Greedy choice property holds\n• Need efficient solution (not necessarily optimal)',
                'difficulty': 'Intermediate'
            },
            {
                'title': 'Bit Manipulation',
                'content': 'Bit manipulation involves operations on individual bits of data.\n\nCommon bit operations:\n• AND (&): Both bits must be 1\n• OR (|): At least one bit must be 1\n• XOR (^): Bits must be different\n• NOT (~): Flip all bits\n• Left shift (<<): Multiply by 2^n\n• Right shift (>>): Divide by 2^n\n\nUseful techniques:\n• Check if bit is set: n & (1 << i)\n• Set a bit: n | (1 << i)\n• Clear a bit: n & ~(1 << i)\n• Toggle a bit: n ^ (1 << i)\n• Count set bits: Brian Kernighan\'s algorithm\n• Power of 2: n & (n-1) == 0\n\nApplications:\n• Flag management\n• Memory optimization\n• Cryptography\n• Graphics programming',
                'difficulty': 'Advanced'
            },
            {
                'title': 'String Algorithms',
                'content': 'String algorithms solve problems involving text processing and pattern matching.\n\nCommon algorithms:\n• String matching: Find pattern in text\n• Longest Common Subsequence: Find longest common sequence\n• Edit Distance: Minimum operations to transform one string to another\n• Palindrome: Check if string reads same forwards and backwards\n• Anagrams: Check if strings have same characters\n\nPattern matching:\n• Naive: Check each position\n• KMP (Knuth-Morris-Pratt): Use failure function\n• Boyer-Moore: Skip characters based on pattern\n• Rabin-Karp: Use hash function\n\nApplications:\n• Text editors\n• DNA sequence analysis\n• Plagiarism detection\n• Data validation',
                'difficulty': 'Intermediate'
            }
        ]
        
        # Get current date
        today = timezone.now().date()
        
        # Use day of year to cycle through concepts
        day_of_year = today.timetuple().tm_yday
        concept_index = day_of_year % len(concepts)
        selected_concept = concepts[concept_index]
        
        # Update or create concept of the day
        concept, created = ConceptOfDay.objects.get_or_create(
            id=1,  # Always use ID 1 for concept of the day
            defaults={
                'title': selected_concept['title'],
                'content': selected_concept['content'],
                'difficulty': selected_concept['difficulty'],
                'date': today
            }
        )
        
        if not created:
            # Update existing concept
            concept.title = selected_concept['title']
            concept.content = selected_concept['content']
            concept.difficulty = selected_concept['difficulty']
            concept.date = today
            concept.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Updated concept of the day: {selected_concept["title"]} ({selected_concept["difficulty"]})')
        )
        
        # Print concept details
        self.stdout.write(f'\nTitle: {selected_concept["title"]}')
        self.stdout.write(f'Difficulty: {selected_concept["difficulty"]}')
        self.stdout.write(f'Date: {today}')
        self.stdout.write(f'Content preview: {selected_concept["content"][:100]}...') 