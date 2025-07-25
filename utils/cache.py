"""
Simple caching system for ROI Calculator
Improves performance by caching expensive calculations
"""

import time
import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class SimpleCache:
    """Thread-safe simple cache with TTL support"""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def _generate_key(self, data: Dict[str, Any]) -> str:
        """Generate cache key from input data"""
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(sorted_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self.cache:
            entry = self.cache[key]
            if datetime.utcnow() < entry['expires']:
                entry['hits'] += 1
                entry['last_accessed'] = datetime.utcnow()
                return entry['data']
            else:
                # Expired entry
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        ttl = ttl or self.default_ttl
        expires = datetime.utcnow() + timedelta(seconds=ttl)
        
        self.cache[key] = {
            'data': data,
            'expires': expires,
            'created': datetime.utcnow(),
            'hits': 0,
            'last_accessed': datetime.utcnow()
        }
        
        # Clean up expired entries periodically
        if len(self.cache) > 100:  # Cleanup when cache gets large
            self._cleanup_expired()
    
    def get_or_set(self, data: Dict[str, Any], calculator_func, ttl: Optional[int] = None) -> Any:
        """Get from cache or calculate and set"""
        key = self._generate_key(data)
        
        # Try to get from cache
        cached_result = self.get(key)
        if cached_result is not None:
            return cached_result
        
        # Calculate and cache
        result = calculator_func()
        self.set(key, result, ttl)
        return result
    
    def _cleanup_expired(self) -> None:
        """Remove expired entries"""
        now = datetime.utcnow()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now >= entry['expires']
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        now = datetime.utcnow()
        active_entries = sum(1 for entry in self.cache.values() if now < entry['expires'])
        total_hits = sum(entry['hits'] for entry in self.cache.values())
        
        return {
            'total_entries': len(self.cache),
            'active_entries': active_entries,
            'total_hits': total_hits,
            'hit_rate': total_hits / max(len(self.cache), 1),
            'oldest_entry': min((entry['created'] for entry in self.cache.values()), default=None),
            'newest_entry': max((entry['created'] for entry in self.cache.values()), default=None)
        }

# Global cache instance
calculation_cache = SimpleCache(default_ttl=600)  # 10 minutes for calculations