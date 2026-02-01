"""
Security utilities for AI Shield Auditor
"""
import re
import hashlib
from typing import Dict, Any, List
from functools import lru_cache
from datetime import datetime, timedelta
from cachetools import TTLCache

# Rate limiting cache (IP -> request times)
_rate_limit_cache = TTLCache(maxsize=1000, ttl=60)

# Input validation patterns
SAFE_INPUT_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_.,!?()[\]{}:;"\'/\n\r]+$')
MAX_INPUT_LENGTH = 100000  # 100KB max input


class SecurityValidator:
    """Validates and sanitizes user inputs"""

    @staticmethod
    def sanitize_input(text: str, max_length: int = MAX_INPUT_LENGTH) -> str:
        """
        Sanitize user input to prevent injection attacks

        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized text

        Raises:
            ValueError: If input is invalid
        """
        if not text:
            return ""

        # Check length
        if len(text) > max_length:
            raise ValueError(f"Input exceeds maximum length of {max_length} characters")

        # Basic sanitization - remove null bytes and control characters
        sanitized = text.replace('\x00', '')

        # Remove potentially dangerous patterns
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript protocol
            r'on\w+\s*=',  # Event handlers
        ]

        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)

        return sanitized.strip()

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate API key format

        Args:
            api_key: API key to validate

        Returns:
            True if valid format
        """
        if not api_key:
            return False

        # Check length and format
        if len(api_key) < 20 or len(api_key) > 200:
            return False

        # Basic format check (alphanumeric and common special chars)
        if not re.match(r'^[a-zA-Z0-9\-_]+$', api_key):
            return False

        return True

    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """
        Hash sensitive data for logging/storage

        Args:
            data: Data to hash

        Returns:
            SHA256 hash of the data
        """
        return hashlib.sha256(data.encode()).hexdigest()


class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed

        Args:
            identifier: Unique identifier (e.g., IP address, user ID)

        Returns:
            True if request is allowed, False if rate limited
        """
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)

        # Get or initialize request list for this identifier
        if identifier not in _rate_limit_cache:
            _rate_limit_cache[identifier] = []

        requests = _rate_limit_cache[identifier]

        # Remove old requests outside the window
        requests = [req_time for req_time in requests if req_time > cutoff]

        # Check if under limit
        if len(requests) >= self.max_requests:
            return False

        # Add current request
        requests.append(now)
        _rate_limit_cache[identifier] = requests

        return True


def get_security_headers() -> Dict[str, str]:
    """
    Get recommended security headers for HTTP responses

    Returns:
        Dictionary of security headers
    """
    return {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
    }


def redact_sensitive_info(text: str) -> str:
    """
    Redact sensitive information from text for logging

    Args:
        text: Text that may contain sensitive info

    Returns:
        Text with sensitive info redacted
    """
    patterns = {
        'api_key': r'(sk-|api[_-]?key[_-]?)[a-zA-Z0-9]{20,}',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    }

    redacted = text
    for pattern_name, pattern in patterns.items():
        redacted = re.sub(pattern, f'[REDACTED_{pattern_name.upper()}]', redacted)

    return redacted
