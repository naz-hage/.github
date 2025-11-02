# Testing Scenarios for Multi-Language Development

This document provides comprehensive testing scenarios that work across multiple programming languages and frameworks. These scenarios ensure that Copilot-generated code is thoroughly tested, follows best practices, and handles edge cases appropriately.

## Overview

The testing scenarios are designed to be:
- **Language-agnostic**: Applicable to Python, JavaScript/TypeScript, Java, C#, and other languages
- **Framework-neutral**: Work with various testing frameworks and tools
- **Comprehensive**: Cover unit tests, integration tests, error handling, and edge cases
- **Practical**: Include real-world scenarios developers encounter

## 1. Input Validation Testing

**Scenario**: Developer needs to implement robust input validation for a CLI command that accepts user input.

**Test Steps**:
1. Open `.github/prompts/workflows/testing.md`
2. Follow the "Input Validation" section
3. Use Copilot to generate validation logic
4. Apply the testing patterns for comprehensive coverage

### Python Example
```python
import argparse
import sys
from typing import Optional

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_positive_integer(value: str) -> int:
    """Validate that input is a positive integer."""
    try:
        num = int(value)
        if num <= 0:
            raise ValidationError(f"Value must be positive, got {num}")
        return num
    except ValueError:
        raise ValidationError(f"Invalid integer: {value}")

def cmd_process_items(args: argparse.Namespace) -> None:
    """Process a specified number of items."""
    try:
        # Validate input
        count = validate_positive_integer(args.count)

        print(f"Processing {count} items...")
        # Process items...

    except ValidationError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)

# Unit tests
import unittest
from unittest.mock import patch

class TestInputValidation(unittest.TestCase):
    """Test input validation functionality."""

    def test_validate_positive_integer_valid(self):
        """Test valid positive integers."""
        self.assertEqual(validate_positive_integer("5"), 5)
        self.assertEqual(validate_positive_integer("100"), 100)

    def test_validate_positive_integer_zero(self):
        """Test that zero is rejected."""
        with self.assertRaises(ValidationError):
            validate_positive_integer("0")

    def test_validate_positive_integer_negative(self):
        """Test that negative numbers are rejected."""
        with self.assertRaises(ValidationError):
            validate_positive_integer("-1")

    def test_validate_positive_integer_invalid(self):
        """Test invalid input strings."""
        with self.assertRaises(ValidationError):
            validate_positive_integer("abc")

    @patch('sys.exit')
    def test_cmd_with_invalid_input(self, mock_exit):
        """Test CLI command with invalid input."""
        args = argparse.Namespace(count="invalid")
        cmd_process_items(args)
        mock_exit.assert_called_once_with(1)
```

### JavaScript/TypeScript Example
```javascript
interface ValidationResult {
    isValid: boolean;
    error?: string;
}

class ValidationError extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'ValidationError';
    }
}

function validatePositiveInteger(value: string): number {
    const num = parseInt(value, 10);
    if (isNaN(num)) {
        throw new ValidationError(`Invalid integer: ${value}`);
    }
    if (num <= 0) {
        throw new ValidationError(`Value must be positive, got ${num}`);
    }
    return num;
}

function processItems(count: string): void {
    try {
        const itemCount = validatePositiveInteger(count);
        console.log(`Processing ${itemCount} items...`);
        // Process items...
    } catch (error) {
        if (error instanceof ValidationError) {
            console.error(`[ERROR] ${error.message}`);
            process.exit(1);
        }
        console.error(`[ERROR] Unexpected error: ${error}`);
        process.exit(1);
    }
}

// Unit tests (Jest)
describe('Input Validation', () => {
    test('valid positive integers', () => {
        expect(validatePositiveInteger('5')).toBe(5);
        expect(validatePositiveInteger('100')).toBe(100);
    });

    test('rejects zero', () => {
        expect(() => validatePositiveInteger('0')).toThrow(ValidationError);
    });

    test('rejects negative numbers', () => {
        expect(() => validatePositiveInteger('-1')).toThrow(ValidationError);
    });

    test('rejects invalid input', () => {
        expect(() => validatePositiveInteger('abc')).toThrow(ValidationError);
    });
});
```

### Java Example
```java
public class ValidationError extends Exception {
    public ValidationError(String message) {
        super(message);
    }
}

public class InputValidator {
    public static int validatePositiveInteger(String value) throws ValidationError {
        try {
            int num = Integer.parseInt(value);
            if (num <= 0) {
                throw new ValidationError("Value must be positive, got " + num);
            }
            return num;
        } catch (NumberFormatException e) {
            throw new ValidationError("Invalid integer: " + value);
        }
    }
}

public class ItemProcessor {
    public static void processItems(String count) {
        try {
            int itemCount = InputValidator.validatePositiveInteger(count);
            System.out.println("Processing " + itemCount + " items...");
            // Process items...
        } catch (ValidationError e) {
            System.err.println("[ERROR] " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.err.println("[ERROR] Unexpected error: " + e.getMessage());
            System.exit(1);
        }
    }
}

// Unit tests (JUnit 5)
class InputValidationTest {
    @Test
    void testValidPositiveIntegers() {
        assertEquals(5, InputValidator.validatePositiveInteger("5"));
        assertEquals(100, InputValidator.validatePositiveInteger("100"));
    }

    @Test
    void testRejectsZero() {
        ValidationError exception = assertThrows(ValidationError.class,
            () -> InputValidator.validatePositiveInteger("0"));
        assertTrue(exception.getMessage().contains("positive"));
    }

    @Test
    void testRejectsNegativeNumbers() {
        assertThrows(ValidationError.class,
            () -> InputValidator.validatePositiveInteger("-1"));
    }

    @Test
    void testRejectsInvalidInput() {
        ValidationError exception = assertThrows(ValidationError.class,
            () -> InputValidator.validatePositiveInteger("abc"));
        assertTrue(exception.getMessage().contains("Invalid integer"));
    }
}
```

### C# Example
```csharp
public class ValidationError : Exception
{
    public ValidationError(string message) : base(message) { }
}

public static class InputValidator
{
    public static int ValidatePositiveInteger(string value)
    {
        if (!int.TryParse(value, out int num))
        {
            throw new ValidationError($"Invalid integer: {value}");
        }
        if (num <= 0)
        {
            throw new ValidationError($"Value must be positive, got {num}");
        }
        return num;
    }
}

public static class ItemProcessor
{
    public static void ProcessItems(string count)
    {
        try
        {
            int itemCount = InputValidator.ValidatePositiveInteger(count);
            Console.WriteLine($"Processing {itemCount} items...");
            // Process items...
        }
        catch (ValidationError e)
        {
            Console.Error.WriteLine($"[ERROR] {e.Message}");
            Environment.Exit(1);
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"[ERROR] Unexpected error: {e.Message}");
            Environment.Exit(1);
        }
    }
}

// Unit tests (xUnit)
public class InputValidationTests
{
    [Theory]
    [InlineData("5", 5)]
    [InlineData("100", 100)]
    public void TestValidPositiveIntegers(string input, int expected)
    {
        Assert.Equal(expected, InputValidator.ValidatePositiveInteger(input));
    }

    [Theory]
    [InlineData("0")]
    [InlineData("-1")]
    public void TestRejectsNonPositiveIntegers(string input)
    {
        Assert.Throws<ValidationError>(() => InputValidator.ValidatePositiveInteger(input));
    }

    [Theory]
    [InlineData("abc")]
    [InlineData("12.5")]
    public void TestRejectsInvalidInput(string input)
    {
        Assert.Throws<ValidationError>(() => InputValidator.ValidatePositiveInteger(input));
    }
}
```

