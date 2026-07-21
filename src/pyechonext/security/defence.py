import html
import json
import re
import secrets
from collections import defaultdict
from typing import Any, Dict


class CSRFTokenManager:
    """Manages CSRF tokens associated with user sessions."""

    def __init__(self):
        self.csrf_tokens = defaultdict(str)

    def generate_token(self, session_id: str) -> str:
        """Generates a new CSRF token for the given session.

        Args:
            session_id (str): given session id.

        Return:
            str: CSRF token
        """
        token = secrets.token_urlsafe(32)
        self.csrf_tokens[session_id] = token
        return token

    def validate_token(self, session_id: str, token: str) -> bool:
        """Validates the CSRF token for the given session.

        Args:
            session_id (str): session id
            token (str): session key

        Return:
            bool - validating status
        """
        return self.csrf_tokens.get(session_id) == token

    def revoke_token(self, session_id: str):
        """Revokes the CSRF token for the given session.

        Args:
            session_id (str): session for revoking
        """
        self.csrf_tokens.pop(session_id, None)


class XSSSanitizer:
    """Handles output sanitization to prevent XSS attacks."""

    @staticmethod
    def sanitize(data: str) -> str:
        """Escapes output data to prevent XSS attacks.

        Args:
            data (str): output data

        Return:
            str: escaped data
        """
        return html.escape(data)

    @staticmethod
    def sanitize_attributes(data: str) -> str:
        """Sanitizes HTML attributes to prevent XSS.

        Args:
            data (str): raw data

        Return:
            str: sanitized data
        """
        return re.sub(r"([\"\'])", r"&quot;\1", data)


class SQLFilter:
    """Filters incoming SQL queries to prevent SQL injection."""

    @staticmethod
    def filter_query(query: str) -> str:
        """Filters potentially harmful SQL commands from the query.

        Args:
            query (str): SQL Query

        Return:
            str: cleaned sql query
        """
        return re.sub(r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP|;|--|\|\|)", "", query)


class InputValidator:
    """Validates incoming data types and formats."""

    @staticmethod
    def validate(data: Any, expected_type: type) -> bool:
        """Validates data against the expected type.

        Args:
            data (Any): input data
            expected_type (type): expected data type

        Return:
            bool: validating status
        """
        if expected_type is str:
            return isinstance(data, str) and bool(data.strip())
        elif expected_type is int:
            return isinstance(data, int) and data >= 0
        raise TypeError("Unsupported type")

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """Checks the validity of an email format.

        Args:
            email (str): raw email data

        Return:
            bool: validating status
        """
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(regex, email) is not None


