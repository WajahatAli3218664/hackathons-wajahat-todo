# Phase V - Local Development Setup

## 📦 Download Code
```bash
git clone https://github.com/WajahatAli3218664/hackathons-wajahat-todo.git
cd hackathons-wajahat-todo
```

## 🚀 Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database URL

# Run backend
python -m uvicorn src.main:app --reload --port 8000
```

## 🎨 Frontend Setup
```bash
# In new terminal
npm install
npm run dev
```

## 🔧 Environment Variables Needed

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000
OPENAI_API_KEY=sk-your-openai-key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
```

## ✅ Phase V Features Available
- Advanced Task Management (Priorities, Due Dates, Recurring)
- Event-Driven Architecture (Kafka integration)
- Microservices (Notification, Recurring services)
- AI Chat Interface
- Search, Filter, Sort functionality
- Tag-based categorization

## 🌐 Local URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📱 Test Features
1. Create tasks with priorities and due dates
2. Use AI chat for natural language task management
3. Test recurring task functionality
4. Try search and filtering
5. Add tags to tasks

All Phase V advanced features are ready to test locally!