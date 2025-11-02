# Code Patterns and Best Practices

This directory contains examples of preferred code patterns, architectural decisions, and implementation best practices for different programming languages and frameworks. These patterns are designed to be adaptable across projects while following language-specific conventions.

## Python Code Patterns

### 1. HTTP API Client Pattern
```python
# Preferred pattern for REST API calls
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = timeout

        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})

        # Configure retry strategy
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"GET {url}")

        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
```

### 2. CLI Command Handler Pattern
```python
import argparse
import sys
from typing import NoReturn

def handle_command_error(func):
    """Decorator to handle command execution errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(130)
        except Exception as e:
            logger.error(f"Command failed: {e}")
            print(f"Error: {e}")
            sys.exit(1)
    return wrapper

@handle_command_error
def cmd_list_items(args: argparse.Namespace) -> None:
    """List items from the API."""
    client = ApiClient(base_url=args.api_url, api_key=args.api_key)

    try:
        items = client.get("items")
        if not items:
            print("No items found.")
            return

        print(f"Found {len(items)} items:")
        for item in items:
            print(f"  - {item['name']} (ID: {item['id']})")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch items: {e}")
```

### 3. Configuration Management Pattern
```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class AppConfig:
    api_url: str
    api_key: Optional[str] = None
    verbose: bool = False
    timeout: int = 30

    @classmethod
    def from_environment(cls) -> 'AppConfig':
        """Load configuration from environment variables."""
        return cls(
            api_url=os.getenv('API_URL', 'https://api.example.com'),
            api_key=os.getenv('API_KEY'),
            verbose=os.getenv('VERBOSE', 'false').lower() == 'true',
            timeout=int(os.getenv('TIMEOUT', '30'))
        )

    @classmethod
    def from_file(cls, config_file: str) -> 'AppConfig':
        """Load configuration from YAML file."""
        import yaml
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)
```

## JavaScript/TypeScript Code Patterns

### 1. API Client Pattern
```typescript
// TypeScript API client with proper error handling
interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

class ApiClient {
  private baseUrl: string;
  private apiKey?: string;
  private timeout: number;

  constructor(baseUrl: string, apiKey?: string, timeout: number = 30000) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.timeout = timeout;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}/${endpoint.replace(/^\//, '')}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
      signal: AbortSignal.timeout(this.timeout),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async get<T>(endpoint: string, params?: Record<string, string>): Promise<T> {
    const url = params ? `${endpoint}?${new URLSearchParams(params)}` : endpoint;
    return this.request<T>(url);
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}
```

### 2. CLI Command Handler Pattern
```typescript
import { Command } from 'commander';
import { ApiClient } from './api-client.js';

interface CliOptions {
  apiUrl: string;
  apiKey?: string;
  verbose: boolean;
}

async function listItems(options: CliOptions): Promise<void> {
  const client = new ApiClient(options.apiUrl, options.apiKey);

  try {
    const items = await client.get<any[]>('items');

    if (items.length === 0) {
      console.log('No items found.');
      return;
    }

    console.log(`Found ${items.length} items:`);
    items.forEach(item => {
      console.log(`  - ${item.name} (ID: ${item.id})`);
    });
  } catch (error) {
    console.error(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    process.exit(1);
  }
}

// Commander.js setup
const program = new Command();

program
  .name('mycli')
  .description('CLI tool for managing items')
  .version('1.0.0');

program
  .command('list')
  .description('List all items')
  .option('--api-url <url>', 'API base URL', 'https://api.example.com')
  .option('--api-key <key>', 'API key')
  .option('--verbose', 'Enable verbose output')
  .action(async (options) => {
    await listItems(options);
  });

program.parse();
```

