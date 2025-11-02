# Error Handling Patterns

This document provides framework-neutral error handling patterns and best practices that can be adapted across different programming languages and platforms.

## Error Classification

### Application Error Types

#### Business Logic Errors
- **ValidationError**: Input validation failures
- **NotFoundError**: Resource doesn't exist
- **ConflictError**: Operation conflicts with current state
- **UnauthorizedError**: Authentication/authorization failures

#### System Errors
- **NetworkError**: Connection or timeout issues
- **TimeoutError**: Operation exceeded time limits
- **RateLimitError**: API rate limits exceeded
- **ServerError**: External service failures

#### Programming Errors
- **ConfigurationError**: Invalid configuration
- **TypeError**: Type mismatches
- **ValueError**: Invalid values

## Python Error Handling Patterns

### Exception Hierarchy
```python
from typing import Optional

class AppError(Exception):
    """Base application exception."""
    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.code = code

class ValidationError(AppError):
    """Input validation errors."""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field

class NotFoundError(AppError):
    """Resource not found errors."""
    def __init__(self, message: str, resource_type: str, resource_id: str):
        super().__init__(message, "NOT_FOUND")
        self.resource_type = resource_type
        self.resource_id = resource_id

class NetworkError(AppError):
    """Network-related errors."""
    def __init__(self, message: str, url: Optional[str] = None):
        super().__init__(message, "NETWORK_ERROR")
        self.url = url
```

### HTTP Error Handling
```python
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ApiClient:
    def _handle_http_error(self, error: requests.exceptions.HTTPError) -> None:
        """Handle HTTP errors with appropriate exceptions."""
        status_code = error.response.status_code
        url = error.response.url

        if status_code == 400:
            raise ValidationError("Invalid request parameters")
        elif status_code == 401:
            raise AppError("Authentication required", "AUTH_REQUIRED")
        elif status_code == 403:
            raise AppError("Access denied", "ACCESS_DENIED")
        elif status_code == 404:
            raise NotFoundError("Resource not found", "resource", url)
        elif status_code == 409:
            raise AppError("Resource conflict", "CONFLICT")
        elif status_code == 429:
            raise AppError("Rate limit exceeded", "RATE_LIMIT")
        elif 500 <= status_code < 600:
            raise AppError(f"Server error: {status_code}", "SERVER_ERROR")
        else:
            raise AppError(f"HTTP error: {status_code}", "HTTP_ERROR")

    def api_call(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API call with comprehensive error handling."""
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network connection failed: {e}")
            raise NetworkError("Unable to connect to service", str(self.base_url))
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            raise AppError("Request timed out", "TIMEOUT")
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise AppError("Invalid response format", "INVALID_RESPONSE")
```

### Input Validation
```python
from typing import Any, Callable, TypeVar

T = TypeVar('T')

def validate_required(value: Any, field_name: str) -> None:
    """Validate that a required field is present and not empty."""
    if value is None:
        raise ValidationError(f"Field '{field_name}' is required", field_name)
    if isinstance(value, str) and not value.strip():
        raise ValidationError(f"Field '{field_name}' cannot be empty", field_name)

def validate_string_length(value: str, field_name: str, min_len: int = 0, max_len: int = 255) -> None:
    """Validate string length constraints."""
    if len(value) < min_len:
        raise ValidationError(f"Field '{field_name}' must be at least {min_len} characters", field_name)
    if len(value) > max_len:
        raise ValidationError(f"Field '{field_name}' cannot exceed {max_len} characters", field_name)

def validate_with_validator(validator: Callable[[T], bool], value: T, field_name: str, error_message: str) -> None:
    """Validate using a custom validator function."""
    if not validator(value):
        raise ValidationError(error_message, field_name)
```

