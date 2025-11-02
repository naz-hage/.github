# Python Error Handling Patterns

This guide covers comprehensive error handling patterns and best practices for Python applications, focusing on exception handling, error recovery, and robust application design.

## Exception Hierarchy and Custom Exceptions

### Base Exception Classes

```python
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ApplicationError(Exception):
    """Base exception for application-specific errors."""

    def __init__(self, message: str, error_code: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }

class ValidationError(ApplicationError):
    """Raised when input validation fails."""
    pass

class NotFoundError(ApplicationError):
    """Raised when a requested resource is not found."""
    pass

class PermissionError(ApplicationError):
    """Raised when user lacks permission for an operation."""
    pass

class ConfigurationError(ApplicationError):
    """Raised when application configuration is invalid."""
    pass

class ExternalServiceError(ApplicationError):
    """Raised when external service calls fail."""
    pass
```

### Domain-Specific Exceptions

```python
# User management exceptions
class UserError(ApplicationError):
    """Base class for user-related errors."""
    pass

class UserNotFoundError(UserError):
    """Raised when user is not found."""
    pass

class UserAlreadyExistsError(UserError):
    """Raised when attempting to create duplicate user."""
    pass

class InvalidCredentialsError(UserError):
    """Raised when user credentials are invalid."""
    pass

# Payment processing exceptions
class PaymentError(ApplicationError):
    """Base class for payment-related errors."""
    pass

class PaymentDeclinedError(PaymentError):
    """Raised when payment is declined."""
    pass

class InsufficientFundsError(PaymentError):
    """Raised when account has insufficient funds."""
    pass

class PaymentTimeoutError(PaymentError):
    """Raised when payment processing times out."""
    pass
```

## Error Handling Patterns

### Try-Except-Finally Pattern

```python
import traceback
from contextlib import contextmanager

@contextmanager
def error_context(operation: str, logger: logging.Logger = None):
    """Context manager for consistent error handling."""
    logger = logger or logging.getLogger(__name__)

    try:
        yield
    except ApplicationError:
        # Re-raise application errors as-is
        raise
    except Exception as e:
        # Wrap unexpected errors
        logger.error(f"Unexpected error during {operation}: {e}")
        logger.error(traceback.format_exc())
        raise ApplicationError(f"Operation '{operation}' failed: {e}") from e
    finally:
        # Cleanup code here
        pass

def process_user_data(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """Process user data with comprehensive error handling."""
    with error_context(f"processing user {user_id}"):
        # Validate input
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("Invalid user ID", error_code="INVALID_USER_ID")

        if not data or not isinstance(data, dict):
            raise ValidationError("Invalid user data", error_code="INVALID_DATA")

        # Check if user exists
        user = get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found", error_code="USER_NOT_FOUND")

        # Validate permissions
        if not has_permission(user, 'update_profile'):
            raise PermissionError("Insufficient permissions to update user",
                                error_code="INSUFFICIENT_PERMISSIONS")

        # Process data
        try:
            processed_data = validate_and_transform_data(data)
            update_user_profile(user_id, processed_data)
            return {"status": "success", "user_id": user_id}
        except ValueError as e:
            raise ValidationError(f"Data validation failed: {e}", error_code="VALIDATION_FAILED")
        except DatabaseError as e:
            logger.error(f"Database error updating user {user_id}: {e}")
            raise ApplicationError("Failed to update user profile", error_code="DATABASE_ERROR") from e
```

### Error Recovery and Retry Patterns

