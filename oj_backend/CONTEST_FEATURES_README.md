# Contest Features - Complete Guide

This document explains all the contest features implemented in the OJ Project.

## 🎯 **Overview**

The contest system now includes:
- ✅ **Real-time timer** for contest problems
- ✅ **Separate contest problems** (different from regular problems)
- ✅ **No AI review** in contest problems (to prevent cheating)
- ✅ **Contest-specific interface** with timer display
- ✅ **Active contest until August 15th, 2025**

---

## 🕐 **Timer Feature**

### **What is the Timer?**
- **Real-time countdown** showing remaining contest time
- **Updates every second** automatically
- **Visual warnings** when time is running low
- **Automatic contest end** when time expires

### **Timer Features:**
- **Display Format**: HH:MM:SS (e.g., 02:45:30)
- **Warning System**: Red pulsing animation when ≤ 5 minutes remaining
- **Auto-refresh**: Updates every second
- **Contest End**: Automatically redirects when time expires

### **Timer Locations:**
1. **Contest Detail Page**: Shows overall contest timer
2. **Contest Problem Pages**: Shows contest timer in the right panel
3. **Real-time Updates**: Timer syncs across all contest pages

---

## 🎯 **Separate Contest Problems**

### **What are Contest Problems?**
- **Different from regular problems** in the problem list
- **Contest-specific titles** (e.g., "Contest Two Sum" vs "Two Sum")
- **Unique test cases** and examples
- **Contest-only access** when participating in contests

### **Current Contest Problems:**
1. **Contest Two Sum** (Easy)
2. **Contest Palindrome Check** (Easy)
3. **Contest Maximum Subarray** (Medium)
4. **Contest Valid Parentheses** (Easy)
5. **Contest Binary Search** (Easy)
6. **Contest Remove Duplicates** (Easy)

### **How They Work:**
- **Created separately** from regular problems
- **Assigned to contests** automatically
- **Different problem sets** for each contest
- **No overlap** with regular problem list

---

## 🚫 **No AI Review in Contests**

### **Why No AI Review?**
- **Prevents cheating** during contests
- **Ensures fair competition**
- **Maintains contest integrity**
- **Focuses on problem-solving skills**

### **What's Different:**
- **No AI Review button** in contest problem interface
- **Cleaner interface** focused on coding
- **Same functionality** for Run/Submit buttons
- **Timer prominently displayed**

---

## 🎨 **Contest Interface**

### **Contest Problem Page Features:**
- **Left Panel**: Problem description, examples, constraints
- **Right Panel**: Code editor, timer, contest info
- **Timer Display**: Prominent countdown timer
- **Contest Info**: Contest title and status
- **Language Selection**: Python, C++, Java
- **Action Buttons**: Run and Submit (no AI Review)

### **Visual Elements:**
- **Timer Section**: Blue gradient background with white text
- **Contest Info**: Light blue background with contest details
- **Code Editor**: Dark theme with syntax highlighting
- **Results Section**: Color-coded test case results

---

## 🏆 **Active Contest: Summer Coding Championship 2025**

### **Contest Details:**
- **Title**: Summer Coding Championship 2025
- **Duration**: Until August 15th, 2025 (23:59:59)
- **Status**: Currently Active
- **Problems**: 3 contest-specific problems
- **Target**: All skill levels

### **Contest Problems:**
1. **Contest Two Sum** (Easy)
2. **Contest Palindrome Check** (Easy)
3. **Contest Maximum Subarray** (Medium)

---

## 🔧 **Technical Implementation**

### **Files Created/Modified:**

#### **New Templates:**
- `contests/contest_problem_detail.html` - Contest problem interface
- `contests/contest_detail.html` - Contest overview page

#### **Management Commands:**
- `create_contest_problems.py` - Creates contest-specific problems
- `update_contests.py` - Updates contests with contest problems

#### **Modified Files:**
- `views.py` - Updated to handle contest problems
- `urls.py` - Contest routing

