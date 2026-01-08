# Phase V Testing Commands

## 🚀 Setup (One Time)
```bash
git clone https://github.com/WajahatAli3218664/hackathons-wajahat-todo.git
cd hackathons-wajahat-todo
```

## 🔧 Start Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --reload
```
**Result**: Backend running on http://localhost:8000

## 🎨 Start Frontend (New Terminal)
```bash
npm install
npm run dev
```
**Result**: Frontend running on http://localhost:3000

## ✅ Test Phase V Features

### 1. Test Advanced Task Management
- Go to http://localhost:3000
- Create task with:
  - Priority: High/Medium/Low
  - Due Date: Pick future date
  - Recurring: Daily/Weekly/Monthly
  - Tags: Add custom tags

### 2. Test AI Chat Interface
- Click "Chat" in navigation
- Try commands:
  - "Add buy milk with high priority"
  - "Show my pending tasks"
  - "Mark task as complete"

### 3. Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Get tasks with filters
curl "http://localhost:8000/api/tasks?priority=high&search=milk"

# API documentation
# Go to: http://localhost:8000/docs
```

### 4. Test Event-Driven Architecture
```bash
# Check if events are being published
# Look for logs in backend terminal:
# "Published task event: created for task xyz"
# "Published reminder event for task xyz"
```

## 🎯 Expected Results
- ✅ Tasks with priorities, due dates, recurring patterns
- ✅ AI chat responds to natural language
- ✅ Search and filter working
- ✅ Event logs in backend terminal
- ✅ API docs at /docs endpoint

## 🐛 If Issues
```bash
# Check backend logs
# Look for errors in terminal

# Check frontend logs  
# Open browser console (F12)

# Restart services
# Ctrl+C and run commands again
```

**All Phase V features should work locally!** 🚀