```python
import time
import random
from functools import wraps
from typing import Callable, Type, Union, Tuple

def retry_on_exceptions(max_retries: int = 3,
                       backoff_factor: float = 1.0,
                       jitter: bool = True,
                       exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    """
    Decorator to retry function calls on specified exceptions.

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Exponential backoff factor
        jitter: Add random jitter to delay
        exceptions: Tuple of exception types to retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
                        break

                    # Calculate delay with exponential backoff
                    delay = backoff_factor * (2 ** attempt)
                    if jitter:
                        delay *= random.uniform(0.5, 1.5)

                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator

class ExternalAPIService:
    """Service for calling external APIs with retry logic."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

    @retry_on_exceptions(
        max_retries=3,
        backoff_factor=1.0,
        exceptions=(requests.exceptions.ConnectionError,
                   requests.exceptions.Timeout,
                   requests.exceptions.HTTPError)
    )
    def call_external_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call external API with automatic retry on failures."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.post(
                url,
                json=data,
                headers={'Authorization': f'Bearer {self.api_key}'},
                timeout=10
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code >= 500:
                # Retry on server errors
                raise
            elif e.response.status_code == 429:
                # Rate limited - retry with longer delay
                raise
            else:
                # Don't retry on client errors
                raise ExternalServiceError(
                    f"API call failed: {e.response.status_code}",
                    error_code="API_CLIENT_ERROR",
                    details={'status_code': e.response.status_code, 'response': e.response.text}
                ) from e
        except requests.exceptions.RequestException as e:
            raise ExternalServiceError(
                f"Network error calling external API: {e}",
                error_code="API_NETWORK_ERROR"
            ) from e
```

### Circuit Breaker Pattern

```python
import threading
from enum import Enum
from typing import Optional

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, requests rejected
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker for external service calls."""

    def __init__(self, failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 expected_exception: Type[Exception] = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._lock = threading.Lock()

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        with self._lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise CircuitBreakerError("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)

            # Success - reset failure count
            with self._lock:
                self.failure_count = 0
                self.state = CircuitState.CLOSED

            return result

        except self.expected_exception as e:
            self._record_failure()
            raise

    def _record_failure(self):
        """Record a failure and potentially open the circuit."""
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit breaker opened after {self.failure_count} failures")

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        if self.last_failure_time is None:
            return True

        return (time.time() - self.last_failure_time) >= self.recovery_timeout

class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""
    pass

# Usage example
circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=30,
    expected_exception=ExternalServiceError
)

def safe_external_call():
    """Call external service with circuit breaker protection."""
    return circuit_breaker.call(external_api_service.call_endpoint, data)
```

## Error Propagation and Context

### Error Context Preservation

```python
from contextlib import contextmanager
from typing import Generator

class ErrorContext:
    """Context manager for preserving error context across call stacks."""

    def __init__(self):
        self.context_stack = []

    @contextmanager
    def push_context(self, operation: str, **context_data) -> Generator[None, None, None]:
        """Push error context onto the stack."""
        context = {
            'operation': operation,
            'timestamp': datetime.utcnow(),
            **context_data
        }

        self.context_stack.append(context)
        try:
            yield
        except Exception as e:
            # Enrich exception with context
            if hasattr(e, 'details'):
                e.details.update({'error_context': self.context_stack.copy()})
            raise
        finally:
            self.context_stack.pop()

    def get_current_context(self) -> list:
        """Get current error context stack."""
        return self.context_stack.copy()

# Global error context
error_context = ErrorContext()

def process_payment(user_id: int, amount: float, payment_method: Dict[str, Any]) -> Dict[str, Any]:
    """Process payment with comprehensive error context."""
    with error_context.push_context('process_payment',
                                   user_id=user_id,
                                   amount=amount,
                                   payment_method_type=payment_method.get('type')):
        # Validate payment data
        with error_context.push_context('validate_payment_data'):
            validate_payment_data(amount, payment_method)

        # Check user balance
        with error_context.push_context('check_user_balance'):
            balance = get_user_balance(user_id)
            if balance < amount:
                raise InsufficientFundsError(
                    f"Insufficient funds: balance {balance}, required {amount}",
                    error_code="INSUFFICIENT_FUNDS",
                    details={'balance': balance, 'required': amount}
                )

        # Process payment
        with error_context.push_context('execute_payment'):
            try:
                transaction_id = payment_gateway.charge(amount, payment_method)
                return {
                    'status': 'success',
                    'transaction_id': transaction_id,
                    'amount': amount
                }
            except PaymentGatewayError as e:
                raise PaymentDeclinedError(
                    f"Payment declined: {e}",
                    error_code="PAYMENT_DECLINED",
                    details={'gateway_error': str(e)}
                ) from e
```

