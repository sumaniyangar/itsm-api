from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import incidents, changes

# Create all DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini ITSM API",
    description="""
A ServiceNow-inspired IT Service Management REST API.

Built by **Suman M** — ServiceNow Platform Lead & CSA Certified Developer.

Demonstrates core ITSM backend mechanics:
- Incident lifecycle: New → In Progress → Resolved → Closed
- Change lifecycle: Draft → Authorize → Implement → Closed
- Auto-number generation (INC/CHG prefix with zero-padding)
- Business Rule-style state transition timestamp logic
    """,
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(incidents.router)
app.include_router(changes.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Mini ITSM API is running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}