### Retry Logic with Exponential Backoff
```python
import time
from functools import wraps
from typing import Callable, Any

def retry_on_failure(max_attempts: int = 3, backoff_factor: float = 1.0,
                     exceptions: tuple = (NetworkError, AppError)):
    """Decorator to retry function on specified exceptions with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        wait_time = backoff_factor * (2 ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time:.1f}s: {e}")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
                        raise last_exception

            raise last_exception
        return wrapper
    return decorator

# Usage
@retry_on_failure(max_attempts=3, exceptions=(NetworkError, TimeoutError))
def fetch_data_with_retry(self, endpoint: str) -> Dict[str, Any]:
    """Fetch data with automatic retry on network failures."""
    return self.api_call(endpoint)
```

## JavaScript/TypeScript Error Handling Patterns

### Error Classes
```typescript
// TypeScript error classes
class AppError extends Error {
  public readonly code?: string;
  public readonly statusCode?: number;

  constructor(message: string, code?: string, statusCode?: number) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
  }
}

class ValidationError extends AppError {
  public readonly field?: string;

  constructor(message: string, field?: string) {
    super(message, 'VALIDATION_ERROR');
    this.name = 'ValidationError';
    this.field = field;
  }
}

class NotFoundError extends AppError {
  public readonly resourceType: string;
  public readonly resourceId: string;

  constructor(message: string, resourceType: string, resourceId: string) {
    super(message, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
    this.resourceType = resourceType;
    this.resourceId = resourceId;
  }
}

class NetworkError extends AppError {
  public readonly url?: string;

  constructor(message: string, url?: string) {
    super(message, 'NETWORK_ERROR');
    this.name = 'NetworkError';
    this.url = url;
  }
}
```

### Async Error Handling
```typescript
class ApiClient {
  private async handleHttpError(response: Response): Promise<never> {
    const url = response.url;

    switch (response.status) {
      case 400:
        throw new ValidationError('Invalid request parameters');
      case 401:
        throw new AppError('Authentication required', 'AUTH_REQUIRED', 401);
      case 403:
        throw new AppError('Access denied', 'ACCESS_DENIED', 403);
      case 404:
        throw new NotFoundError('Resource not found', 'resource', url);
      case 409:
        throw new AppError('Resource conflict', 'CONFLICT', 409);
      case 429:
        throw new AppError('Rate limit exceeded', 'RATE_LIMIT', 429);
      default:
        if (response.status >= 500) {
          throw new AppError(`Server error: ${response.status}`, 'SERVER_ERROR', response.status);
        }
        throw new AppError(`HTTP error: ${response.status}`, 'HTTP_ERROR', response.status);
    }
  }

  async apiCall(endpoint: string, options: RequestInit = {}): Promise<any> {
    const url = `${this.baseUrl}/${endpoint.replace(/^\//, '')}`;

    try {
      const response = await fetch(url, {
        ...options,
        signal: AbortSignal.timeout(this.timeout)
      });

      if (!response.ok) {
        await this.handleHttpError(response);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }

      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new NetworkError('Network connection failed', url);
      }

      if (error instanceof Error && error.name === 'AbortError') {
        throw new AppError('Request timed out', 'TIMEOUT');
      }

      throw new AppError(error instanceof Error ? error.message : 'Unknown error');
    }
  }
}
```

### Input Validation
```typescript
// TypeScript validation utilities
function validateRequired<T>(value: T | null | undefined, fieldName: string): T {
  if (value === null || value === undefined) {
    throw new ValidationError(`Field '${fieldName}' is required`, fieldName);
  }
  return value;
}

function validateStringLength(value: string, fieldName: string, minLength: number = 0, maxLength: number = 255): void {
  if (value.length < minLength) {
    throw new ValidationError(`Field '${fieldName}' must be at least ${minLength} characters`, fieldName);
  }
  if (value.length > maxLength) {
    throw new ValidationError(`Field '${fieldName}' cannot exceed ${maxLength} characters`, fieldName);
  }
}

