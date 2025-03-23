from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.api.v1.endpoints import router as api_router
from app.core.config import settings
from app.core.rate_limit import limiter
from slowapi.middleware import SlowAPIMiddleware
from app.middleware.origin_user_agent import OriginAndUserAgentMiddleware

app = FastAPI(title="LLaMA3 Chat API 🦙")  # LLaMA 3 API route
# 🔐 Middleware for origin and browser validation
app.add_middleware(
    OriginAndUserAgentMiddleware
)  # add middleware for origin and user-agent validation

# Set up rate limiter
app.state.limiter = limiter  # attach limiter to app state

app.add_middleware(SlowAPIMiddleware)  # add slowapi middleware
app.add_exception_handler(
    429, _rate_limit_exceeded_handler
)  # handle rate limit exceeded

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)