### **Key Features:**
- **Template Selection**: Automatically chooses contest template when accessed from contest
- **Timer Integration**: Real-time timer updates via AJAX
- **Problem Separation**: Contest problems stored separately
- **Interface Adaptation**: Different UI for contest vs regular problems

---

## 🚀 **How to Use**

### **For Users:**

#### **1. Join a Contest:**
1. Visit the Contests page
2. Click on "Summer Coding Championship 2025"
3. Click "Start Contest" button
4. Timer will start automatically

#### **2. Solve Contest Problems:**
1. Click on any problem in the contest
2. You'll see the contest interface with timer
3. Write your code in the editor
4. Use "Run" to test on sample cases
5. Use "Submit" to submit final solution
6. No AI Review available (by design)

#### **3. Monitor Time:**
- Timer is visible on all contest pages
- Red warning when ≤ 5 minutes remaining
- Contest automatically ends when time expires

### **For Administrators:**

#### **1. Create Contest Problems:**
```bash
python manage.py create_contest_problems
```

#### **2. Update Contests:**
```bash
python manage.py update_contests
```

#### **3. Update Daily Content:**
```bash
python manage.py update_concept_of_day
python manage.py update_contests
```

---

## 📊 **Contest Management**

### **Contest Types:**
1. **Active Contest**: Currently running (Summer Coding Championship 2025)
2. **Upcoming Contest**: Starts in 3 days (Advanced Algorithms Masterclass)
3. **Future Contest**: Starts in 7 days (Data Structures Challenge)
4. **Ended Contest**: Already completed (Beginner Friendly Contest)

### **Problem Distribution:**
- **Each contest** has unique problem combinations
- **No duplicate problems** across contests
- **Different difficulty levels** for variety
- **Contest-specific problems** used when available

---

## 🎯 **Contest Rules**

### **Timer Rules:**
- **Real-time countdown** from contest start
- **No time extension** once contest starts
- **Automatic submission** when time expires
- **Warning notifications** at 5 minutes remaining

### **Problem Rules:**
- **No AI assistance** during contests
- **Original solutions only** required
- **No external help** allowed
- **Fair competition** enforced

### **Scoring Rules:**
- **Points based on difficulty** (Easy: 10, Medium: 20, Hard: 30)
- **Partial credit** for correct logic
- **Time bonus** for early submissions
- **Leaderboard ranking** by total score

---

## 🔍 **Troubleshooting**

### **Common Issues:**

#### **1. Timer Not Updating:**
- Check internet connection
- Refresh the page
- Ensure contest is active
- Check browser console for errors

#### **2. Contest Problems Not Loading:**
- Run `python manage.py create_contest_problems`
- Check if contest problems exist in database
- Verify contest is properly configured

#### **3. AI Review Still Appearing:**
- Ensure you're accessing from contest link
- Check URL contains contest parameter
- Clear browser cache
- Verify template is being used correctly

### **Debug Commands:**
```bash
# Check contest problems
python manage.py shell
>>> from auth_app.models import Problem
>>> Problem.objects.filter(title__icontains='Contest').count()

# Check contest status
>>> from auth_app.models import Contest
>>> Contest.objects.filter(is_active=True).first()
```

---

## 📈 **Future Enhancements**

### **Planned Features:**
- **Multiple contest types** (individual, team, elimination)
- **Contest themes** (algorithms, data structures, etc.)
- **Real-time leaderboard** updates
- **Contest analytics** and statistics
- **Custom contest creation** for administrators

### **Advanced Timer Features:**
- **Pause/resume** functionality
- **Time warnings** at multiple intervals
- **Contest extension** capabilities
- **Time zone** support

---

## 📝 **Summary**

The contest system now provides:
- ✅ **Professional contest experience** with real-time timer
- ✅ **Separate contest problems** to prevent overlap
- ✅ **Fair competition** with no AI assistance
- ✅ **Active contest** running until August 15th, 2025
- ✅ **Comprehensive contest management** tools

This creates a complete contest environment similar to professional coding platforms like Codeforces, HackerRank, and LeetCode contests! 