function validateWithPredicate<T>(
  predicate: (value: T) => boolean,
  value: T,
  fieldName: string,
  errorMessage: string
): void {
  if (!predicate(value)) {
    throw new ValidationError(errorMessage, fieldName);
  }
}

// Usage with Zod (recommended for complex validation)
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().min(0).max(150).optional()
});

function validateUser(data: unknown): z.infer<typeof userSchema> {
  try {
    return userSchema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      const fieldErrors = error.errors.map(err => `${err.path.join('.')}: ${err.message}`);
      throw new ValidationError(`Validation failed: ${fieldErrors.join(', ')}`);
    }
    throw error;
  }
}
```

### Retry Logic
```typescript
function withRetry<T>(
  operation: () => Promise<T>,
  maxAttempts: number = 3,
  backoffFactor: number = 1000,
  retryableErrors: (new Set([NetworkError, AppError]))
): Promise<T> {
  return new Promise(async (resolve, reject) => {
    let lastError: Error;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      try {
        const result = await operation();
        resolve(result);
        return;
      } catch (error) {
        lastError = error as Error;

        // Check if error is retryable
        const isRetryable = Array.from(retryableErrors).some(errorType =>
          error instanceof errorType
        );

        if (!isRetryable || attempt === maxAttempts - 1) {
          reject(lastError);
          return;
        }

        const waitTime = backoffFactor * Math.pow(2, attempt);
        console.warn(`Attempt ${attempt + 1} failed, retrying in ${waitTime}ms:`, error);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }
    }
  });
}

// Usage
const result = await withRetry(
  () => apiClient.fetchData(endpoint),
  3, // max attempts
  1000, // base backoff in ms
  new Set([NetworkError]) // retry only network errors
);
```

## Java Error Handling Patterns

### Exception Hierarchy
```java
// Java exception hierarchy
public class AppException extends Exception {
    private final String code;

    public AppException(String message, String code) {
        super(message);
        this.code = code;
    }

    public AppException(String message, String code, Throwable cause) {
        super(message, cause);
        this.code = code;
    }

    public String getCode() {
        return code;
    }
}

public class ValidationException extends AppException {
    private final String field;

    public ValidationException(String message, String field) {
        super(message, "VALIDATION_ERROR");
        this.field = field;
    }

    public String getField() {
        return field;
    }
}

public class NotFoundException extends AppException {
    private final String resourceType;
    private final String resourceId;

    public NotFoundException(String message, String resourceType, String resourceId) {
        super(message, "NOT_FOUND");
        this.resourceType = resourceType;
        this.resourceId = resourceId;
    }

    public String getResourceType() {
        return resourceType;
    }

    public String getResourceId() {
        return resourceId;
    }
}

public class NetworkException extends AppException {
    private final String url;

    public NetworkException(String message, String url) {
        super(message, "NETWORK_ERROR");
        this.url = url;
    }