**Validation Checklist**:
- [ ] Function follows language-specific patterns
- [ ] Proper error handling with custom exception types
- [ ] Input validation before processing
- [ ] Clear user feedback with appropriate exit codes
- [ ] Comprehensive unit test coverage

## 2. API Error Handling Testing

**Scenario**: Developer implements a REST API client and needs to handle various HTTP error responses appropriately.

**Test Steps**:
1. Open `.github/prompts/workflows/testing.md`
2. Follow the "API Testing" section
3. Use Copilot to generate error handling logic
4. Apply the testing patterns for comprehensive coverage

### Python Example
```python
import requests
from typing import Dict, Any
import time

class APIError(Exception):
    """Base exception for API errors."""
    pass

class AuthenticationError(APIError):
    """Exception for authentication failures."""
    pass

class RateLimitError(APIError):
    """Exception for rate limiting."""
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_key}'})

    def get_data(self, endpoint: str) -> Dict[str, Any]:
        """Fetch data from API with error handling."""
        url = f"{self.base_url}/{endpoint}"

        for attempt in range(3):
            try:
                response = self.session.get(url, timeout=30)
                return self._handle_response(response)
            except requests.exceptions.Timeout:
                if attempt == 2:  # Last attempt
                    raise APIError("Request timeout")
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.exceptions.ConnectionError:
                if attempt == 2:  # Last attempt
                    raise APIError("Connection failed")
                time.sleep(2 ** attempt)

        raise APIError("Max retries exceeded")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif response.status_code == 403:
            raise APIError("Access forbidden")
        elif response.status_code == 404:
            raise APIError("Resource not found")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            raise RateLimitError("Rate limit exceeded", retry_after)
        else:
            raise APIError(f"HTTP {response.status_code}: {response.text}")

# Unit tests
import unittest
from unittest.mock import patch, MagicMock

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient("https://api.example.com", "fake-key")

    def test_successful_request(self):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}

        with patch.object(self.client.session, 'get', return_value=mock_response):
            result = self.client.get_data("test")
            self.assertEqual(result, {"data": "test"})

    def test_authentication_error(self):
        """Test 401 authentication error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        with patch.object(self.client.session, 'get', return_value=mock_response):
            with self.assertRaises(AuthenticationError):
                self.client.get_data("test")

    def test_rate_limit_error(self):
        """Test 429 rate limit error."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '120'}
        mock_response.text = "Rate limit exceeded"

        with patch.object(self.client.session, 'get', return_value=mock_response):
            with self.assertRaises(RateLimitError) as cm:
                self.client.get_data("test")
            self.assertEqual(cm.exception.retry_after, 120)

    def test_timeout_retry(self):
        """Test timeout with retry logic."""
        with patch.object(self.client.session, 'get') as mock_get:
            mock_get.side_effect = [
                requests.exceptions.Timeout(),
                requests.exceptions.Timeout(),
                MagicMock(status_code=200, json=lambda: {"success": True})
            ]

            result = self.client.get_data("test")
            self.assertEqual(result, {"success": True})
            self.assertEqual(mock_get.call_count, 3)
```

### JavaScript/TypeScript Example
```typescript
class APIError extends Error {
    constructor(message: string, public statusCode?: number) {
        super(message);
        this.name = 'APIError';
    }
}

class AuthenticationError extends APIError {
    constructor(message: string) {
        super(message, 401);
        this.name = 'AuthenticationError';
    }
}

class RateLimitError extends APIError {
    constructor(message: string, public retryAfter: number = 60) {
        super(message, 429);
        this.name = 'RateLimitError';
    }
}

interface APIResponse {
    data: any;
}

class APIClient {
    constructor(private baseUrl: string, private apiKey: string) {}

    async getData(endpoint: string): Promise<APIResponse> {
        const url = `${this.baseUrl}/${endpoint}`;

        for (let attempt = 0; attempt < 3; attempt++) {
            try {
                const response = await fetch(url, {
                    headers: {
                        'Authorization': `Bearer ${this.apiKey}`,
                        'Content-Type': 'application/json'
                    },
                    signal: AbortSignal.timeout(30000)
                });

                return await this.handleResponse(response);
            } catch (error) {
                if (error instanceof Error) {
                    if (error.name === 'TimeoutError' || error.name === 'AbortError') {
                        if (attempt === 2) {
                            throw new APIError('Request timeout');
                        }
                        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
                    } else if (error.message.includes('fetch')) {
                        if (attempt === 2) {
                            throw new APIError('Connection failed');
                        }
                        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
                    } else {
                        throw error;
                    }
                }
            }
        }

        throw new APIError('Max retries exceeded');
    }

    private async handleResponse(response: Response): Promise<APIResponse> {
        if (response.ok) {
            return await response.json();
        } else if (response.status === 401) {
            throw new AuthenticationError('Invalid API key');
        } else if (response.status === 403) {
            throw new APIError('Access forbidden');
        } else if (response.status === 404) {
            throw new APIError('Resource not found');
        } else if (response.status === 429) {
            const retryAfter = parseInt(response.headers.get('Retry-After') || '60');
            throw new RateLimitError('Rate limit exceeded', retryAfter);
        } else {
            const text = await response.text();
            throw new APIError(`HTTP ${response.status}: ${text}`);
        }
    }
}

// Unit tests (Jest)
describe('APIClient', () => {
    let client: APIClient;

    beforeEach(() => {
        client = new APIClient('https://api.example.com', 'fake-key');
        global.fetch = jest.fn();
    });

    test('successful request', async () => {
        (global.fetch as jest.Mock).mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve({ data: 'test' })
        });

        const result = await client.getData('test');
        expect(result).toEqual({ data: 'test' });
    });

    test('authentication error', async () => {
        (global.fetch as jest.Mock).mockResolvedValueOnce({
            ok: false,
            status: 401,
            text: () => Promise.resolve('Unauthorized')
        });

        await expect(client.getData('test')).rejects.toThrow(AuthenticationError);
    });

    test('rate limit error', async () => {
        (global.fetch as jest.Mock).mockResolvedValueOnce({
            ok: false,
            status: 429,
            headers: new Map([['Retry-After', '120']]),
            text: () => Promise.resolve('Rate limit exceeded')
        });

        await expect(client.getData('test')).rejects.toThrow(RateLimitError);
    });
});
```

