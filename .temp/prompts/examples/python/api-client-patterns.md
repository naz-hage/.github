# Python API Client Patterns

This document provides comprehensive patterns for building robust API clients in Python, focusing on best practices for HTTP communication, error handling, and maintainability.

## Core HTTP Client Patterns

### Basic REST API Client

```python
import requests
from typing import Dict, List, Optional, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """Base API client with retry logic and error handling."""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout

        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update({
            'User-Agent': 'Python-API-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}

        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e, url)
        except requests.exceptions.ConnectionError:
            raise APIConnectionError(f"Failed to connect to {url}")
        except requests.exceptions.Timeout:
            raise APITimeoutError(f"Request to {url} timed out")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}")

    def _handle_http_error(self, error: requests.exceptions.HTTPError, url: str):
        """Handle HTTP errors with appropriate exceptions."""
        response = error.response
        status_code = response.status_code

        try:
            error_data = response.json()
            message = error_data.get('message', error_data.get('error', str(error)))
        except ValueError:
            message = str(error)

        if status_code == 400:
            raise APIValidationError(f"Bad request: {message}")
        elif status_code == 401:
            raise APIAuthenticationError(f"Authentication failed: {message}")
        elif status_code == 403:
            raise APIAuthorizationError(f"Access forbidden: {message}")
        elif status_code == 404:
            raise APINotFoundError(f"Resource not found: {message}")
        elif status_code == 429:
            raise APIRateLimitError(f"Rate limit exceeded: {message}")
        elif 500 <= status_code < 600:
            raise APIServerError(f"Server error ({status_code}): {message}")
        else:
            raise APIError(f"HTTP {status_code}: {message}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET request."""
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POST request."""
        return self._make_request('POST', endpoint, json=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """PUT request."""
        return self._make_request('PUT', endpoint, json=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request."""
        return self._make_request('DELETE', endpoint)

    def close(self):
        """Close the session."""
        self.session.close()
```

### Async API Client (aiohttp)

```python
import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class AsyncAPIClient:
    """Asynchronous API client using aiohttp."""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = aiohttp.ClientTimeout(total=timeout)

        # Default headers
        self.headers = {
            'User-Agent': 'Python-Async-API-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers, timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make async HTTP request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            async with self.session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                if response.content_type == 'application/json':
                    return await response.json()
                else:
                    return {'content': await response.text()}

        except aiohttp.ClientResponseError as e:
            await self._handle_http_error(e, url)
        except aiohttp.ClientConnectionError:
            raise APIConnectionError(f"Failed to connect to {url}")
        except asyncio.TimeoutError:
            raise APITimeoutError(f"Request to {url} timed out")
        except Exception as e:
            raise APIError(f"Request failed: {e}")

    async def _handle_http_error(self, error: aiohttp.ClientResponseError, url: str):
        """Handle HTTP errors with appropriate exceptions."""
        status_code = error.status
        message = str(error)

        if status_code == 400:
            raise APIValidationError(f"Bad request: {message}")
        elif status_code == 401:
            raise APIAuthenticationError(f"Authentication failed: {message}")
        elif status_code == 403:
            raise APIAuthorizationError(f"Access forbidden: {message}")
        elif status_code == 404:
            raise APINotFoundError(f"Resource not found: {message}")
        elif status_code == 429:
            raise APIRateLimitError(f"Rate limit exceeded: {message}")
        elif 500 <= status_code < 600:
            raise APIServerError(f"Server error ({status_code}): {message}")
        else:
            raise APIError(f"HTTP {status_code}: {message}")

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async GET request."""
        return await self._make_request('GET', endpoint, params=params)

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async POST request."""
        return await self._make_request('POST', endpoint, json=data)

    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async PUT request."""
        return await self._make_request('PUT', endpoint, json=data)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Async DELETE request."""
        return await self._make_request('DELETE', endpoint)
```

## Specialized API Clients

### GraphQL Client

```python
import requests
from typing import Dict, Optional, Any
import json

class GraphQLClient(APIClient):
    """GraphQL API client."""

    def query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GraphQL query."""
        payload = {'query': query}
        if variables:
            payload['variables'] = variables

        response = self.post('graphql', payload)

        if 'errors' in response:
            raise GraphQLError(f"GraphQL errors: {response['errors']}")

        return response.get('data', {})

    def mutate(self, mutation: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GraphQL mutation."""
        return self.query(mutation, variables)
```

### REST API with Pagination

```python
from typing import List, Dict, Any, Iterator, Optional
import logging

logger = logging.getLogger(__name__)

class PaginatedAPIClient(APIClient):
    """API client with automatic pagination support."""

    def get_paginated(self, endpoint: str, page_size: int = 50,
                     max_pages: Optional[int] = None) -> Iterator[Dict[str, Any]]:
        """Get paginated results as iterator."""
        page = 1

        while max_pages is None or page <= max_pages:
            params = {
                'page': page,
                'per_page': page_size
            }

            try:
                response = self.get(endpoint, params=params)
                items = response.get('items', response.get('data', []))

                if not items:
                    break

                for item in items:
                    yield item

                page += 1

                # Check if there are more pages
                if 'has_more' in response and not response['has_more']:
                    break
                if 'next_page' in response and not response['next_page']:
                    break

            except APINotFoundError:
                break  # No more pages
            except Exception as e:
                logger.error(f"Error fetching page {page}: {e}")
                break

    def get_all(self, endpoint: str, page_size: int = 50) -> List[Dict[str, Any]]:
        """Get all paginated results as list."""
        return list(self.get_paginated(endpoint, page_size))
```