    public String getUrl() {
        return url;
    }
}
```

### HTTP Error Handling
```java
import java.io.IOException;
import java.net.http.HttpResponse;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ApiClient {
    private static final Logger logger = LoggerFactory.getLogger(ApiClient.class);
    private final HttpClient httpClient;
    private final String baseUrl;
    private final ObjectMapper objectMapper;

    public ApiClient(String baseUrl) {
        this.baseUrl = baseUrl.replaceAll("/$", "");
        this.objectMapper = new ObjectMapper();
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(java.time.Duration.ofSeconds(30))
            .build();
    }

    private void handleHttpError(HttpResponse<String> response) throws AppException {
        int statusCode = response.statusCode();
        String url = response.uri().toString();

        switch (statusCode) {
            case 400:
                throw new ValidationException("Invalid request parameters", null);
            case 401:
                throw new AppException("Authentication required", "AUTH_REQUIRED");
            case 403:
                throw new AppException("Access denied", "ACCESS_DENIED");
            case 404:
                throw new NotFoundException("Resource not found", "resource", url);
            case 409:
                throw new AppException("Resource conflict", "CONFLICT");
            case 429:
                throw new AppException("Rate limit exceeded", "RATE_LIMIT");
            default:
                if (statusCode >= 500) {
                    throw new AppException("Server error: " + statusCode, "SERVER_ERROR");
                }
                throw new AppException("HTTP error: " + statusCode, "HTTP_ERROR");
        }
    }

    public <T> T apiCall(String endpoint, Class<T> responseType) throws AppException {
        String url = baseUrl + "/" + endpoint.replaceAll("^/", "");

        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(java.net.URI.create(url))
                .timeout(java.time.Duration.ofSeconds(30))
                .GET()
                .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() >= 400) {
                handleHttpError(response);
            }

            return objectMapper.readValue(response.body(), responseType);

        } catch (IOException e) {
            logger.error("Network error: {}", e.getMessage());
            throw new NetworkException("Unable to connect to service", url);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new AppException("Request was interrupted", "INTERRUPTED");
        } catch (java.util.concurrent.TimeoutException e) {
            throw new AppException("Request timed out", "TIMEOUT");
        } catch (Exception e) {
            logger.error("Unexpected error: {}", e.getMessage(), e);
            throw new AppException("An unexpected error occurred", "UNKNOWN_ERROR", e);
        }
    }
}
```

### Input Validation
```java
import java.util.function.Predicate;

public class ValidationUtils {
    public static <T> T requireNonNull(T value, String fieldName) {
        if (value == null) {
            throw new ValidationException("Field '" + fieldName + "' is required", fieldName);
        }
        return value;
    }

    public static String validateStringLength(String value, String fieldName, int minLength, int maxLength) {
        requireNonNull(value, fieldName);

        if (value.length() < minLength) {
            throw new ValidationException(
                "Field '" + fieldName + "' must be at least " + minLength + " characters",
                fieldName
            );
        }

        if (value.length() > maxLength) {
            throw new ValidationException(
                "Field '" + fieldName + "' cannot exceed " + maxLength + " characters",
                fieldName
            );
        }

        return value;
    }

    public static <T> T validateWithPredicate(
            Predicate<T> predicate,
            T value,
            String fieldName,
            String errorMessage) {
        requireNonNull(value, fieldName);

        if (!predicate.test(value)) {
            throw new ValidationException(errorMessage, fieldName);
        }

        return value;
    }
}

// Usage
public class UserValidator {
    private static final Predicate<String> EMAIL_PATTERN =
        Pattern.compile("^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$").asPredicate();

    public static User validateUser(String name, String email, Integer age) {
        String validatedName = ValidationUtils.validateStringLength(name, "name", 1, 100);
        String validatedEmail = ValidationUtils.validateWithPredicate(
            EMAIL_PATTERN, email, "email", "Invalid email format"
        );

        if (age != null && (age < 0 || age > 150)) {
            throw new ValidationException("Age must be between 0 and 150", "age");
        }

        return new User(validatedName, validatedEmail, age);
    }
}
```

## C# Error Handling Patterns

### Exception Hierarchy
```csharp
using System;

[Serializable]
public class AppException : Exception
{
    public string Code { get; }

    public AppException(string message, string code = null) : base(message)
    {
        Code = code;
    }

    public AppException(string message, string code, Exception innerException)
        : base(message, innerException)
    {
        Code = code;
    }
}

public class ValidationException : AppException
{
    public string Field { get; }

    public ValidationException(string message, string field = null)
        : base(message, "VALIDATION_ERROR")
    {
        Field = field;
    }
}

public class NotFoundException : AppException
{
    public string ResourceType { get; }
    public string ResourceId { get; }

    public NotFoundException(string message, string resourceType, string resourceId)
        : base(message, "NOT_FOUND")
    {
        ResourceType = resourceType;
        ResourceId = resourceId;
    }
}

public class NetworkException : AppException
{
    public string Url { get; }

