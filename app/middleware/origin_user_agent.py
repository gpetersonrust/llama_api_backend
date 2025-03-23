from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN
from app.core.config import settings


class OriginAndUserAgentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        user_agent = request.headers.get("user-agent", "")

        if not origin or origin != settings.ALLOWED_ORIGIN:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"Unauthorized origin: {origin or 'missing'}",
            )

        if not self.is_browser_user_agent(user_agent):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Access denied: Browser required.",
            )

        return await call_next(request)

    def is_browser_user_agent(self, user_agent: str) -> bool:
        browsers = ["Mozilla", "Chrome", "Safari", "Firefox", "Edge"]
        return any(browser in user_agent for browser in browsers)