### Java Example
```java
public class APIError extends Exception {
    private final Integer statusCode;

    public APIError(String message) {
        super(message);
        this.statusCode = null;
    }

    public APIError(String message, Integer statusCode) {
        super(message);
        this.statusCode = statusCode;
    }

    public Integer getStatusCode() {
        return statusCode;
    }
}

public class AuthenticationError extends APIError {
    public AuthenticationError(String message) {
        super(message, 401);
    }
}

public class RateLimitError extends APIError {
    private final int retryAfter;

    public RateLimitError(String message, int retryAfter) {
        super(message, 429);
        this.retryAfter = retryAfter;
    }

    public int getRetryAfter() {
        return retryAfter;
    }
}

public class APIClient {
    private final String baseUrl;
    private final String apiKey;
    private final HttpClient httpClient;

    public APIClient(String baseUrl, String apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();
    }

    public Map<String, Object> getData(String endpoint) throws APIError {
        String url = baseUrl + "/" + endpoint;

        for (int attempt = 0; attempt < 3; attempt++) {
            try {
                HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Authorization", "Bearer " + apiKey)
                    .header("Content-Type", "application/json")
                    .timeout(Duration.ofSeconds(30))
                    .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                return handleResponse(response);
            } catch (IOException | InterruptedException e) {
                if (e instanceof HttpTimeoutException || e.getMessage().contains("timeout")) {
                    if (attempt == 2) {
                        throw new APIError("Request timeout");
                    }
                    try {
                        Thread.sleep((long) (Math.pow(2, attempt) * 1000));
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        throw new APIError("Interrupted during retry");
                    }
                } else {
                    if (attempt == 2) {
                        throw new APIError("Connection failed: " + e.getMessage());
                    }
                    try {
                        Thread.sleep((long) (Math.pow(2, attempt) * 1000));
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        throw new APIError("Interrupted during retry");
                    }
                }
            }
        }

        throw new APIError("Max retries exceeded");
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> handleResponse(HttpResponse<String> response) throws APIError {
        if (response.statusCode() == 200) {
            try {
                return new ObjectMapper().readValue(response.body(), Map.class);
            } catch (JsonProcessingException e) {
                throw new APIError("Invalid JSON response");
            }
        } else if (response.statusCode() == 401) {
            throw new AuthenticationError("Invalid API key");
        } else if (response.statusCode() == 403) {
            throw new APIError("Access forbidden");
        } else if (response.statusCode() == 404) {
            throw new APIError("Resource not found");
        } else if (response.statusCode() == 429) {
            int retryAfter = Integer.parseInt(response.headers()
                .firstValue("Retry-After").orElse("60"));
            throw new RateLimitError("Rate limit exceeded", retryAfter);
        } else {
            throw new APIError("HTTP " + response.statusCode() + ": " + response.body());
        }
    }
}

// Unit tests (JUnit 5 with Mockito)
@ExtendWith(MockitoExtension.class)
class APIClientTest {
    private APIClient client;

    @BeforeEach
    void setUp() {
        client = new APIClient("https://api.example.com", "fake-key");
    }

    @Test
    void testSuccessfulRequest() throws APIError {
        // Mock successful response
        // Implementation would use Mockito to mock HttpClient
    }

    @Test
    void testAuthenticationError() {
        // Mock 401 response
        APIError exception = assertThrows(AuthenticationError.class,
            () -> client.getData("test"));
        assertEquals(401, exception.getStatusCode());
    }

    @Test
    void testRateLimitError() {
        // Mock 429 response with Retry-After header
        RateLimitError exception = assertThrows(RateLimitError.class,
            () -> client.getData("test"));
        assertEquals(429, exception.getStatusCode());
        assertTrue(exception.getRetryAfter() > 0);
    }
}
```

### C# Example
```csharp
public class APIError : Exception
{
    public int? StatusCode { get; }

    public APIError(string message, int? statusCode = null) : base(message)
    {
        StatusCode = statusCode;
    }
}

public class AuthenticationError : APIError
{
    public AuthenticationError(string message) : base(message, 401) { }
}

public class RateLimitError : APIError
{
    public int RetryAfter { get; }

    public RateLimitError(string message, int retryAfter = 60) : base(message, 429)
    {
        RetryAfter = retryAfter;
    }
}

public class APIClient
{
    private readonly string _baseUrl;
    private readonly string _apiKey;
    private readonly HttpClient _httpClient;

    public APIClient(string baseUrl, string apiKey)
    {
        _baseUrl = baseUrl;
        _apiKey = apiKey;
        _httpClient = new HttpClient();
        _httpClient.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", apiKey);
        _httpClient.Timeout = TimeSpan.FromSeconds(30);
    }

    public async Task<Dictionary<string, object>> GetDataAsync(string endpoint)
    {
        string url = $"{_baseUrl}/{endpoint}";

        for (int attempt = 0; attempt < 3; attempt++)
        {
            try
            {
                var response = await _httpClient.GetAsync(url);
                return await HandleResponseAsync(response);
            }
            catch (TaskCanceledException)
            {
                if (attempt == 2)
                    throw new APIError("Request timeout");

                await Task.Delay((int)Math.Pow(2, attempt) * 1000);
            }
            catch (HttpRequestException)
            {
                if (attempt == 2)
                    throw new APIError("Connection failed");

                await Task.Delay((int)Math.Pow(2, attempt) * 1000);
            }
        }

        throw new APIError("Max retries exceeded");
    }

    private async Task<Dictionary<string, object>> HandleResponseAsync(HttpResponseMessage response)
    {
        if (response.IsSuccessStatusCode)
        {
            var content = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<Dictionary<string, object>>(content);
        }
        else if (response.StatusCode == HttpStatusCode.Unauthorized)
        {
            throw new AuthenticationError("Invalid API key");
        }
        else if (response.StatusCode == HttpStatusCode.Forbidden)
        {
            throw new APIError("Access forbidden");
        }
        else if (response.StatusCode == HttpStatusCode.NotFound)
        {
            throw new APIError("Resource not found");
        }
        else if (response.StatusCode == HttpStatusCode.TooManyRequests)
        {
            var retryAfter = int.Parse(response.Headers.RetryAfter?.ToString() ?? "60");
            throw new RateLimitError("Rate limit exceeded", retryAfter);
        }
        else
        {
            var content = await response.Content.ReadAsStringAsync();
            throw new APIError($"HTTP {(int)response.StatusCode}: {content}");
        }
    }
}

// Unit tests (xUnit with Moq)
public class APIClientTests
{
    private readonly APIClient _client;

    public APIClientTests()
    {
        _client = new APIClient("https://api.example.com", "fake-key");
    }

    [Fact]
    public async Task TestSuccessfulRequest()
    {
        // Arrange - mock HttpClient
        var mockHttpClient = new Mock<HttpClient>();
        // Setup mock response...

        // Act
        var result = await _client.GetDataAsync("test");

        // Assert
        Assert.NotNull(result);
    }

    [Fact]
    public async Task TestAuthenticationError()
    {
        // Arrange - mock 401 response
        var exception = await Assert.ThrowsAsync<AuthenticationError>(
            () => _client.GetDataAsync("test"));
        Assert.Equal(401, exception.StatusCode);
    }

    [Fact]
    public async Task TestRateLimitError()
    {
        // Arrange - mock 429 response
        var exception = await Assert.ThrowsAsync<RateLimitError>(
            () => _client.GetDataAsync("test"));
        Assert.Equal(429, exception.StatusCode);
        Assert.True(exception.RetryAfter > 0);
    }
}
```