    public NetworkException(string message, string url = null)
        : base(message, "NETWORK_ERROR")
    {
        Url = url;
    }
}
```

### HTTP Error Handling
```csharp
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.Extensions.Logging;

public class ApiClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ApiClient> _logger;
    private readonly string _baseUrl;

    public ApiClient(string baseUrl, HttpClient httpClient, ILogger<ApiClient> logger)
    {
        _baseUrl = baseUrl.TrimEnd('/');
        _httpClient = httpClient;
        _logger = logger;
    }

    private void HandleHttpError(HttpResponseMessage response)
    {
        var statusCode = (int)response.StatusCode;
        var url = response.RequestMessage?.RequestUri?.ToString();

        switch (statusCode)
        {
            case 400:
                throw new ValidationException("Invalid request parameters");
            case 401:
                throw new AppException("Authentication required", "AUTH_REQUIRED");
            case 403:
                throw new AppException("Access denied", "ACCESS_DENIED");
            case 404:
                throw new NotFoundException("Resource not found", "resource", url);
            case 409:
                throw new AppException("Resource conflict", "CONFLICT");
            case 429:
                throw new AppException("Rate limit exceeded", "RATE_LIMIT");
            default:
                if (statusCode >= 500)
                {
                    throw new AppException($"Server error: {statusCode}", "SERVER_ERROR");
                }
                throw new AppException($"HTTP error: {statusCode}", "HTTP_ERROR");
        }
    }

    public async Task<T> ApiCallAsync<T>(string endpoint, CancellationToken cancellationToken = default)
    {
        var url = $"{_baseUrl}/{endpoint.TrimStart('/')}";

        try
        {
            var response = await _httpClient.GetAsync(url, cancellationToken);

            if (!response.IsSuccessStatusCode)
            {
                HandleHttpError(response);
            }

            return await response.Content.ReadFromJsonAsync<T>(cancellationToken: cancellationToken);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Network error for {Url}", url);
            throw new NetworkException("Unable to connect to service", url);
        }
        catch (TaskCanceledException ex) when (!cancellationToken.IsCancellationRequested)
        {
            _logger.LogError(ex, "Request timed out for {Url}", url);
            throw new AppException("Request timed out", "TIMEOUT");
        }
        catch (JsonException ex)
        {
            _logger.LogError(ex, "Invalid JSON response from {Url}", url);
            throw new AppException("Invalid response format", "INVALID_RESPONSE");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error for {Url}", url);
            throw new AppException($"An unexpected error occurred: {ex.Message}", "UNKNOWN_ERROR", ex);
        }
    }
}
```

### Input Validation
```csharp
using System.ComponentModel.DataAnnotations;
using System.Text.RegularExpressions;

public static class ValidationUtils
{
    public static T RequireNonNull<T>(T value, string fieldName)
        where T : class
    {
        if (value == null)
        {
            throw new ValidationException($"Field '{fieldName}' is required", fieldName);
        }
        return value;
    }

    public static string ValidateStringLength(string value, string fieldName, int minLength = 0, int maxLength = int.MaxValue)
    {
        RequireNonNull(value, fieldName);

        if (value.Length < minLength)
        {
            throw new ValidationException(
                $"Field '{fieldName}' must be at least {minLength} characters",
                fieldName
            );
        }

        if (value.Length > maxLength)
        {
            throw new ValidationException(
                $"Field '{fieldName}' cannot exceed {maxLength} characters",
                fieldName
            );
        }

        return value;
    }

    public static T ValidateWithPredicate<T>(
        Func<T, bool> predicate,
        T value,
        string fieldName,
        string errorMessage)
    {
        RequireNonNull(value, fieldName);

        if (!predicate(value))
        {
            throw new ValidationException(errorMessage, fieldName);
        }

        return value;
    }
}