### Structured Error Responses

```python
from typing import Union
import json

class ErrorResponse:
    """Structured error response for APIs."""

    def __init__(self, exception: Exception, include_traceback: bool = False):
        self.exception = exception
        self.include_traceback = include_traceback

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to structured dictionary."""
        response = {
            'success': False,
            'error': {
                'type': self.exception.__class__.__name__,
                'message': str(self.exception),
            }
        }

        if hasattr(self.exception, 'error_code') and self.exception.error_code:
            response['error']['code'] = self.exception.error_code

        if hasattr(self.exception, 'details') and self.exception.details:
            response['error']['details'] = self.exception.details

        if hasattr(self.exception, 'timestamp'):
            response['error']['timestamp'] = self.exception.timestamp.isoformat()

        if self.include_traceback and hasattr(self.exception, '__traceback__'):
            response['error']['traceback'] = traceback.format_exception(
                type(self.exception),
                self.exception,
                self.exception.__traceback__
            )

        return response

    def to_json(self) -> str:
        """Convert error to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)

def handle_api_error(exception: Exception) -> tuple:
    """Handle API errors and return appropriate response."""
    # Log the error
    logger.error(f"API error: {exception}", exc_info=True)

    # Determine HTTP status code
    if isinstance(exception, ValidationError):
        status_code = 400
    elif isinstance(exception, NotFoundError):
        status_code = 404
    elif isinstance(exception, PermissionError):
        status_code = 403
    elif isinstance(exception, ExternalServiceError):
        status_code = 502
    else:
        status_code = 500

    # Create error response
    error_response = ErrorResponse(exception, include_traceback=status_code >= 500)

    return error_response.to_dict(), status_code
```

## Async Error Handling

### Async Error Patterns

```python
import asyncio
from typing import Awaitable, TypeVar

T = TypeVar('T')

async def async_retry_on_exceptions(func: Callable[..., Awaitable[T]],
                                   max_retries: int = 3,
                                   backoff_factor: float = 1.0,
                                   exceptions: Tuple[Type[Exception], ...] = (Exception,)) -> T:
    """Async version of retry decorator."""
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return await func()
        except exceptions as e:
            last_exception = e

            if attempt == max_retries:
                logger.error(f"All {max_retries + 1} async attempts failed")
                break

            delay = backoff_factor * (2 ** attempt)
            logger.warning(f"Async attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            await asyncio.sleep(delay)

    raise last_exception

class AsyncErrorHandler:
    """Handle errors in async contexts."""

    @staticmethod
    async def gather_with_error_handling(*coroutines, continue_on_error: bool = False):
        """Execute multiple coroutines and handle errors."""
        results = []
        errors = []

        for coro in asyncio.as_completed(coroutines):
            try:
                result = await coro
                results.append(result)
            except Exception as e:
                errors.append(e)
                if not continue_on_error:
                    # Cancel remaining tasks
                    for task in asyncio.all_tasks():
                        if not task.done():
                            task.cancel()
                    break

        return results, errors

    @staticmethod
    async def execute_with_timeout(coro: Awaitable[T], timeout: float) -> T:
        """Execute coroutine with timeout."""
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            raise ApplicationError(
                f"Operation timed out after {timeout} seconds",
                error_code="TIMEOUT_ERROR",
                details={'timeout': timeout}
            )

# Usage example
async def process_multiple_users(user_ids: List[int]) -> Tuple[List[Dict], List[Exception]]:
    """Process multiple users concurrently with error handling."""
    async def process_single_user(user_id: int):
        async with error_context.push_context('process_user', user_id=user_id):
            return await user_service.process_user_data(user_id)

    # Create coroutines for each user
    coroutines = [process_single_user(uid) for uid in user_ids]

    # Execute with error handling
    results, errors = await AsyncErrorHandler.gather_with_error_handling(
        *coroutines,
        continue_on_error=True
    )

    return results, errors
```