class HTTPHeaderManager:
    """Manages HTTP security headers."""

    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Sets security headers for a response, with optional custom headers.

        Return:
            Dict[str, str]: security headers
        """
        headers = {
            "Content-Security-Policy": "default-src 'self';",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "X-Frame-Options": "DENY",
            "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
            "Referrer-Policy": "no-referrer",
        }

        return headers


class RateLimiter:
    """Manages request counting and rate limiting."""

    def __init__(self, request_limit: int = 100):
        """
        Initialize a RateLimiter

        Args:
            request_limit (int) - requests count limit
        """
        self.requests_counter = defaultdict(int)
        self.request_limit = request_limit
        self.request_times = defaultdict(list)

    def is_rate_limited(self, req_id: str) -> bool:
        """Checks if the user is rate-limited.

        Args:
            req_id(str) - request id
        """
        return self.requests_counter[req_id] >= self.request_limit

    def increment_requests(self, req_id: str):
        """Increments the request counter for the user.

        Args:
            req_id(str) - request id
        """
        self.requests_counter[req_id] += 1

    def reset_request_count(self, req_id: str):
        """Resets the request counter for the user.

        Args:
            req_id(str) - request id
        """
        self.requests_counter[req_id] = 0


class Security:
    """Aggregates various security mechanisms for the web application."""

    def __init__(self, request_limit: int = 100):
        """Initializes the Security class with a specific request limit.

        Args:
            request_limit (int): The maximum number of requests per object (default is 100).
        """
        self.csrf_token_manager = CSRFTokenManager()
        self.xss_sanitizer = XSSSanitizer()
        self.sql_filter = SQLFilter()
        self.input_validator = InputValidator()
        self.http_header_manager = HTTPHeaderManager()
        self.rate_limiter = RateLimiter(request_limit)

    @classmethod
    def generate_csrf_token(cls, session_id: str) -> str:
        """Generates a new CSRF token for the given session.

        Args:
            session_id (str): The unique identifier for the user session.

        Returns:
            str: The generated CSRF token.
        """
        return cls().csrf_token_manager.generate_token(session_id)

    @classmethod
    def validate_csrf_token(cls, session_id: str, token: str) -> bool:
        """Validates the CSRF token for the given session.

        Args:
            session_id (str): The unique identifier for the user session.
            token (str): The CSRF token to validate.

        Returns:
            bool: True if the token is valid, otherwise False.
        """
        return cls().csrf_token_manager.validate_token(session_id, token)

    @classmethod
    def revoke_csrf_token(cls, session_id: str):
        """Revokes the CSRF token for the given session.

        Args:
            session_id (str): The unique identifier for the user session.
        """
        cls().csrf_token_manager.revoke_token(session_id)

    @classmethod
    def sanitize_output(cls, data: str) -> str:
        """Escapes output data to prevent XSS attacks.

        Args:
            data (str): The input data to sanitize.

        Returns:
            str: The sanitized output data.
        """
        return cls().xss_sanitizer.sanitize(data)

    @classmethod
    def sanitize_html_attributes(cls, data: str) -> str:
        """Sanitizes HTML attributes to prevent XSS.

        Args:
            data (str): The input data containing HTML attributes.

        Returns:
            str: The sanitized HTML attributes.
        """
        return cls().xss_sanitizer.sanitize_attributes(data)

    @classmethod
    def filter_sql_query(cls, query: str) -> str:
        """Filters potentially harmful SQL commands from the query.

        Args:
            query (str): The SQL query to filter.

        Returns:
            str: The filtered SQL query.
        """
        return cls().sql_filter.filter_query(query)

    @classmethod
    def validate_input(cls, data: Any, expected_type: type) -> bool:
        """Validates data against the expected type.

        Args:
            data (Any): The data to validate.
            expected_type (type): The expected type of the data.

        Returns:
            bool: True if the data matches the expected type, otherwise False.
        """
        return cls().input_validator.validate(data, expected_type)

    @classmethod
    def is_email_valid(cls, email: str) -> bool:
        """Checks the validity of an email format.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email format is valid, otherwise False.
        """
        return cls().input_validator.is_email_valid(email)

    @classmethod
    def get_security_headers(cls) -> Dict[str, str]:
        """Sets security headers for a response, with optional custom headers.

        Returns:
            Dict[str, str]: The updated response dictionary with security headers.
        """
        return cls().http_header_manager.get_security_headers()

    @classmethod
    def is_rate_limited(cls, object_id: str) -> bool:
        """Checks if the object is rate-limited.

        Args:
            object_id (str): The unique identifier for the object.

        Returns:
        bool: True if the object has exceeded the request limit, otherwise False.
        """
        return cls().rate_limiter.is_rate_limited(object_id)

    @classmethod
    def increment_request_count(cls, object_id: str):
        """Increments the request counter for the object.

        Args:
            object_id (str): The unique identifier for the object.
        """
        cls().rate_limiter.increment_requests(object_id)

    @classmethod
    def reset_request_count(cls, object_id: str):
        """Resets the request counter for the object.

        Args:
            object_id (str): The unique identifier for the object.
        """
        cls().rate_limiter.reset_request_count(object_id)


# Example usage of the Security class
if __name__ == "__main__":
    session_id = "user123"
    csrf_token = Security.generate_csrf_token(session_id)
    print("CSRF Token:", csrf_token)

    is_valid_csrf = Security.validate_csrf_token(session_id, csrf_token)
    print("Is CSRF valid?", is_valid_csrf)

    Security.revoke_csrf_token(session_id)

    raw_query = "SELECT * FROM users WHERE id=1; DROP TABLE users;"
    filtered_query = Security.filter_sql_query(raw_query)
    print("Filtered Query:", filtered_query)

    user_input = "example"
    is_valid_input = Security.validate_input(user_input, str)
    print("Is user input valid?", is_valid_input)

    email_check = "test@example.com"
    is_email_valid = Security.is_email_valid(email_check)
    print("Is email valid?", is_email_valid)

    response_headers = {}
    custom_headers = {"X-Custom-Header": "CustomValue"}
    Security.get_security_headers()
    print("Security Headers:", json.dumps(response_headers, indent=2))

    user_id = "user123"
    for _ in range(101):
        Security.increment_request_count(user_id)

    if Security.is_rate_limited(user_id):
        print(f"{user_id} is rate-limited.")
    else:
        print(f"{user_id} can make more requests.")