**API Testing Checklist**:
- [ ] **HTTP Status Codes**: Handle all relevant status codes (200, 401, 403, 404, 429, 5xx)
- [ ] **Retry Logic**: Implement exponential backoff for transient failures
- [ ] **Timeout Handling**: Appropriate timeouts for different operations
- [ ] **Custom Exceptions**: Specific exception types for different error conditions
- [ ] **Rate Limiting**: Handle rate limit responses with retry-after headers
- [ ] **Connection Errors**: Handle network connectivity issues
- [ ] **Response Parsing**: Validate and parse API responses correctly

## 3. Data Processing Testing

**Scenario**: Developer needs to implement data processing logic that handles various data formats and edge cases.

**Test Steps**:
1. Open `.github/prompts/workflows/testing.md`
2. Follow the "Data Processing" section
3. Use Copilot to generate processing logic
4. Apply the testing patterns for comprehensive coverage

### Python Example
```python
from typing import List, Dict, Any, Optional
import json

class DataProcessingError(Exception):
    """Exception for data processing errors."""
    pass

class DataProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def process_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of items with validation and transformation."""
        if not items:
            return []

        processed = []
        for i, item in enumerate(items):
            try:
                processed_item = self._process_single_item(item, i)
                if processed_item is not None:
                    processed.append(processed_item)
            except DataProcessingError as e:
                if self.config.get('strict_mode', False):
                    raise
                # Log warning and continue in non-strict mode
                print(f"Warning: Skipping item {i}: {e}")
                continue

        return processed

    def _process_single_item(self, item: Dict[str, Any], index: int) -> Optional[Dict[str, Any]]:
        """Process a single item with validation."""
        if not isinstance(item, dict):
            raise DataProcessingError(f"Item {index} is not a dictionary")

        # Validate required fields
        required_fields = self.config.get('required_fields', [])
        for field in required_fields:
            if field not in item:
                raise DataProcessingError(f"Missing required field '{field}' in item {index}")

        # Transform data
        processed = item.copy()

        # Apply field transformations
        transformations = self.config.get('transformations', {})
        for field, transform_func in transformations.items():
            if field in processed:
                try:
                    processed[field] = transform_func(processed[field])
                except Exception as e:
                    raise DataProcessingError(f"Transformation failed for field '{field}' in item {index}: {e}")

        # Filter items if needed
        filter_func = self.config.get('filter')
        if filter_func and not filter_func(processed):
            return None

        return processed

# Unit tests
import unittest

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.config = {
            'required_fields': ['id', 'name'],
            'transformations': {
                'name': lambda x: x.upper(),
                'value': lambda x: float(x) if x is not None else 0.0
            },
            'filter': lambda x: x.get('active', True)
        }
        self.processor = DataProcessor(self.config)

    def test_process_empty_list(self):
        """Test processing empty list."""
        result = self.processor.process_items([])
        self.assertEqual(result, [])

    def test_process_valid_items(self):
        """Test processing valid items."""
        items = [
            {'id': 1, 'name': 'item1', 'value': '10.5', 'active': True},
            {'id': 2, 'name': 'item2', 'value': None, 'active': True}
        ]
        result = self.processor.process_items(items)

        expected = [
            {'id': 1, 'name': 'ITEM1', 'value': 10.5, 'active': True},
            {'id': 2, 'name': 'ITEM2', 'value': 0.0, 'active': True}
        ]
        self.assertEqual(result, expected)

    def test_missing_required_field(self):
        """Test handling missing required fields."""
        items = [{'id': 1, 'value': 10}]  # Missing 'name'

        with self.assertRaises(DataProcessingError):
            self.processor.process_items(items)

    def test_invalid_item_type(self):
        """Test handling invalid item types."""
        items = ["not a dict"]

        with self.assertRaises(DataProcessingError):
            self.processor.process_items(items)

    def test_transformation_error(self):
        """Test handling transformation errors."""
        items = [{'id': 1, 'name': 'test', 'value': 'invalid_number'}]

        with self.assertRaises(DataProcessingError):
            self.processor.process_items(items)

    def test_filtering(self):
        """Test item filtering."""
        items = [
            {'id': 1, 'name': 'active', 'active': True},
            {'id': 2, 'name': 'inactive', 'active': False}
        ]
        result = self.processor.process_items(items)

        # Should only include active items
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'ACTIVE')

    def test_non_strict_mode(self):
        """Test non-strict mode with invalid items."""
        config = self.config.copy()
        config['strict_mode'] = False
        processor = DataProcessor(config)

        items = [
            {'id': 1, 'name': 'valid'},
            {'id': 2, 'value': 10},  # Missing name
            {'id': 3, 'name': 'also_valid'}
        ]

        result = processor.process_items(items)
        # Should skip invalid item and process valid ones
        self.assertEqual(len(result), 2)
```