### 3. Configuration Management Pattern
```typescript
// TypeScript configuration with validation
import { z } from 'zod';
import * as fs from 'fs';
import * as path from 'path';

const configSchema = z.object({
  apiUrl: z.string().url(),
  apiKey: z.string().optional(),
  verbose: z.boolean().default(false),
  timeout: z.number().min(1000).max(300000).default(30000),
});

type AppConfig = z.infer<typeof configSchema>;

class ConfigManager {
  static fromEnvironment(): AppConfig {
    return configSchema.parse({
      apiUrl: process.env.API_URL || 'https://api.example.com',
      apiKey: process.env.API_KEY,
      verbose: process.env.VERBOSE === 'true',
      timeout: parseInt(process.env.TIMEOUT || '30000', 10),
    });
  }

  static fromFile(configPath: string): AppConfig {
    const fullPath = path.resolve(configPath);
    const configData = JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
    return configSchema.parse(configData);
  }
}
```

## Java Code Patterns

### 1. HTTP API Client Pattern
```java
import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.time.Duration;
import java.util.Map;
import java.util.Optional;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ApiClient {
    private static final Logger logger = LoggerFactory.getLogger(ApiClient.class);

    private final HttpClient httpClient;
    private final String baseUrl;
    private final Optional<String> apiKey;
    private final ObjectMapper objectMapper;

    public ApiClient(String baseUrl, Optional<String> apiKey) {
        this.baseUrl = baseUrl.replaceAll("/$", "");
        this.apiKey = apiKey;
        this.objectMapper = new ObjectMapper();

        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();
    }

    public <T> T get(String endpoint, Class<T> responseType) throws IOException, InterruptedException {
        String url = baseUrl + "/" + endpoint.replaceAll("^/", "");
        logger.debug("GET {}", url);

        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .timeout(Duration.ofSeconds(30))
            .GET();

        if (apiKey.isPresent()) {
            requestBuilder.header("Authorization", "Bearer " + apiKey.get());
        }

        HttpRequest request = requestBuilder.build();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() >= 400) {
            throw new RuntimeException("HTTP " + response.statusCode() + ": " + response.body());
        }

        return objectMapper.readValue(response.body(), responseType);
    }
}
```

### 2. CLI Command Handler Pattern
```java
import picocli.CommandLine;
import java.util.concurrent.Callable;

@CommandLine.Command(name = "mycli", description = "CLI tool for managing items")
public class CliApplication implements Callable<Integer> {

    @CommandLine.Option(names = {"--api-url"}, description = "API base URL", defaultValue = "https://api.example.com")
    private String apiUrl;

    @CommandLine.Option(names = {"--api-key"}, description = "API key")
    private String apiKey;

    @CommandLine.Option(names = {"--verbose"}, description = "Enable verbose output")
    private boolean verbose;

    @Override
    public Integer call() throws Exception {
        // Main application logic
        return 0;
    }

    @CommandLine.Command(name = "list", description = "List all items")
    public static class ListCommand implements Callable<Integer> {

        @CommandLine.ParentCommand
        private CliApplication parent;

        @Override
        public Integer call() throws Exception {
            ApiClient client = new ApiClient(parent.apiUrl,
                Optional.ofNullable(parent.apiKey));

            try {
                Item[] items = client.get("items", Item[].class);

                if (items.length == 0) {
                    System.out.println("No items found.");
                    return 0;
                }

                System.out.println("Found " + items.length + " items:");
                for (Item item : items) {
                    System.out.println("  - " + item.getName() + " (ID: " + item.getId() + ")");
                }

                return 0;
            } catch (Exception e) {
                System.err.println("Error: " + e.getMessage());
                return 1;
            }
        }
    }

    public static void main(String[] args) {
        int exitCode = new CommandLine(new CliApplication())
            .addSubcommand("list", new ListCommand())
            .execute(args);
        System.exit(exitCode);
    }
}
```

### 3. Configuration Management Pattern
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.annotation.JsonProperty;

public class AppConfig {
    private final String apiUrl;
    private final Optional<String> apiKey;
    private final boolean verbose;
    private final int timeout;

    public AppConfig(
            @JsonProperty("apiUrl") String apiUrl,
            @JsonProperty("apiKey") Optional<String> apiKey,
            @JsonProperty("verbose") boolean verbose,
            @JsonProperty("timeout") int timeout) {
        this.apiUrl = apiUrl;
        this.apiKey = apiKey;
        this.verbose = verbose;
        this.timeout = timeout;
    }