## Authentication Patterns

### OAuth2 Client Credentials

```python
import time
from typing import Optional

class OAuth2Client(APIClient):
    """API client with OAuth2 client credentials flow."""

    def __init__(self, base_url: str, client_id: str, client_secret: str,
                 token_url: str, **kwargs):
        super().__init__(base_url, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self._token = None
        self._token_expires = 0

    def _get_access_token(self) -> str:
        """Get valid access token, refreshing if necessary."""
        if self._token and time.time() < self._token_expires:
            return self._token

        # Request new token
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(self.token_url, data=data)
        response.raise_for_status()

        token_data = response.json()
        self._token = token_data['access_token']
        self._token_expires = time.time() + token_data.get('expires_in', 3600) - 60

        return self._token

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make request with automatic token refresh."""
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Authorization'] = f'Bearer {self._get_access_token()}'
        return super()._make_request(method, endpoint, **kwargs)
```

### API Key with HMAC

```python
import hmac
import hashlib
import time
from typing import Dict, Any

class HMACClient(APIClient):
    """API client with HMAC authentication."""

    def __init__(self, base_url: str, api_key: str, secret_key: str, **kwargs):
        super().__init__(base_url, api_key, **kwargs)
        self.secret_key = secret_key

    def _generate_signature(self, method: str, endpoint: str, timestamp: str,
                          body: str = "") -> str:
        """Generate HMAC signature."""
        message = f"{method.upper()}{endpoint}{timestamp}{body}"
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make request with HMAC signature."""
        timestamp = str(int(time.time()))
        body = json.dumps(kwargs.get('json', {})) if 'json' in kwargs else ""

        signature = self._generate_signature(method, endpoint, timestamp, body)

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers'].update({
            'X-API-Key': self.api_key,
            'X-Timestamp': timestamp,
            'X-Signature': signature
        })

        return super()._make_request(method, endpoint, **kwargs)
```

## Error Handling Patterns

### Custom Exceptions

```python
class APIError(Exception):
    """Base API exception."""
    pass

class APIConnectionError(APIError):
    """Connection-related errors."""
    pass

class APITimeoutError(APIError):
    """Request timeout errors."""
    pass

class APIAuthenticationError(APIError):
    """Authentication failures."""
    pass

class APIAuthorizationError(APIError):
    """Authorization failures."""
    pass

class APINotFoundError(APIError):
    """Resource not found."""
    pass

class APIValidationError(APIError):
    """Request validation errors."""
    pass

class APIRateLimitError(APIError):
    """Rate limiting errors."""
    pass

class APIServerError(APIError):
    """Server-side errors."""
    pass

class GraphQLError(APIError):
    """GraphQL-specific errors."""
    pass
```

### Error Recovery Strategies

```python
import time
from functools import wraps
from typing import Callable, Any

def retry_on_error(max_retries: int = 3, backoff_factor: float = 1.0,
                   exceptions: tuple = (APIConnectionError, APITimeoutError, APIServerError)):
    """Decorator to retry API calls on specific exceptions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = backoff_factor * (2 ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed")

            raise last_exception
        return wrapper
    return decorator
```

## Testing Patterns

### Mock API Client for Testing

```python
from unittest.mock import Mock, patch
import pytest

class MockAPIClient:
    """Mock API client for testing."""

    def __init__(self, responses: Dict[str, Any]):
        self.responses = responses
        self.requests = []

    def get(self, endpoint: str, params=None):
        self.requests.append(('GET', endpoint, params))
        return self.responses.get(endpoint, {})

    def post(self, endpoint: str, data=None):
        self.requests.append(('POST', endpoint, data))
        return self.responses.get(endpoint, {})

@pytest.fixture
def mock_client():
    """Fixture providing mock API client."""
    responses = {
        'users/1': {'id': 1, 'name': 'John Doe'},
        'users': [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Doe'}]
    }
    return MockAPIClient(responses)

def test_get_user(mock_client):
    """Test getting user data."""
    result = mock_client.get('users/1')
    assert result['id'] == 1
    assert result['name'] == 'John Doe'
    assert mock_client.requests[0] == ('GET', 'users/1', None)
```

## Usage Examples

### Basic Usage

```python
# Synchronous client
client = APIClient('https://api.example.com', api_key='your-key')

try:
    user = client.get('users/123')
    print(f"User: {user['name']}")
except APIAuthenticationError:
    print("Authentication failed")
except APINotFoundError:
    print("User not found")

# Async client
async with AsyncAPIClient('https://api.example.com', api_key='your-key') as client:
    users = await client.get('users')
    print(f"Found {len(users)} users")
```

### Advanced Usage with Pagination

```python
client = PaginatedAPIClient('https://api.example.com')

# Get all users as iterator (memory efficient)
for user in client.get_paginated('users', page_size=100):
    process_user(user)

# Or get all as list
all_users = client.get_all('users')
print(f"Total users: {len(all_users)}")
```

### OAuth2 Usage

```python
client = OAuth2Client(
    base_url='https://api.example.com',
    client_id='your-client-id',
    client_secret='your-client-secret',
    token_url='https://auth.example.com/oauth2/token'
)

# Token is automatically managed
data = client.get('protected-resource')
```

This comprehensive set of patterns provides a solid foundation for building robust, maintainable API clients in Python across various use cases and authentication methods.