### JavaScript/TypeScript Example
```typescript
interface ProcessingConfig {
    requiredFields?: string[];
    transformations?: { [key: string]: (value: any) => any };
    filter?: (item: any) => boolean;
    strictMode?: boolean;
}

class DataProcessingError extends Error {
    constructor(message: string, public itemIndex?: number) {
        super(message);
        this.name = 'DataProcessingError';
    }
}

class DataProcessor {
    constructor(private config: ProcessingConfig) {}

    processItems(items: any[]): any[] {
        if (!items || items.length === 0) {
            return [];
        }

        const processed: any[] = [];

        for (let i = 0; i < items.length; i++) {
            try {
                const processedItem = this.processSingleItem(items[i], i);
                if (processedItem !== null) {
                    processed.push(processedItem);
                }
            } catch (error) {
                if (error instanceof DataProcessingError) {
                    if (this.config.strictMode) {
                        throw error;
                    }
                    console.warn(`Warning: Skipping item ${i}: ${error.message}`);
                    continue;
                }
                throw error;
            }
        }

        return processed;
    }

    private processSingleItem(item: any, index: number): any | null {
        if (typeof item !== 'object' || item === null) {
            throw new DataProcessingError(`Item ${index} is not an object`, index);
        }

        // Validate required fields
        const requiredFields = this.config.requiredFields || [];
        for (const field of requiredFields) {
            if (!(field in item)) {
                throw new DataProcessingError(`Missing required field '${field}' in item ${index}`, index);
            }
        }

        // Transform data
        const processed = { ...item };

        // Apply transformations
        const transformations = this.config.transformations || {};
        for (const [field, transformFunc] of Object.entries(transformations)) {
            if (field in processed) {
                try {
                    processed[field] = transformFunc(processed[field]);
                } catch (error) {
                    throw new DataProcessingError(
                        `Transformation failed for field '${field}' in item ${index}: ${error}`,
                        index
                    );
                }
            }
        }

        // Apply filter
        const filterFunc = this.config.filter;
        if (filterFunc && !filterFunc(processed)) {
            return null;
        }

        return processed;
    }
}

// Unit tests (Jest)
describe('DataProcessor', () => {
    let processor: DataProcessor;

    beforeEach(() => {
        processor = new DataProcessor({
            requiredFields: ['id', 'name'],
            transformations: {
                name: (x: string) => x.toUpperCase(),
                value: (x: any) => x !== null ? parseFloat(x) : 0.0
            },
            filter: (x: any) => x.active !== false
        });
    });

    test('process empty array', () => {
        const result = processor.processItems([]);
        expect(result).toEqual([]);
    });

    test('process valid items', () => {
        const items = [
            { id: 1, name: 'item1', value: '10.5', active: true },
            { id: 2, name: 'item2', value: null, active: true }
        ];
        const result = processor.processItems(items);

        expect(result).toEqual([
            { id: 1, name: 'ITEM1', value: 10.5, active: true },
            { id: 2, name: 'ITEM2', value: 0.0, active: true }
        ]);
    });

    test('missing required field', () => {
        const items = [{ id: 1, value: 10 }];

        expect(() => processor.processItems(items)).toThrow(DataProcessingError);
    });

    test('invalid item type', () => {
        const items = ['not an object'];

        expect(() => processor.processItems(items)).toThrow(DataProcessingError);
    });

    test('transformation error', () => {
        const items = [{ id: 1, name: 'test', value: 'invalid_number' }];

        expect(() => processor.processItems(items)).toThrow(DataProcessingError);
    });

    test('filtering', () => {
        const items = [
            { id: 1, name: 'active', active: true },
            { id: 2, name: 'inactive', active: false }
        ];
        const result = processor.processItems(items);

        expect(result).toHaveLength(1);
        expect(result[0].name).toBe('ACTIVE');
    });

    test('non-strict mode', () => {
        const nonStrictProcessor = new DataProcessor({
            ...processor['config'],
            strictMode: false
        });

        const items = [
            { id: 1, name: 'valid' },
            { id: 2, value: 10 }, // Missing name
            { id: 3, name: 'also_valid' }
        ];

        const result = nonStrictProcessor.processItems(items);
        expect(result).toHaveLength(2);
    });
});
```

### Java Example
```java
public class DataProcessingError extends Exception {
    private final Integer itemIndex;

    public DataProcessingError(String message) {
        super(message);
        this.itemIndex = null;
    }

    public DataProcessingError(String message, Integer itemIndex) {
        super(message);
        this.itemIndex = itemIndex;
    }

    public Integer getItemIndex() {
        return itemIndex;
    }
}

public class ProcessingConfig {
    private List<String> requiredFields = new ArrayList<>();
    private Map<String, Function<Object, Object>> transformations = new HashMap<>();
    private Predicate<Map<String, Object>> filter;
    private boolean strictMode = false;

    // Getters and setters...
}

public class DataProcessor {
    private final ProcessingConfig config;

    public DataProcessor(ProcessingConfig config) {
        this.config = config;
    }

    public List<Map<String, Object>> processItems(List<Map<String, Object>> items) {
        if (items == null || items.isEmpty()) {
            return new ArrayList<>();
        }

        List<Map<String, Object>> processed = new ArrayList<>();

        for (int i = 0; i < items.size(); i++) {
            try {
                Map<String, Object> processedItem = processSingleItem(items.get(i), i);
                if (processedItem != null) {
                    processed.add(processedItem);
                }
            } catch (DataProcessingError e) {
                if (config.isStrictMode()) {
                    throw new RuntimeException(e);
                }
                System.out.println("Warning: Skipping item " + i + ": " + e.getMessage());
                continue;
            }
        }

        return processed;
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> processSingleItem(Map<String, Object> item, int index) throws DataProcessingError {
        if (item == null) {
            throw new DataProcessingError("Item " + index + " is null", index);
        }

        // Validate required fields
        for (String field : config.getRequiredFields()) {
            if (!item.containsKey(field)) {
                throw new DataProcessingError("Missing required field '" + field + "' in item " + index, index);
            }
        }

        // Transform data
        Map<String, Object> processed = new HashMap<>(item);

        // Apply transformations
        for (Map.Entry<String, Function<Object, Object>> entry : config.getTransformations().entrySet()) {
            String field = entry.getKey();
            Function<Object, Object> transformFunc = entry.getValue();

            if (processed.containsKey(field)) {
                try {
                    processed.put(field, transformFunc.apply(processed.get(field)));
                } catch (Exception e) {
                    throw new DataProcessingError(
                        "Transformation failed for field '" + field + "' in item " + index + ": " + e.getMessage(),
                        index
                    );
                }
            }
        }

        // Apply filter
        if (config.getFilter() != null && !config.getFilter().test(processed)) {
            return null;
        }

        return processed;
    }
}

// Unit tests (JUnit 5)
class DataProcessorTest {
    private DataProcessor processor;
    private ProcessingConfig config;

    @BeforeEach
    void setUp() {
        config = new ProcessingConfig();
        config.setRequiredFields(Arrays.asList("id", "name"));
        config.setTransformations(Map.of(
            "name", (Object x) -> ((String) x).toUpperCase(),
            "value", (Object x) -> x != null ? Double.parseDouble(x.toString()) : 0.0
        ));
        config.setFilter(item -> !Boolean.FALSE.equals(item.get("active")));

        processor = new DataProcessor(config);
    }

    @Test
    void testProcessEmptyList() {
        List<Map<String, Object>> result = processor.processItems(new ArrayList<>());
        assertTrue(result.isEmpty());
    }

    @Test
    void testProcessValidItems() {
        List<Map<String, Object>> items = Arrays.asList(
            Map.of("id", 1, "name", "item1", "value", "10.5", "active", true),
            Map.of("id", 2, "name", "item2", "value", null, "active", true)
        );

        List<Map<String, Object>> result = processor.processItems(items);

        assertEquals(2, result.size());
        assertEquals("ITEM1", result.get(0).get("name"));
        assertEquals(10.5, result.get(0).get("value"));
        assertEquals("ITEM2", result.get(1).get("name"));
        assertEquals(0.0, result.get(1).get("value"));
    }

    @Test
    void testMissingRequiredField() {
        List<Map<String, Object>> items = List.of(Map.of("id", 1, "value", 10));

        assertThrows(RuntimeException.class, () -> processor.processItems(items));
    }

    @Test
    void testInvalidItemType() {
        List<Map<String, Object>> items = List.of("not a map");

        assertThrows(ClassCastException.class, () -> processor.processItems(items));
    }

    @Test
    void testFiltering() {
        List<Map<String, Object>> items = Arrays.asList(
            Map.of("id", 1, "name", "active", "active", true),
            Map.of("id", 2, "name", "inactive", "active", false)
        );

        List<Map<String, Object>> result = processor.processItems(items);

        assertEquals(1, result.size());
        assertEquals("ACTIVE", result.get(0).get("name"));
    }

    @Test
    void testNonStrictMode() {
        config.setStrictMode(false);
        DataProcessor nonStrictProcessor = new DataProcessor(config);

        List<Map<String, Object>> items = Arrays.asList(
            Map.of("id", 1, "name", "valid"),
            Map.of("id", 2, "value", 10), // Missing name
            Map.of("id", 3, "name", "also_valid")
        );

        List<Map<String, Object>> result = nonStrictProcessor.processItems(items);
        assertEquals(2, result.size());
    }
}
```