## Logging and Monitoring

### Structured Error Logging

```python
import structlog
from typing import Any, Dict

class ErrorLogger:
    """Structured error logging."""

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or structlog.get_logger()

    def log_error(self, exception: Exception, context: Dict[str, Any] = None):
        """Log error with structured context."""
        error_data = {
            'error_type': exception.__class__.__name__,
            'error_message': str(exception),
            'traceback': traceback.format_exception(
                type(exception), exception, exception.__traceback__
            )
        }

        if hasattr(exception, 'error_code'):
            error_data['error_code'] = exception.error_code

        if hasattr(exception, 'details'):
            error_data['details'] = exception.details

        if context:
            error_data['context'] = context

        self.logger.error("Application error occurred", **error_data)

    def log_error_with_metrics(self, exception: Exception, metrics_collector=None):
        """Log error and update metrics."""
        self.log_error(exception)

        if metrics_collector:
            # Increment error counters
            metrics_collector.increment(f"errors.{exception.__class__.__name__}")

            if hasattr(exception, 'error_code'):
                metrics_collector.increment(f"errors.code.{exception.error_code}")

# Usage in error handlers
error_logger = ErrorLogger()

def handle_unexpected_error(exception: Exception, request_context: Dict[str, Any] = None):
    """Handle unexpected errors with comprehensive logging."""
    error_logger.log_error(exception, request_context)

    # Send to error monitoring service
    if error_monitoring_service:
        error_monitoring_service.capture_exception(exception, context=request_context)

    # Return generic error response
    return {
        'success': False,
        'error': {
            'type': 'InternalServerError',
            'message': 'An unexpected error occurred'
        }
    }
```

## Testing Error Conditions

### Error Testing Patterns

```python
import pytest
from unittest.mock import Mock, patch

class TestErrorHandling:
    """Test error handling patterns."""

    def test_validation_error_propagation(self, user_service):
        """Test that validation errors are properly propagated."""
        invalid_data = {'email': 'invalid-email'}

        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(invalid_data)

        assert exc_info.value.error_code == "VALIDATION_FAILED"
        assert 'email' in exc_info.value.details

    def test_not_found_error_handling(self, user_service):
        """Test handling of not found errors."""
        with patch.object(user_service.repository, 'get_by_id', return_value=None):
            with pytest.raises(NotFoundError) as exc_info:
                user_service.get_user(999)

            assert exc_info.value.error_code == "USER_NOT_FOUND"
            assert "999" in exc_info.value.message

    @pytest.mark.parametrize("exception_class,expected_status", [
        (ValidationError, 400),
        (NotFoundError, 404),
        (PermissionError, 403),
        (Exception, 500),
    ])
    def test_error_response_mapping(self, exception_class, expected_status):
        """Test that exceptions map to correct HTTP status codes."""
        exception = exception_class("Test error")
        response, status_code = handle_api_error(exception)

        assert status_code == expected_status
        assert response['success'] is False
        assert 'error' in response

    def test_retry_mechanism(self, external_service):
        """Test retry mechanism on transient failures."""
        call_count = 0

        def failing_call():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Temporary failure")
            return {"success": True}

        with patch.object(external_service, 'make_request', side_effect=failing_call):
            result = external_service.call_with_retry()

            assert result == {"success": True}
            assert call_count == 3  # Failed twice, succeeded on third try

    def test_circuit_breaker_open_state(self, circuit_breaker):
        """Test circuit breaker opens after threshold failures."""
        # Simulate failures
        for _ in range(5):
            with pytest.raises(CircuitBreakerError):
                circuit_breaker.call(lambda: (_ for _ in ()).throw(Exception("Service down")))

        # Circuit should be open
        with pytest.raises(CircuitBreakerError, match="Circuit breaker is OPEN"):
            circuit_breaker.call(lambda: "should not execute")
```

This comprehensive error handling guide provides patterns for building robust, maintainable Python applications with proper error management, recovery mechanisms, and monitoring capabilities.