    public static AppConfig fromEnvironment() {
        return new AppConfig(
            Optional.ofNullable(System.getenv("API_URL")).orElse("https://api.example.com"),
            Optional.ofNullable(System.getenv("API_KEY")),
            Boolean.parseBoolean(System.getenv("VERBOSE")),
            Integer.parseInt(System.getenv().getOrDefault("TIMEOUT", "30000"))
        );
    }

    public static AppConfig fromFile(String configPath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        String content = Files.readString(Path.of(configPath));
        return mapper.readValue(content, AppConfig.class);
    }

    // Getters...
    public String getApiUrl() { return apiUrl; }
    public Optional<String> getApiKey() { return apiKey; }
    public boolean isVerbose() { return verbose; }
    public int getTimeout() { return timeout; }
}
```

## C# Code Patterns

### 1. HTTP API Client Pattern
```csharp
using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

public class ApiClient : IDisposable
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ApiClient> _logger;
    private readonly string _apiKey;
    private bool _disposed;

    public ApiClient(string baseUrl, string apiKey = null, ILogger<ApiClient> logger = null)
    {
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri(baseUrl.TrimEnd('/')),
            Timeout = TimeSpan.FromSeconds(30)
        };

        _apiKey = apiKey;
        _logger = logger ?? LoggerFactory.Create(builder => builder.AddConsole()).CreateLogger<ApiClient>();

        if (!string.IsNullOrEmpty(_apiKey))
        {
            _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_apiKey}");
        }
    }

    public async Task<T> GetAsync<T>(string endpoint)
    {
        _logger.LogDebug("GET {BaseAddress}{endpoint}", _httpClient.BaseAddress, endpoint);

        var response = await _httpClient.GetAsync(endpoint);
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<T>();
    }

    public async Task<T> PostAsync<T>(string endpoint, object data)
    {
        var json = JsonSerializer.Serialize(data);
        var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");

        var response = await _httpClient.PostAsync(endpoint, content);
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<T>();
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed)
        {
            if (disposing)
            {
                _httpClient?.Dispose();
            }
            _disposed = true;
        }
    }
}
```

### 2. CLI Command Handler Pattern
```csharp
using System.CommandLine;
using System.CommandLine.Invocation;
using Microsoft.Extensions.Logging;

public class Program
{
    public static async Task<int> Main(string[] args)
    {
        var loggerFactory = LoggerFactory.Create(builder => builder.AddConsole());
        var logger = loggerFactory.CreateLogger<Program>();

        var rootCommand = new RootCommand("CLI tool for managing items");

        var apiUrlOption = new Option<string>(
            "--api-url",
            getDefaultValue: () => "https://api.example.com",
            description: "API base URL");

        var apiKeyOption = new Option<string>(
            "--api-key",
            description: "API key");

        var verboseOption = new Option<bool>(
            "--verbose",
            description: "Enable verbose output");

        rootCommand.AddGlobalOption(apiUrlOption);
        rootCommand.AddGlobalOption(apiKeyOption);
        rootCommand.AddGlobalOption(verboseOption);

        var listCommand = new Command("list", "List all items");
        listCommand.SetHandler(async (string apiUrl, string apiKey, bool verbose) =>
        {
            try
            {
                using var client = new ApiClient(apiUrl, apiKey, logger);

                var items = await client.GetAsync<Item[]>("items");

                if (items.Length == 0)
                {
                    Console.WriteLine("No items found.");
                    return;
                }

                Console.WriteLine($"Found {items.Length} items:");
                foreach (var item in items)
                {
                    Console.WriteLine($"  - {item.Name} (ID: {item.Id})");
                }
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Failed to list items");
                Console.Error.WriteLine($"Error: {ex.Message}");
                Environment.Exit(1);
            }
        }, apiUrlOption, apiKeyOption, verboseOption);

        rootCommand.AddCommand(listCommand);

        return await rootCommand.InvokeAsync(args);
    }
}