### C# Example
```csharp
public class DataProcessingError : Exception
{
    public int? ItemIndex { get; }

    public DataProcessingError(string message, int? itemIndex = null) : base(message)
    {
        ItemIndex = itemIndex;
    }
}

public class ProcessingConfig
{
    public List<string> RequiredFields { get; set; } = new();
    public Dictionary<string, Func<object, object>> Transformations { get; set; } = new();
    public Func<Dictionary<string, object>, bool>? Filter { get; set; }
    public bool StrictMode { get; set; } = false;
}

public class DataProcessor
{
    private readonly ProcessingConfig _config;

    public DataProcessor(ProcessingConfig config)
    {
        _config = config;
    }

    public List<Dictionary<string, object>> ProcessItems(List<Dictionary<string, object>> items)
    {
        if (items == null || items.Count == 0)
        {
            return new List<Dictionary<string, object>>();
        }

        var processed = new List<Dictionary<string, object>>();

        for (int i = 0; i < items.Count; i++)
        {
            try
            {
                var processedItem = ProcessSingleItem(items[i], i);
                if (processedItem != null)
                {
                    processed.Add(processedItem);
                }
            }
            catch (DataProcessingError e)
            {
                if (_config.StrictMode)
                {
                    throw;
                }
                Console.WriteLine($"Warning: Skipping item {i}: {e.Message}");
                continue;
            }
        }

        return processed;
    }

    private Dictionary<string, object>? ProcessSingleItem(Dictionary<string, object> item, int index)
    {
        if (item == null)
        {
            throw new DataProcessingError($"Item {index} is null", index);
        }

        // Validate required fields
        foreach (var field in _config.RequiredFields)
        {
            if (!item.ContainsKey(field))
            {
                throw new DataProcessingError($"Missing required field '{field}' in item {index}", index);
            }
        }

        // Transform data
        var processed = new Dictionary<string, object>(item);

        // Apply transformations
        foreach (var (field, transformFunc) in _config.Transformations)
        {
            if (processed.ContainsKey(field))
            {
                try
                {
                    processed[field] = transformFunc(processed[field]);
                }
                catch (Exception e)
                {
                    throw new DataProcessingError(
                        $"Transformation failed for field '{field}' in item {index}: {e.Message}",
                        index
                    );
                }
            }
        }

        // Apply filter
        if (_config.Filter != null && !_config.Filter(processed))
        {
            return null;
        }

        return processed;
    }
}

// Unit tests (xUnit)
public class DataProcessorTests
{
    private DataProcessor _processor;
    private ProcessingConfig _config;

    public DataProcessorTests()
    {
        _config = new ProcessingConfig
        {
            RequiredFields = new List<string> { "id", "name" },
            Transformations = new Dictionary<string, Func<object, object>>
            {
                ["name"] = x => ((string)x).ToUpper(),
                ["value"] = x => x != null ? Convert.ToDouble(x) : 0.0
            },
            Filter = x => x.GetValueOrDefault("active", true) as bool? ?? true
        };

        _processor = new DataProcessor(_config);
    }

    [Fact]
    public void TestProcessEmptyList()
    {
        var result = _processor.ProcessItems(new List<Dictionary<string, object>>());
        Assert.Empty(result);
    }

    [Fact]
    public void TestProcessValidItems()
    {
        var items = new List<Dictionary<string, object>>
        {
            new() { ["id"] = 1, ["name"] = "item1", ["value"] = "10.5", ["active"] = true },
            new() { ["id"] = 2, ["name"] = "item2", ["value"] = null, ["active"] = true }
        };

        var result = _processor.ProcessItems(items);

        Assert.Equal(2, result.Count);
        Assert.Equal("ITEM1", result[0]["name"]);
        Assert.Equal(10.5, result[0]["value"]);
        Assert.Equal("ITEM2", result[1]["name"]);
        Assert.Equal(0.0, result[1]["value"]);
    }

    [Fact]
    public void TestMissingRequiredField()
    {
        var items = new List<Dictionary<string, object>>
        {
            new() { ["id"] = 1, ["value"] = 10 }
        };

        Assert.Throws<DataProcessingError>(() => _processor.ProcessItems(items));
    }

    [Fact]
    public void TestInvalidItemType()
    {
        var items = new List<Dictionary<string, object>> { null };

        Assert.Throws<DataProcessingError>(() => _processor.ProcessItems(items));
    }

    [Fact]
    public void TestFiltering()
    {
        var items = new List<Dictionary<string, object>>
        {
            new() { ["id"] = 1, ["name"] = "active", ["active"] = true },
            new() { ["id"] = 2, ["name"] = "inactive", ["active"] = false }
        };

        var result = _processor.ProcessItems(items);

        Assert.Single(result);
        Assert.Equal("ACTIVE", result[0]["name"]);
    }

    [Fact]
    public void TestNonStrictMode()
    {
        _config.StrictMode = false;
        var nonStrictProcessor = new DataProcessor(_config);

        var items = new List<Dictionary<string, object>>
        {
            new() { ["id"] = 1, ["name"] = "valid" },
            new() { ["id"] = 2, ["value"] = 10 }, // Missing name
            new() { ["id"] = 3, ["name"] = "also_valid" }
        };

        var result = nonStrictProcessor.ProcessItems(items);
        Assert.Equal(2, result.Count);
    }
}
```

**Data Processing Testing Checklist**:
- [ ] **Input Validation**: Validate data types and required fields
- [ ] **Edge Cases**: Handle null values, empty collections, malformed data
- [ ] **Transformations**: Test data transformation functions
- [ ] **Filtering**: Verify filtering logic works correctly
- [ ] **Error Handling**: Test both strict and non-strict error modes
- [ ] **Performance**: Test with large datasets
- [ ] **Memory Management**: Ensure no memory leaks with large data sets

## Cross-Language Testing Patterns

### Framework-Agnostic Testing

**Common Testing Patterns**:
- **Arrange-Act-Assert**: Set up test data, execute code, verify results
- **Given-When-Then**: Define preconditions, actions, and expected outcomes
- **Equivalence Partitioning**: Test valid/invalid input ranges
- **Boundary Value Analysis**: Test edge cases at boundaries
- **Error Injection**: Test error conditions and recovery

