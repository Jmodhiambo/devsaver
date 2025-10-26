#!/usr/bin/env python3
from contextvars import ContextVar

request_context = ContextVar("request_context", default={})

class ContextualASGIMiddleware:
    """ASGI middleware that sets a ContextVar visible to the app task."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Only apply to HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # session (if SessionMiddleware already ran earlier) is in scope['session']
        session = scope.get("session", {})
        user_id = session.get("user") if isinstance(session, dict) else None

        # set context BEFORE calling the app — this will be visible to the downstream task
        request_context.set({
            "path": scope.get("path", "-"),
            "method": scope.get("method", "-"),
            "user_id": user_id,
        })

        try:
            await self.app(scope, receive, send)
        finally:
            # clear context after respones completes
            request_context.set({})



# #!/usr/bin/env python3
# """Middleware to add per-request logging context."""

# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from contextvars import ContextVar

# # Context variable to hold request info
# request_context = ContextVar("request_context", default={})

# class ContextualLoggingMiddleware(BaseHTTPMiddleware):
#     """Attach user and request context to logs automatically."""

#     async def dispatch(self, request: Request, call_next):
#         """Attach user and request context to logs automatically."""
#         # Default context before route execution
#         request_context.set({
#             "path": request.url.path,
#             "method": request.method,
#             "user_id": None,
#         })

#         # Continue request processing
#         response = await call_next(request)

#         # 🔹 Fetch session data AFTER route execution
#         user_id = None
#         if "session" in request.scope:
#             user_id = request.session.get("user")

#         # Update context for final logs
#         request_context.set({
#             "path": request.url.path,
#             "method": request.method,
#             "user_id": user_id,
#         })

#         # Clear after request to avoid context leakage (optional)
#         request_context.set({})
#         return response