public record Item(string Id, string Name);
```

### 3. Configuration Management Pattern
```csharp
using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Configuration;

public class AppConfig
{
    public string ApiUrl { get; set; } = "https://api.example.com";
    public string? ApiKey { get; set; }
    public bool Verbose { get; set; }
    public int Timeout { get; set; } = 30000;

    public static AppConfig FromEnvironment()
    {
        return new AppConfig
        {
            ApiUrl = Environment.GetEnvironmentVariable("API_URL") ?? "https://api.example.com",
            ApiKey = Environment.GetEnvironmentVariable("API_KEY"),
            Verbose = Environment.GetEnvironmentVariable("VERBOSE")?.ToLower() == "true",
            Timeout = int.Parse(Environment.GetEnvironmentVariable("TIMEOUT") ?? "30000")
        };
    }

    public static AppConfig FromFile(string configPath)
    {
        var json = File.ReadAllText(configPath);
        var config = JsonSerializer.Deserialize<AppConfig>(json, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        });

        return config ?? throw new InvalidOperationException("Invalid configuration file");
    }

    public static AppConfig FromConfiguration(IConfiguration configuration)
    {
        return new AppConfig
        {
            ApiUrl = configuration["ApiUrl"] ?? "https://api.example.com",
            ApiKey = configuration["ApiKey"],
            Verbose = bool.Parse(configuration["Verbose"] ?? "false"),
            Timeout = int.Parse(configuration["Timeout"] ?? "30000")
        };
    }
}
```

## Cross-Language Patterns

### Error Handling Patterns

#### Python
```python
class AppError(Exception):
    """Base application error."""
    pass

class ApiError(AppError):
    """API-related errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

def handle_api_errors(func):
    """Decorator for consistent API error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            raise ApiError("Network connection failed")
        except requests.exceptions.Timeout:
            raise ApiError("Request timed out")
        except requests.exceptions.HTTPError as e:
            raise ApiError(f"HTTP {e.response.status_code}: {e.response.reason}", e.response.status_code)
    return wrapper
```

#### JavaScript/TypeScript
```typescript
class AppError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'AppError';
  }
}

class ApiError extends AppError {
  constructor(message: string, public statusCode?: number) {
    super(message, 'API_ERROR');
    this.statusCode = statusCode;
  }
}

async function withApiErrorHandling<T>(operation: () => Promise<T>): Promise<T> {
  try {
    return await operation();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError('Network connection failed');
    }

    throw new AppError(error instanceof Error ? error.message : 'Unknown error');
  }
}
```

#### Java
```java
public class AppException extends Exception {
    public AppException(String message) {
        super(message);
    }

    public AppException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class ApiException extends AppException {
    private final int statusCode;

    public ApiException(String message, int statusCode) {
        super(message);
        this.statusCode = statusCode;
    }

    public int getStatusCode() {
        return statusCode;
    }
}

public static <T> T withApiErrorHandling(Supplier<T> operation) throws AppException {
    try {
        return operation.get();
    } catch (IOException e) {
        if (e.getMessage().contains("Connection refused")) {
            throw new ApiException("Network connection failed", 0);
        }
        throw new AppException("I/O error: " + e.getMessage(), e);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        throw new AppException("Operation was interrupted", e);
    }
}
```

#### C#
```csharp
public class AppException : Exception
{
    public AppException(string message) : base(message) { }
    public AppException(string message, Exception innerException)
        : base(message, innerException) { }
}

public class ApiException : AppException
{
    public int? StatusCode { get; }

