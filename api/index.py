import sys
import os

# Add backend src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    # Import modules directly without relative imports
    import routes.tasks as tasks_module
    import routes.chat as chat_module
    import routes.auth_simple as auth_module
    import db as db_module
    
    app = FastAPI(title="Todo API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize database on startup
    @app.on_event("startup")
    async def startup_event():
        try:
            await db_module.init_db()
        except Exception as e:
            print(f"Database init error: {e}")

    # Include routers
    app.include_router(tasks_module.router)
    app.include_router(chat_module.router)
    app.include_router(auth_module.router)
    
    @app.get("/")
    def read_root():
        return {"message": "Todo API is running on Vercel!", "version": "1.0.0"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "version": "1.0.0"}

    @app.get("/api/health")
    def api_health():
        return {"status": "ok", "service": "todo-api"}
        
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback minimal app
    from fastapi import FastAPI
    app = FastAPI(title="Todo API - Import Error")
    
    @app.get("/")
    def error_root():
        return {"error": f"Import failed: {e}", "message": "Basic API running"}
        
    @app.get("/health")
    def error_health():
        return {"status": "error", "error": str(e)}