### Multi-Language Test Organization

**Test Structure**:
```
tests/
├── unit/           # Unit tests
├── integration/   # Integration tests
├── e2e/          # End-to-end tests
├── fixtures/     # Test data
└── helpers/      # Test utilities
```

**Test Naming Conventions**:
- `test_function_name.py` (Python)
- `functionName.test.js` (JavaScript)
- `FunctionNameTests.java` (Java)
- `FunctionNameTests.cs` (C#)

### Continuous Integration Testing

**CI/CD Pipeline Testing**:
```yaml
# Generic CI configuration
test:
  stages:
    - test
    - integration
    - deploy

  jobs:
    unit-tests:
      script:
        - run_unit_tests()
      coverage: '/TOTAL.*\s+(\d+%)$/'

    integration-tests:
      script:
        - run_integration_tests()
      dependencies:
        - unit-tests

    e2e-tests:
      script:
        - run_e2e_tests()
      dependencies:
        - integration-tests
```

## Performance and Load Testing

### Performance Testing Scenarios

**Scenario**: Test application performance under various loads

**Test Implementation**:
- **Load Testing**: Simulate multiple concurrent users
- **Stress Testing**: Test system limits and breaking points
- **Spike Testing**: Test sudden load increases
- **Volume Testing**: Test with large data sets

### Memory and Resource Testing

**Scenario**: Ensure application doesn't have memory leaks or resource issues

**Test Focus**:
- Memory usage monitoring
- Garbage collection efficiency
- File handle management
- Database connection pooling
- Network connection handling

## Security Testing Scenarios

### Input Validation Security

**Scenario**: Test for common security vulnerabilities

**Security Test Cases**:
- SQL injection attempts
- Cross-site scripting (XSS)
- Command injection
- Path traversal attacks
- Buffer overflow attempts

### Authentication and Authorization Testing

**Scenario**: Verify security controls work properly

**Test Cases**:
- Invalid credentials
- Expired tokens
- Insufficient permissions
- Session management
- Secure data transmission

## Conclusion

These testing scenarios provide comprehensive coverage for multi-language development, ensuring that Copilot-generated code is:

- **Thoroughly Tested**: Unit tests, integration tests, and edge cases
- **Language-Agnostic**: Applicable to Python, JavaScript, Java, C#, and other languages
- **Framework-Neutral**: Work with various testing frameworks and tools
- **Security-Focused**: Include security testing scenarios
- **Performance-Aware**: Include performance and load testing
- **Maintainable**: Well-organized test structure and naming conventions

By following these testing scenarios, development teams can confidently use Copilot to accelerate development while maintaining high code quality and comprehensive test coverage across multiple programming languages.

        # Display results
        if not users:
            print(f"[INFO] No users found matching '{args.query}'")
            return

        print(f"Users matching '{args.query}' ({len(users)} total):")
        print("-" * 50)

        for user in users:
            print(f"-- {user['displayName']} ({user['mailAddress']})")
            print(f"   ID: {user['id']}")
            print()

    except AuthenticationError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"User search failed: {e}")
        print(f"[ERROR] Failed to search users: {e}")
        sys.exit(1)