    public ApiException(string message, int? statusCode = null)
        : base(message)
    {
        StatusCode = statusCode;
    }
}

public static async Task<T> WithApiErrorHandling<T>(Func<Task<T>> operation)
{
    try
    {
        return await operation();
    }
    catch (HttpRequestException ex) when (ex.StatusCode.HasValue)
    {
        throw new ApiException($"HTTP {(int)ex.StatusCode}: {ex.Message}", (int)ex.StatusCode);
    }
    catch (TaskCanceledException ex) when (!ex.CancellationToken.IsCancellationRequested)
    {
        throw new ApiException("Request timed out");
    }
    catch (Exception ex)
    {
        throw new AppException($"Unexpected error: {ex.Message}", ex);
    }
}
```

### Testing Patterns

#### Unit Test Structure (Python)
```python
import pytest
from unittest.mock import Mock, patch
from myapp.api_client import ApiClient, ApiError

class TestApiClient:
    @pytest.fixture
    def client(self):
        return ApiClient("https://api.example.com", "test-key")

    @patch('myapp.api_client.requests.get')
    def test_get_success(self, mock_get, client):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = client.get("test")
        assert result == {"data": "test"}

    @patch('myapp.api_client.requests.get')
    def test_get_http_error(self, mock_get, client):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("Not found")
        mock_get.return_value = mock_response

        with pytest.raises(ApiError):
            client.get("nonexistent")
```

#### Unit Test Structure (JavaScript/TypeScript)
```typescript
import { describe, it, expect, jest, beforeEach } from '@jest/globals';
import { ApiClient, ApiError } from '../src/api-client.js';

describe('ApiClient', () => {
  let client: ApiClient;

  beforeEach(() => {
    client = new ApiClient('https://api.example.com', 'test-key');
  });

  it('should get data successfully', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ data: 'test' }),
      } as Response)
    );

    const result = await client.get('test');
    expect(result).toEqual({ data: 'test' });
  });

  it('should handle HTTP errors', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        status: 404,
        statusText: 'Not Found',
      } as Response)
    );

    await expect(client.get('nonexistent')).rejects.toThrow(ApiError);
  });
});
```

### Logging Patterns

#### Python
```python
import logging

logger = logging.getLogger(__name__)

def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def api_call_with_logging(endpoint: str):
    logger.debug(f"Calling API endpoint: {endpoint}")
    try:
        result = make_api_call(endpoint)
        logger.info(f"Successfully called {endpoint}")
        return result
    except Exception as e:
        logger.error(f"Failed to call {endpoint}: {e}")
        raise
```

#### JavaScript/TypeScript
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) =>
      `${timestamp} [${level.toUpperCase()}]: ${message}`
    )
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log' })
  ]
});

async function apiCallWithLogging(endpoint: string): Promise<any> {
  logger.debug(`Calling API endpoint: ${endpoint}`);
  try {
    const result = await makeApiCall(endpoint);
    logger.info(`Successfully called ${endpoint}`);
    return result;
  } catch (error) {
    logger.error(`Failed to call ${endpoint}: ${error}`);
    throw error;
  }
}
```

### Documentation Patterns

#### Python (Google Style)
```python
def create_item(name: str, description: str = "", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a new item in the system.

    Args:
        name: The name of the item to create (required)
        description: Optional description of the item
        metadata: Additional metadata as key-value pairs

    Returns:
        Dictionary containing the created item information including ID

    Raises:
        ApiError: If the item creation fails due to API errors
        ValidationError: If the input parameters are invalid

    Example:
        >>> create_item("my-item", "A sample item")
        {'id': '123', 'name': 'my-item', 'description': 'A sample item'}
    """
```

#### JavaScript/TypeScript (JSDoc)
```typescript
/**
 * Create a new item in the system.
 *
 * @param {string} name - The name of the item to create (required)
 * @param {string} [description=""] - Optional description of the item
 * @param {Object.<string, any>} [metadata] - Additional metadata as key-value pairs
 * @returns {Promise<Object>} Promise resolving to the created item information
 * @throws {ApiError} If the item creation fails due to API errors
 * @throws {ValidationError} If the input parameters are invalid
 *
 * @example
 * const item = await createItem("my-item", "A sample item");
 * console.log(item.id); // "123"
 */
async function createItem(
  name: string,
  description: string = "",
  metadata?: Record<string, any>
): Promise<any> {
  // Implementation...
}
```