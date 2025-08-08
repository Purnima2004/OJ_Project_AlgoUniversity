# Daily Content Updates

This document explains how to set up automatic daily updates for the OJ Project.

## What Gets Updated Daily

### 1. Concept of the Day
- **12 different programming concepts** that cycle daily
- Topics include: Dynamic Programming, Binary Search, Graph Algorithms, Two Pointers, Sliding Window, Recursion, Sorting Algorithms, Hash Tables, Tree Data Structures, Greedy Algorithms, Bit Manipulation, String Algorithms
- Each concept includes detailed explanations, key points, and applications

### 2. Contests
- **Active Contest**: "Summer Coding Championship 2025" (until August 15th, 2025)
- **Upcoming Contest**: "Advanced Algorithms Masterclass" (starts in 3 days)
- **Future Contest**: "Data Structures Challenge" (starts in 7 days)
- **Ended Contest**: "Beginner Friendly Contest" (ended 14 days ago)

## Manual Updates

### Update Concept of the Day
```bash
python manage.py update_concept_of_day
```

### Update Contests
```bash
python manage.py update_contests
```

### Update Both
```bash
python manage.py update_concept_of_day
python manage.py update_contests
```

Or use the batch script:
```bash
update_daily.bat
```

## Automatic Daily Updates

### Windows Task Scheduler

1. **Open Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task**:
   - Click "Create Basic Task"
   - Name: "OJ Daily Content Update"
   - Trigger: Daily
   - Start time: 00:01 (1 minute past midnight)
   - Action: Start a program
   - Program: `cmd.exe`
   - Arguments: `/c "cd /d C:\path\to\your\project\oj_backend && python manage.py update_concept_of_day && python manage.py update_contests"`

3. **Advanced Settings**:
   - Run whether user is logged on or not
   - Run with highest privileges
   - Configure for: Windows 10

### Linux/Mac Cron Job

1. **Open crontab**:
   ```bash
   crontab -e
   ```

2. **Add daily job** (runs at 00:01 every day):
   ```bash
   1 0 * * * cd /path/to/your/project/oj_backend && python manage.py update_concept_of_day && python manage.py update_contests
   ```

### Using Python Script

You can also use the provided Python script:
```bash
python update_daily_content.py
```

## Contest Details

### Active Contest: Summer Coding Championship 2025
- **Duration**: Until August 15th, 2025
- **Problems**: 3 problems (Two Sum, Add Two Numbers, Longest Substring)
- **Status**: Currently running

### Upcoming Contest: Advanced Algorithms Masterclass
- **Start**: 3 days from now
- **Duration**: 4 hours
- **Problems**: 3 problems (Median of Two Sorted Arrays, Reverse String, Valid Parentheses)
- **Target**: Experienced coders

### Future Contest: Data Structures Challenge
- **Start**: 7 days from now
- **Duration**: 5 hours
- **Problems**: 3 problems (Two Sum, Longest Substring)
- **Target**: Intermediate coders

### Ended Contest: Beginner Friendly Contest
- **Ended**: 14 days ago
- **Problems**: 3 problems (Add Two Numbers, Median of Two Sorted Arrays, Valid Parentheses)
- **Target**: Beginners

## Concept of the Day Topics

The system cycles through these 12 topics daily:

1. **Dynamic Programming** (Advanced)
2. **Binary Search** (Intermediate)
3. **Graph Algorithms** (Advanced)
4. **Two Pointers Technique** (Intermediate)
5. **Sliding Window** (Intermediate)
6. **Recursion** (Intermediate)
7. **Sorting Algorithms** (Intermediate)
8. **Hash Tables** (Intermediate)
9. **Tree Data Structures** (Advanced)
10. **Greedy Algorithms** (Intermediate)
11. **Bit Manipulation** (Advanced)
12. **String Algorithms** (Intermediate)

## Troubleshooting

### Common Issues

1. **Permission Denied**:
   - Run as administrator (Windows)
   - Check file permissions (Linux/Mac)

2. **Python Path Issues**:
   - Ensure Python is in PATH
   - Use full path to Python executable

3. **Django Settings**:
   - Ensure DJANGO_SETTINGS_MODULE is set correctly
   - Check if virtual environment is activated

### Manual Verification

To verify updates are working:
1. Check the home page for updated concept of the day
2. Visit the contests page to see contest status
3. Check the database directly:
   ```bash
   python manage.py shell
   >>> from auth_app.models import ConceptOfDay, Contest
   >>> ConceptOfDay.objects.first()
   >>> Contest.objects.all()
   ```

## Notes

- The concept of the day changes at midnight based on the day of the year
- Contests are updated with different problem combinations
- All contests have unique problem sets to avoid repetition
- The active contest runs until August 15th, 2025 as requested 