# Simple Local Setup (No Docker Required)

## Step 1: Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create simple .env file
echo DATABASE_URL=sqlite:///./todo.db > .env
echo BETTER_AUTH_SECRET=your-secret-key-min-32-characters >> .env
echo CORS_ORIGINS=http://localhost:3000 >> .env

# Run backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 2: Frontend Setup (New Terminal)
```bash
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

## Step 3: Custom Hosts (Optional)
Add to Windows hosts file (C:\Windows\System32\drivers\etc\hosts):
```
127.0.0.1 todo-app.local
127.0.0.1 todo-api.local
```

## URLs:
- Frontend: http://localhost:3000 or http://todo-app.local:3000
- Backend: http://localhost:8000 or http://todo-api.local:8000
- API Docs: http://localhost:8000/docs

## Test Commands:
```bash
# Test backend
curl http://localhost:8000/health

# Test frontend
# Open browser: http://localhost:3000
```

## Features Available:
✅ All Phase V advanced features
✅ Priority tasks, due dates, recurring
✅ AI chat interface  
✅ Search and filtering
✅ Event-driven architecture (without Kafka)
✅ Clean local URLs