// Usage with Data Annotations (recommended for complex validation)
public class UserModel
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 1, ErrorMessage = "Name must be between 1 and 100 characters")]
    public string Name { get; set; }

    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email format")]
    public string Email { get; set; }

    [Range(0, 150, ErrorMessage = "Age must be between 0 and 150")]
    public int? Age { get; set; }
}

public class UserValidator
{
    public static UserModel ValidateUser(UserModel user)
    {
        var validationContext = new ValidationContext(user);
        var validationResults = new List<ValidationResult>();

        if (!Validator.TryValidateObject(user, validationContext, validationResults, true))
        {
            var errors = validationResults.Select(r => r.ErrorMessage);
            throw new ValidationException($"Validation failed: {string.Join(", ", errors)}");
        }

        return user;
    }
}
```

### Retry Logic
```csharp
using Polly;
using Polly.Retry;

public static class RetryUtils
{
    public static AsyncRetryPolicy CreateRetryPolicy(
        int maxAttempts = 3,
        double backoffFactor = 1.0,
        Func<Exception, bool> shouldRetry = null)
    {
        shouldRetry ??= (exception) =>
            exception is NetworkException ||
            exception is HttpRequestException ||
            exception is TaskCanceledException;

        return Policy
            .Handle(shouldRetry)
            .WaitAndRetryAsync(
                maxAttempts,
                attempt => TimeSpan.FromSeconds(backoffFactor * Math.Pow(2, attempt - 1)),
                (exception, waitTime, attempt, context) =>
                {
                    Console.WriteLine($"Attempt {attempt} failed, retrying in {waitTime.TotalSeconds:F1}s: {exception.Message}");
                }
            );
    }
}

// Usage
public class ApiService
{
    private readonly AsyncRetryPolicy _retryPolicy;

    public ApiService()
    {
        _retryPolicy = RetryUtils.CreateRetryPolicy();
    }

    public async Task<T> FetchDataWithRetryAsync<T>(string endpoint)
    {
        return await _retryPolicy.ExecuteAsync(async () =>
            await _apiClient.ApiCallAsync<T>(endpoint)
        );
    }
}
```

## Cross-Language Best Practices

### Error Message Guidelines
- **Be specific**: Explain exactly what went wrong
- **Be actionable**: Tell users how to fix the problem
- **Be consistent**: Use similar phrasing across similar errors
- **Don't expose internals**: Avoid showing stack traces or sensitive data
- **Include context**: Reference field names, resource IDs, etc.

### Logging Error Context
```python
# Python
def log_error_with_context(error: Exception, operation: str, context: Dict[str, Any]):
    logger.error(
        f"Operation '{operation}' failed",
        extra={
            'error_type': type(error).__name__,
            'error_message': str(error),
            'operation': operation,
            'context': context,
            'timestamp': datetime.utcnow().isoformat()
        },
        exc_info=True
    )
```

```typescript
// TypeScript
function logErrorWithContext(error: Error, operation: string, context: Record<string, any>): void {
  logger.error('Operation failed', {
    errorType: error.name,
    errorMessage: error.message,
    operation,
    context,
    timestamp: new Date().toISOString(),
    stack: error.stack
  });
}
```

### Graceful Degradation
```python
# Python
def get_data_with_fallback(primary_source: str, fallback_source: str = None) -> Optional[Dict]:
    """Try primary source, fall back to secondary if available."""
    try:
        return fetch_from_source(primary_source)
    except PermissionError:
        logger.warning(f"Primary source access denied, trying fallback")
        if fallback_source:
            try:
                return fetch_from_source(fallback_source)
            except Exception as e:
                logger.error(f"Fallback also failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        return None
```

### User-Friendly Error Messages

#### Good Examples
- "Repository 'my-repo' not found. Check the repository name and try again."
- "Authentication failed. Verify your API key is valid and has required permissions."
- "Network timeout. Check your internet connection and try again."

#### Bad Examples
- "API call failed" (too vague)
- "404" (not user-friendly)
- "Exception: 'NoneType' object has no attribute 'id'" (exposes implementation details)