```

**Validation Checklist**:
- [ ] Function follows CLI command pattern
- [ ] Proper error handling with specific exception types
- [ ] Input validation before API calls
- [ ] Clear user feedback with appropriate exit codes
- [ ] Verbose mode support for detailed output

### 2. Code Review Workflow Testing

**Scenario**: Developer has implemented a new pipeline status command and needs to prepare it for code review.

**Test Steps**:
1. Open `.github/prompts/workflows/code-review.md`
2. Follow the "PR Preparation" checklist
3. Use Copilot to generate the implementation
4. Apply the code review guidelines

**Sample Generated Code**:
```python
def cmd_pipeline_status(args: argparse.Namespace) -> None:
    """Show the status of a specific pipeline run."""
    client = AzureDevOpsClient(verbose=getattr(args, 'verbose', False))

    try:
        # Validate build ID
        if not args.build_id or not args.build_id.isdigit():
            print("[ERROR] Build ID must be a valid number")
            sys.exit(1)

        build_id = int(args.build_id)

        # Get build status
        build_info = client.get_build_status(build_id)

        # Display formatted output
        print(f"Build #{build_id}")
        print(f"Pipeline: {build_info['definition']['name']}")
        print(f"Status: {build_info['status']}")
        print(f"Result: {build_info.get('result', 'In Progress')}")
        print(f"Branch: {build_info.get('sourceBranch', 'N/A')}")

        # Show timing information
        if build_info.get('startTime'):
            start_time = datetime.fromisoformat(build_info['startTime'].replace('Z', '+00:00'))
            print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        if build_info.get('finishTime'):
            finish_time = datetime.fromisoformat(build_info['finishTime'].replace('Z', '+00:00'))
            duration = finish_time - start_time
            print(f"Duration: {duration}")
            print(f"Finished: {finish_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        # Show verbose details if requested
        if getattr(args, 'verbose', False):
            print("\nFull API Response:")
            print(json.dumps(build_info, indent=2, default=str))

    except ResourceNotFoundError:
        print(f"[ERROR] Build {args.build_id} not found")
        sys.exit(1)
    except AuthenticationError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to get pipeline status: {e}")
        print(f"[ERROR] Failed to get pipeline status: {e}")
        sys.exit(1)
```

**Code Review Checklist Application**:
- [ ] **Functionality**: Command works with valid and invalid build IDs
- [ ] **Error Handling**: Proper exception handling for all error cases
- [ ] **Input Validation**: Build ID validation before API calls
- [ ] **User Experience**: Clear output formatting and error messages
- [ ] **Documentation**: Comprehensive docstring with examples
- [ ] **Type Hints**: All parameters and return values typed
- [ ] **Logging**: Appropriate error logging with context
- [ ] **Testing**: Unit tests cover success and error cases

### 3. Testing Workflow Testing

**Scenario**: Developer needs to add comprehensive tests for a new repository deletion feature.

**Test Steps**:
1. Open `.github/prompts/workflows/testing.md`
2. Follow the "Unit Testing" section
3. Use Copilot to generate test cases
4. Apply the testing patterns and validation steps

**Generated Test Examples**:
```python
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from saz_package.client import AzureDevOpsClient, AuthenticationError, PermissionError
from saz_package.repositories import cmd_repo_delete


class TestRepositoryDeletion(unittest.TestCase):
    """Test cases for repository deletion functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = AzureDevOpsClient(
            organization="test-org",
            project="test-project",
            pat="fake-pat"
        )

    def test_delete_repository_success(self):
        """Test successful repository deletion."""
        with patch.object(self.client.session, 'delete') as mock_delete:
            mock_response = MagicMock()
            mock_response.status_code = 204
            mock_delete.return_value = mock_response

            # Should not raise exception
            self.client.delete_repository("test-repo")

            # Verify correct API call
            mock_delete.assert_called_once_with(
                "https://dev.azure.com/test-org/test-project/_apis/git/repositories/test-repo",
                params={'api-version': '7.1'}
            )

    def test_delete_repository_not_found(self):
        """Test deletion of non-existent repository."""
        with patch.object(self.client.session, 'delete') as mock_delete:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
            mock_delete.return_value = mock_response

            with self.assertRaises(ResourceNotFoundError):
                self.client.delete_repository("nonexistent-repo")

    def test_delete_repository_access_denied(self):
        """Test deletion with insufficient permissions."""
        with patch.object(self.client.session, 'delete') as mock_delete:
            mock_response = MagicMock()
            mock_response.status_code = 403
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
            mock_delete.return_value = mock_response

            with self.assertRaises(PermissionError):
                self.client.delete_repository("protected-repo")

    @patch('saz_package.repositories.AzureDevOpsClient')
    def test_cmd_repo_delete_success(self, mock_client_class):
        """Test CLI command for successful repository deletion."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        # Mock successful deletion (no exception)
        mock_client.delete_repository.return_value = None

        # Test command execution
        import argparse
        args = argparse.Namespace(repo_name="test-repo", verbose=False, force=False)

        # Should not raise exception
        cmd_repo_delete(args)

        # Verify client was called correctly
        mock_client.delete_repository.assert_called_once_with("test-repo")

    @patch('saz_package.repositories.AzureDevOpsClient')
    def test_cmd_repo_delete_not_found(self, mock_client_class):
        """Test CLI command when repository doesn't exist."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        # Mock repository not found
        mock_client.delete_repository.side_effect = ResourceNotFoundError("Repository not found")

        args = argparse.Namespace(repo_name="missing-repo", verbose=False, force=False)

        # Should exit with code 1
        with self.assertRaises(SystemExit) as cm:
            cmd_repo_delete(args)

        self.assertEqual(cm.exception.code, 1)
```

**Testing Validation**:
- [ ] **Unit Tests**: Cover success and error cases
- [ ] **Mocking**: Proper use of unittest.mock for external dependencies
- [ ] **CLI Tests**: Test command-line interface behavior
- [ ] **Error Cases**: Test all exception paths
- [ ] **Edge Cases**: Test boundary conditions and invalid inputs
- [ ] **Integration**: Test with real Azure DevOps (when PAT available)

## Cross-Platform Testing Scenarios

### Windows Compatibility Testing

**Scenario**: Test CLI commands on Windows PowerShell

**Test Commands**:
```powershell
# Test repository listing
python -m saz_package.cli repo list

# Test with verbose output
python -m saz_package.cli repo show --verbose

# Test error handling
python -m saz_package.cli repo show nonexistent-repo
```

**Expected Behavior**:
- Commands execute without path-related errors
- Unicode characters display correctly
- Error messages are clear and actionable
- Exit codes are appropriate (0 for success, 1 for errors)

### CI/CD Integration Testing

**Scenario**: Validate prompts work in automated environments

**Test Setup**:
```yaml
# .github/workflows/test-prompts.yml
name: Test Copilot Prompts
on: [push, pull_request]

jobs:
  test-prompts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest
      - name: Validate CLI
        run: python -m saz_package.cli --help
```

## Performance Testing Scenarios

### API Call Efficiency

**Scenario**: Test that generated code handles API rate limits appropriately

**Test Code**:
```python
import time
from unittest.mock import patch

def test_api_rate_limiting(self):
    """Test that client handles rate limiting gracefully."""
    with patch.object(self.client.session, 'get') as mock_get:
        # Mock rate limit response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '60'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        mock_get.return_value = mock_response

        start_time = time.time()
        with self.assertRaises(AzureDevOpsError) as cm:
            self.client.get_repository("test-repo")

        # Should include rate limit message
        self.assertIn("Rate limit", str(cm.exception))

        # Should not retry immediately (would be too fast)
        elapsed = time.time() - start_time
        self.assertGreater(elapsed, 0.1)  # At least some delay
```

## Documentation Testing

### README Validation

**Scenario**: Ensure generated code examples in README are accurate

**Test Process**:
1. Copy code examples from README
2. Execute them in test environment
3. Verify they produce expected output
4. Update examples if they become outdated

### Help System Testing

**Scenario**: Validate that `--help` output matches documented commands

**Test Commands**:
```bash
# Get help output
python -m saz_package.cli --help > help_output.txt

# Compare with documented examples
diff help_output.txt docs/cli-help-expected.txt
```

## Integration Testing Scenarios

### End-to-End Workflow Testing

**Scenario**: Complete feature development using all workflow prompts

**Test Workflow**:
1. **PBI Creation**: Use pbi-creation.md to plan feature
2. **Implementation**: Use code-patterns.md for implementation guidance
3. **Testing**: Use testing.md to create comprehensive tests
4. **Code Review**: Use code-review.md for PR preparation
5. **Documentation**: Update README and examples

**Success Metrics**:
- [ ] Feature works end-to-end
- [ ] All tests pass
- [ ] Code review passes
- [ ] Documentation is accurate
- [ ] No breaking changes introduced

## Automated Testing Integration

### Test Coverage Validation

**Scenario**: Ensure prompts lead to well-tested code

**Coverage Requirements**:
```python
# Minimum coverage thresholds
MIN_COVERAGE = 80

def test_coverage_validation(self):
    """Test that new code meets coverage requirements."""
    import coverage

    cov = coverage.Coverage()
    cov.start()

    # Run test suite
    import subprocess
    result = subprocess.run(['python', '-m', 'pytest'], capture_output=True, text=True)

    cov.stop()
    cov.save()

    # Check coverage
    percentage = cov.report()
    self.assertGreaterEqual(percentage, MIN_COVERAGE,
                          f"Test coverage {percentage}% is below minimum {MIN_COVERAGE}%")
```

## Continuous Improvement

### Feedback Collection

**After Each Test Scenario**:
1. **Record Results**: Document what worked and what didn't
2. **Identify Patterns**: Note common issues or improvements
3. **Update Prompts**: Refine prompts based on testing feedback
4. **Share Learnings**: Update team documentation with findings

### Metrics Tracking

**Track These Metrics**:
- Time to implement features using prompts
- Bug rates in Copilot-generated vs manual code
- Code review feedback and common issues
- Test coverage and quality metrics
- Developer satisfaction and productivity

### Prompt Evolution

**Regular Review Process**:
- Monthly review of prompt effectiveness
- Update prompts based on new patterns and best practices
- Incorporate feedback from development team
- Test new prompt versions before deployment

## Conclusion

These testing scenarios ensure that the Copilot prompts in the SAZ repository are:

- **Clear and actionable** for developers
- **Comprehensive** in covering error cases and edge conditions
- **Consistent** with project standards and conventions
- **Effective** in accelerating development while maintaining quality
- **Well-tested** through systematic validation procedures

By following these testing scenarios, we can confidently use Copilot to accelerate development while maintaining the high code quality standards of the SAZ project.