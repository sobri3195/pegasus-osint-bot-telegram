import time
from collections import defaultdict
from typing import Dict, Tuple
from datetime import datetime, timedelta

from utils.config import settings


class RateLimiter:
    def __init__(self):
        self.requests: Dict[int, list] = defaultdict(list)
        self.max_requests = settings.rate_limit_requests
        self.period = settings.rate_limit_period
    
    def is_allowed(self, user_id: int) -> Tuple[bool, int]:
        if user_id in settings.admin_ids:
            return True, 0
        
        now = time.time()
        user_requests = self.requests[user_id]
        
        user_requests[:] = [req_time for req_time in user_requests 
                           if now - req_time < self.period]
        
        if len(user_requests) >= self.max_requests:
            oldest_request = min(user_requests)
            wait_time = int(self.period - (now - oldest_request))
            return False, wait_time
        
        user_requests.append(now)
        return True, 0
    
    def reset(self, user_id: int):
        if user_id in self.requests:
            del self.requests[user_id]
    
    def get_remaining(self, user_id: int) -> int:
        if user_id in settings.admin_ids:
            return 999
        
        now = time.time()
        user_requests = self.requests[user_id]
        
        user_requests[:] = [req_time for req_time in user_requests 
                           if now - req_time < self.period]
        
        return max(0, self.max_requests - len(user_requests))


rate_limiter = RateLimiter()
