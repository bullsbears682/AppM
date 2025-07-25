"""
Simple rate limiter for ROI Calculator API
Prevents abuse and ensures fair usage
"""

import time
from collections import defaultdict, deque
from typing import Dict, Tuple
from functools import wraps
from flask import request, jsonify

class SimpleRateLimiter:
    """Simple token bucket rate limiter"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """Check if request is allowed, return (allowed, retry_after)"""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        user_requests = self.requests[identifier]
        while user_requests and user_requests[0] < window_start:
            user_requests.popleft()
        
        # Check if under limit
        if len(user_requests) < self.max_requests:
            user_requests.append(now)
            return True, 0
        else:
            # Calculate retry after
            retry_after = int(user_requests[0] + self.window_seconds - now) + 1
            return False, retry_after
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests for identifier"""
        now = time.time()
        window_start = now - self.window_seconds
        
        user_requests = self.requests[identifier]
        # Clean old requests
        while user_requests and user_requests[0] < window_start:
            user_requests.popleft()
        
        return max(0, self.max_requests - len(user_requests))

# Global rate limiters
calculation_limiter = SimpleRateLimiter(max_requests=20, window_seconds=300)  # 20 calculations per 5 minutes
api_limiter = SimpleRateLimiter(max_requests=100, window_seconds=3600)  # 100 API calls per hour

def rate_limit(limiter: SimpleRateLimiter, error_message: str = "Rate limit exceeded"):
    """Decorator for rate limiting"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (IP address)
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if not client_ip:
                client_ip = 'unknown'
            
            # Check rate limit
            allowed, retry_after = limiter.is_allowed(client_ip)
            
            if not allowed:
                response = jsonify({
                    'error': True,
                    'message': error_message,
                    'retry_after': retry_after,
                    'limit_info': {
                        'max_requests': limiter.max_requests,
                        'window_seconds': limiter.window_seconds,
                        'remaining': limiter.get_remaining(client_ip)
                    }
                })
                response.status_code = 429  # Too Many Requests
                response.headers['Retry-After'] = str(retry_after)
                return response
            
            # Add rate limit headers
            response = f(*args, **kwargs)
            if hasattr(response, 'headers'):
                response.headers['X-RateLimit-Limit'] = str(limiter.max_requests)
                response.headers['X-RateLimit-Remaining'] = str(limiter.get_remaining(client_ip))
                response.headers['X-RateLimit-Reset'] = str(int(time.time() + limiter.window_seconds))
            
            return response
        return decorated_function
    return decorator