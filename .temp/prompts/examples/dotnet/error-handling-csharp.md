# Error Handling Patterns in C#

This guide covers comprehensive error handling patterns for .NET applications, including custom exceptions, retry mechanisms, circuit breaker patterns, and best practices for robust error management.

## Custom Exception Hierarchy

### Base Exception Classes

```csharp
// Domain/Exceptions/DomainException.cs
using System;

namespace Domain.Exceptions
{
    /// <summary>
    /// Base exception for all domain-related errors
    /// </summary>
    public abstract class DomainException : Exception
    {
        public string ErrorCode { get; }
        public object[] Parameters { get; }

        protected DomainException(string errorCode, string message, params object[] parameters)
            : base(message)
        {
            ErrorCode = errorCode;
            Parameters = parameters;
        }

        protected DomainException(string errorCode, string message, Exception innerException, params object[] parameters)
            : base(message, innerException)
        {
            ErrorCode = errorCode;
            Parameters = parameters;
        }
    }

    /// <summary>
    /// Exception for business rule violations
    /// </summary>
    public class BusinessRuleException : DomainException
    {
        public BusinessRuleException(string ruleName, string message)
            : base("BUSINESS_RULE_VIOLATION", $"Business rule '{ruleName}' violated: {message}")
        {
        }
    }

    /// <summary>
    /// Exception for entity not found scenarios
    /// </summary>
    public class EntityNotFoundException : DomainException
    {
        public EntityNotFoundException(string entityType, object entityId)
            : base("ENTITY_NOT_FOUND", $"{entityType} with ID '{entityId}' was not found")
        {
        }
    }

    /// <summary>
    /// Exception for validation errors
    /// </summary>
    public class ValidationException : DomainException
    {
        public ValidationException(string fieldName, string validationMessage)
            : base("VALIDATION_ERROR", $"Validation failed for field '{fieldName}': {validationMessage}")
        {
        }

        public ValidationException(string message)
            : base("VALIDATION_ERROR", message)
        {
        }
    }

    /// <summary>
    /// Exception for concurrency conflicts
    /// </summary>
    public class ConcurrencyException : DomainException
    {
        public ConcurrencyException(string entityType, object entityId)
            : base("CONCURRENCY_CONFLICT", $"Concurrency conflict occurred for {entityType} with ID '{entityId}'")
        {
        }
    }
}

// Application/Exceptions/ApplicationException.cs
using System;

namespace Application.Exceptions
{
    /// <summary>
    /// Base exception for all application layer errors
    /// </summary>
    public abstract class ApplicationException : Exception
    {
        public string ErrorCode { get; }
        public object[] Parameters { get; }

        protected ApplicationException(string errorCode, string message, params object[] parameters)
            : base(message)
        {
            ErrorCode = errorCode;
            Parameters = parameters;
        }

        protected ApplicationException(string errorCode, string message, Exception innerException, params object[] parameters)
            : base(message, innerException)
        {
            ErrorCode = errorCode;
            Parameters = parameters;
        }
    }

    /// <summary>
    /// Exception for command/query validation failures
    /// </summary>
    public class CommandValidationException : ApplicationException
    {
        public CommandValidationException(string commandName, string message)
            : base("COMMAND_VALIDATION_FAILED", $"Command '{commandName}' validation failed: {message}")
        {
        }
    }

    /// <summary>
    /// Exception for unauthorized operations
    /// </summary>
    public class UnauthorizedOperationException : ApplicationException
    {
        public UnauthorizedOperationException(string operation, string reason)
            : base("UNAUTHORIZED_OPERATION", $"Unauthorized operation '{operation}': {reason}")
        {
        }
    }

    /// <summary>
    /// Exception for external service failures
    /// </summary>
    public class ExternalServiceException : ApplicationException
    {
        public ExternalServiceException(string serviceName, string operation, Exception innerException)
            : base("EXTERNAL_SERVICE_ERROR", $"External service '{serviceName}' failed for operation '{operation}'", innerException)
        {
        }
    }
}

// Infrastructure/Exceptions/InfrastructureException.cs
using System;

namespace Infrastructure.Exceptions
{
    /// <summary>
    /// Base exception for all infrastructure layer errors
    /// </summary>
    public abstract class InfrastructureException : Exception
    {
        public string ErrorCode { get; }
        public object[] Parameters { get; }

        protected InfrastructureException(string errorCode, string message, params object[] parameters)
            : base(message)
        {
            ErrorCode = errorCode;
            Parameters = parameters;
        }

        protected InfrastructureException(string errorCode, string message, Exception innerException, params object[] parameters)
            : base(message, innerException)
        {
            ErrorCode = errorCode;
            Parameters = parameters;
        }
    }

    /// <summary>
    /// Exception for database operation failures
    /// </summary>
    public class DatabaseException : InfrastructureException
    {
        public DatabaseException(string operation, Exception innerException)
            : base("DATABASE_ERROR", $"Database operation '{operation}' failed", innerException)
        {
        }
    }

    /// <summary>
    /// Exception for external API failures
    /// </summary>
    public class ApiException : InfrastructureException
    {
        public int StatusCode { get; }

        public ApiException(string serviceName, int statusCode, string message)
            : base("API_ERROR", $"API call to '{serviceName}' failed with status {statusCode}: {message}")
        {
            StatusCode = statusCode;
        }
    }

    /// <summary>
    /// Exception for messaging failures
    /// </summary>
    public class MessagingException : InfrastructureException
    {
        public MessagingException(string operation, Exception innerException)
            : base("MESSAGING_ERROR", $"Messaging operation '{operation}' failed", innerException)
        {
        }
    }
}
```

### Exception Usage Examples

```csharp
// Domain/Entities/User.cs
using System;
using Domain.Exceptions;

namespace Domain.Entities
{
    public class User : BaseEntity
    {
        public string Email { get; private set; }
        public string FirstName { get; private set; }
        public string LastName { get; private set; }
        public bool IsActive { get; private set; }

        protected User() { } // EF Core constructor

        public User(string email, string firstName, string lastName)
        {
            if (string.IsNullOrWhiteSpace(email))
                throw new ValidationException("Email", "Email address is required");

            if (string.IsNullOrWhiteSpace(firstName))
                throw new ValidationException("FirstName", "First name is required");

            if (string.IsNullOrWhiteSpace(lastName))
                throw new ValidationException("LastName", "Last name is required");

            if (!IsValidEmail(email))
                throw new ValidationException("Email", "Invalid email format");

            Email = email;
            FirstName = firstName;
            LastName = lastName;
            IsActive = true;
        }

        public void UpdateProfile(string firstName, string lastName)
        {
            if (string.IsNullOrWhiteSpace(firstName))
                throw new ValidationException("FirstName", "First name cannot be empty");

            if (string.IsNullOrWhiteSpace(lastName))
                throw new ValidationException("LastName", "Last name cannot be empty");

            FirstName = firstName;
            LastName = lastName;
        }

        public void Deactivate()
        {
            if (!IsActive)
                throw new BusinessRuleException("UserDeactivation", "User is already inactive");

            IsActive = false;
        }

        private bool IsValidEmail(string email)
        {
            // Simple email validation - in real app, use a proper validator
            return email.Contains("@") && email.Contains(".");
        }
    }
}

// Application/Commands/CreateUserCommandHandler.cs
using System.Threading;
using System.Threading.Tasks;
using Domain.Entities;
using Domain.Interfaces;
using MediatR;
using Microsoft.Extensions.Logging;

namespace Application.Commands
{
    public class CreateUserCommandHandler : IRequestHandler<CreateUserCommand, Guid>
    {
        private readonly IUserRepository _userRepository;
        private readonly ILogger<CreateUserCommandHandler> _logger;

        public CreateUserCommandHandler(
            IUserRepository userRepository,
            ILogger<CreateUserCommandHandler> logger)
        {
            _userRepository = userRepository;
            _logger = logger;
        }

        public async Task<Guid> Handle(CreateUserCommand request, CancellationToken cancellationToken)
        {
            try
            {
                _logger.LogInformation("Creating user with email {Email}", request.Email);

                // Check if user already exists
                var existingUser = await _userRepository.GetByEmailAsync(request.Email);
                if (existingUser != null)
                {
                    throw new UserAlreadyExistsException(request.Email);
                }

                // Create user (this may throw domain exceptions)
                var user = new User(request.Email, request.FirstName, request.LastName);

                await _userRepository.AddAsync(user);
                await _userRepository.SaveChangesAsync();

                _logger.LogInformation("User created with ID {UserId}", user.Id);

                return user.Id;
            }
            catch (DomainException ex)
            {
                _logger.LogWarning(ex, "Domain validation failed for user creation: {ErrorCode}", ex.ErrorCode);
                throw;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error during user creation");
                throw new ApplicationException("USER_CREATION_FAILED", "Failed to create user", ex);
            }
        }
    }
}
```

## Retry and Circuit Breaker Patterns

### Polly Implementation

```csharp
// Infrastructure/Resilience/RetryPolicies.cs
using System;
using System.Net.Http;
using Polly;
using Polly.CircuitBreaker;
using Polly.Retry;
using Polly.Timeout;

namespace Infrastructure.Resilience
{
    public static class RetryPolicies
    {
        /// <summary>
        /// Creates a retry policy for HTTP requests
        /// </summary>
        public static IAsyncPolicy<HttpResponseMessage> GetHttpRetryPolicy(int retryCount = 3)
        {
            return Policy<HttpResponseMessage>
                .Handle<HttpRequestException>()
                .Or<TimeoutRejectedException>()
                .OrResult(response => !response.IsSuccessStatusCode &&
                    (response.StatusCode == System.Net.HttpStatusCode.RequestTimeout ||
                     response.StatusCode == System.Net.HttpStatusCode.TooManyRequests ||
                     response.StatusCode == System.Net.HttpStatusCode.InternalServerError ||
                     response.StatusCode == System.Net.HttpStatusCode.BadGateway ||
                     response.StatusCode == System.Net.HttpStatusCode.ServiceUnavailable ||
                     response.StatusCode == System.Net.HttpStatusCode.GatewayTimeout))
                .WaitAndRetryAsync(retryCount, retryAttempt =>
                    TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
        }

        /// <summary>
        /// Creates a circuit breaker policy
        /// </summary>
        public static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy(
            int exceptionsAllowedBeforeBreaking = 5,
            TimeSpan durationOfBreak = default)
        {
            if (durationOfBreak == default)
                durationOfBreak = TimeSpan.FromSeconds(30);

            return Policy<HttpResponseMessage>
                .Handle<HttpRequestException>()
                .Or<TimeoutRejectedException>()
                .OrResult(response => !response.IsSuccessStatusCode)
                .CircuitBreakerAsync(exceptionsAllowedBeforeBreaking, durationOfBreak);
        }

        /// <summary>
        /// Creates a timeout policy
        /// </summary>
        public static IAsyncPolicy<HttpResponseMessage> GetTimeoutPolicy(TimeSpan timeout)
        {
            return Policy.TimeoutAsync<HttpResponseMessage>(timeout);
        }

        /// <summary>
        /// Creates a combined policy with retry, circuit breaker, and timeout
        /// </summary>
        public static IAsyncPolicy<HttpResponseMessage> GetResilientHttpPolicy(
            int retryCount = 3,
            int exceptionsAllowedBeforeBreaking = 5,
            TimeSpan durationOfBreak = default,
            TimeSpan timeout = default)
        {
            if (durationOfBreak == default)
                durationOfBreak = TimeSpan.FromSeconds(30);

            if (timeout == default)
                timeout = TimeSpan.FromSeconds(10);

            var retryPolicy = GetHttpRetryPolicy(retryCount);
            var circuitBreakerPolicy = GetCircuitBreakerPolicy(exceptionsAllowedBeforeBreaking, durationOfBreak);
            var timeoutPolicy = GetTimeoutPolicy(timeout);

            return Policy.WrapAsync(retryPolicy, circuitBreakerPolicy, timeoutPolicy);
        }
    }
}

// Infrastructure/Resilience/DatabaseRetryPolicies.cs
using System;
using Microsoft.EntityFrameworkCore;
using Polly;
using Polly.Retry;

namespace Infrastructure.Resilience
{
    public static class DatabaseRetryPolicies
    {
        /// <summary>
        /// Creates a retry policy for database operations
        /// </summary>
        public static AsyncRetryPolicy GetDatabaseRetryPolicy(int retryCount = 3)
        {
            return Policy
                .Handle<DbUpdateException>()
                .Or<DbUpdateConcurrencyException>()
                .Or<InvalidOperationException>(ex => ex.Message.Contains("connection"))
                .WaitAndRetryAsync(retryCount, retryAttempt =>
                    TimeSpan.FromMilliseconds(100 * Math.Pow(2, retryAttempt)));
        }

        /// <summary>
        /// Creates a retry policy for database queries
        /// </summary>
        public static AsyncRetryPolicy<TResult> GetDatabaseQueryRetryPolicy<TResult>(int retryCount = 3)
        {
            return Policy<TResult>
                .Handle<DbUpdateException>()
                .Or<InvalidOperationException>(ex => ex.Message.Contains("connection"))
                .WaitAndRetryAsync(retryCount, retryAttempt =>
                    TimeSpan.FromMilliseconds(100 * Math.Pow(2, retryAttempt)));
        }
    }
}
```

### External Service Client with Resilience

```csharp
// Infrastructure/External/ExternalApiClient.cs
using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using Application.Interfaces;
using Infrastructure.Exceptions;
using Infrastructure.Resilience;
using Microsoft.Extensions.Logging;
using Polly;

namespace Infrastructure.External
{
    public class ExternalApiClient : IExternalApiClient
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<ExternalApiClient> _logger;
        private readonly IAsyncPolicy<HttpResponseMessage> _resilientPolicy;

        public ExternalApiClient(
            HttpClient httpClient,
            ILogger<ExternalApiClient> logger)
        {
            _httpClient = httpClient;
            _logger = logger;

            // Configure resilient HTTP policy
            _resilientPolicy = RetryPolicies.GetResilientHttpPolicy(
                retryCount: 3,
                exceptionsAllowedBeforeBreaking: 5,
                durationOfBreak: TimeSpan.FromSeconds(30),
                timeout: TimeSpan.FromSeconds(10));
        }

        public async Task<TResponse> GetAsync<TResponse>(string endpoint)
        {
            return await ExecuteWithResilience(async () =>
            {
                var response = await _httpClient.GetAsync(endpoint);
                return await response.Content.ReadFromJsonAsync<TResponse>();
            }, $"GET {endpoint}");
        }

        public async Task<TResponse> PostAsync<TRequest, TResponse>(string endpoint, TRequest data)
        {
            return await ExecuteWithResilience(async () =>
            {
                var response = await _httpClient.PostAsJsonAsync(endpoint, data);
                return await response.Content.ReadFromJsonAsync<TResponse>();
            }, $"POST {endpoint}");
        }

        public async Task PutAsync<TRequest>(string endpoint, TRequest data)
        {
            await ExecuteWithResilience(async () =>
            {
                var response = await _httpClient.PutAsJsonAsync(endpoint, data);
                return response;
            }, $"PUT {endpoint}");
        }

        public async Task DeleteAsync(string endpoint)
        {
            await ExecuteWithResilience(async () =>
            {
                var response = await _httpClient.DeleteAsync(endpoint);
                return response;
            }, $"DELETE {endpoint}");
        }

        private async Task<T> ExecuteWithResilience<T>(Func<Task<T>> operation, string operationName)
        {
            try
            {
                _logger.LogInformation("Executing external API operation: {Operation}", operationName);

                var result = await _resilientPolicy.ExecuteAsync(async () =>
                {
                    var response = await operation();

                    // Handle HTTP response
                    if (response is HttpResponseMessage httpResponse)
                    {
                        if (!httpResponse.IsSuccessStatusCode)
                        {
                            var errorContent = await httpResponse.Content.ReadAsStringAsync();
                            _logger.LogWarning("External API call failed: {StatusCode} - {Error}",
                                httpResponse.StatusCode, errorContent);

                            throw new ApiException("ExternalService", (int)httpResponse.StatusCode, errorContent);
                        }

                        return response;
                    }

                    return response;
                });

                _logger.LogInformation("External API operation completed successfully: {Operation}", operationName);
                return result;
            }
            catch (BrokenCircuitException ex)
            {
                _logger.LogError(ex, "Circuit breaker is open for external API operation: {Operation}", operationName);
                throw new ExternalServiceException("ExternalApi", operationName, ex);
            }
            catch (ApiException)
            {
                // Re-throw API exceptions as-is
                throw;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error during external API operation: {Operation}", operationName);
                throw new ExternalServiceException("ExternalApi", operationName, ex);
            }
        }
    }
}

// Infrastructure/External/EmailService.cs
using System.Net;
using System.Net.Mail;
using System.Threading.Tasks;
using Application.Interfaces;
using Infrastructure.Exceptions;
using Infrastructure.Resilience;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Polly;

namespace Infrastructure.External
{
    public class EmailService : IEmailService
    {
        private readonly EmailSettings _emailSettings;
        private readonly ILogger<EmailService> _logger;
        private readonly AsyncRetryPolicy _retryPolicy;

        public EmailService(IOptions<EmailSettings> emailSettings, ILogger<EmailService> logger)
        {
            _emailSettings = emailSettings.Value;
            _logger = logger;

            // Configure retry policy for email operations
            _retryPolicy = Policy
                .Handle<SmtpException>()
                .Or<InvalidOperationException>()
                .WaitAndRetryAsync(3, retryAttempt =>
                    TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
        }

        public async Task SendEmailAsync(string to, string subject, string body)
        {
            await _retryPolicy.ExecuteAsync(async () =>
            {
                try
                {
                    using var smtpClient = new SmtpClient(_emailSettings.SmtpServer, _emailSettings.Port)
                    {
                        Credentials = new NetworkCredential(_emailSettings.Username, _emailSettings.Password),
                        EnableSsl = _emailSettings.EnableSsl
                    };

                    var mailMessage = new MailMessage
                    {
                        From = new MailAddress(_emailSettings.FromEmail, _emailSettings.FromName),
                        Subject = subject,
                        Body = body,
                        IsBodyHtml = true
                    };

                    mailMessage.To.Add(to);

                    await smtpClient.SendMailAsync(mailMessage);
                    _logger.LogInformation("Email sent to {To} with subject '{Subject}'", to, subject);
                }
                catch (SmtpException ex)
                {
                    _logger.LogError(ex, "SMTP error while sending email to {To}: {Message}", to, ex.Message);
                    throw new InfrastructureException("EMAIL_SEND_FAILED",
                        $"Failed to send email to {to}", ex);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Unexpected error while sending email to {To}", to);
                    throw new InfrastructureException("EMAIL_SEND_FAILED",
                        $"Failed to send email to {to}", ex);
                }
            });
        }
    }
}
```

## Global Exception Handling

### ASP.NET Core Exception Middleware

```csharp
// Api/Middleware/GlobalExceptionMiddleware.cs
using System;
using System.Net;
using System.Text.Json;
using System.Threading.Tasks;
using Domain.Exceptions;
using Infrastructure.Exceptions;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Hosting;

namespace Api.Middleware
{
    public class GlobalExceptionMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<GlobalExceptionMiddleware> _logger;
        private readonly IHostEnvironment _environment;

        public GlobalExceptionMiddleware(
            RequestDelegate next,
            ILogger<GlobalExceptionMiddleware> _logger,
            IHostEnvironment environment)
        {
            _next = next;
            this._logger = _logger;
            _environment = environment;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (Exception ex)
            {
                await HandleExceptionAsync(context, ex);
            }
        }

        private async Task HandleExceptionAsync(HttpContext context, Exception exception)
        {
            var errorResponse = CreateErrorResponse(exception);
            var statusCode = GetStatusCode(exception);

            context.Response.ContentType = "application/json";
            context.Response.StatusCode = statusCode;

            _logger.LogError(exception, "An error occurred: {ErrorCode} - {Message}",
                errorResponse.ErrorCode, errorResponse.Message);

            var options = new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                WriteIndented = _environment.IsDevelopment()
            };

            await context.Response.WriteAsync(JsonSerializer.Serialize(errorResponse, options));
        }

        private ErrorResponse CreateErrorResponse(Exception exception)
        {
            return exception switch
            {
                DomainException domainEx => new ErrorResponse(
                    domainEx.ErrorCode,
                    domainEx.Message,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                ApplicationException appEx => new ErrorResponse(
                    appEx.ErrorCode,
                    appEx.Message,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                InfrastructureException infraEx => new ErrorResponse(
                    infraEx.ErrorCode,
                    infraEx.Message,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                FluentValidation.ValidationException validationEx => new ErrorResponse(
                    "VALIDATION_ERROR",
                    "Validation failed",
                    _environment.IsDevelopment() ? string.Join("; ", validationEx.Errors.Select(e => e.ErrorMessage)) : null,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                _ => new ErrorResponse(
                    "INTERNAL_SERVER_ERROR",
                    _environment.IsDevelopment() ? exception.Message : "An unexpected error occurred",
                    _environment.IsDevelopment() ? exception.StackTrace : null)
            };
        }

        private int GetStatusCode(Exception exception)
        {
            return exception switch
            {
                EntityNotFoundException => StatusCodes.Status404NotFound,
                ValidationException => StatusCodes.Status400BadRequest,
                BusinessRuleException => StatusCodes.Status409Conflict,
                ConcurrencyException => StatusCodes.Status409Conflict,
                UnauthorizedOperationException => StatusCodes.Status403Forbidden,
                FluentValidation.ValidationException => StatusCodes.Status400BadRequest,
                ApiException apiEx when apiEx.StatusCode == 404 => StatusCodes.Status404NotFound,
                ApiException apiEx when apiEx.StatusCode == 400 => StatusCodes.Status400BadRequest,
                ApiException apiEx when apiEx.StatusCode == 401 => StatusCodes.Status401Unauthorized,
                ApiException apiEx when apiEx.StatusCode == 403 => StatusCodes.Status403Forbidden,
                ApiException => StatusCodes.Status502BadGateway,
                ExternalServiceException => StatusCodes.Status502BadGateway,
                DatabaseException => StatusCodes.Status500InternalServerError,
                _ => StatusCodes.Status500InternalServerError
            };
        }
    }

    public static class GlobalExceptionMiddlewareExtensions
    {
        public static IApplicationBuilder UseGlobalExceptionHandler(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<GlobalExceptionMiddleware>();
        }
    }

    public class ErrorResponse
    {
        public string ErrorCode { get; set; }
        public string Message { get; set; }
        public string Details { get; set; }
        public string StackTrace { get; set; }
        public DateTime Timestamp { get; set; }

        public ErrorResponse(string errorCode, string message, string details = null, string stackTrace = null)
        {
            ErrorCode = errorCode;
            Message = message;
            Details = details;
            StackTrace = stackTrace;
            Timestamp = DateTime.UtcNow;
        }
    }
}
```

### Exception Filters

```csharp
// Api/Filters/GlobalExceptionFilter.cs
using System;
using System.Linq;
using Domain.Exceptions;
using Infrastructure.Exceptions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Api.Filters
{
    public class GlobalExceptionFilter : IExceptionFilter
    {
        private readonly ILogger<GlobalExceptionFilter> _logger;
        private readonly IHostEnvironment _environment;

        public GlobalExceptionFilter(ILogger<GlobalExceptionFilter> logger, IHostEnvironment environment)
        {
            _logger = logger;
            _environment = environment;
        }

        public void OnException(ExceptionContext context)
        {
            var exception = context.Exception;
            var errorResponse = CreateErrorResponse(exception);
            var statusCode = GetStatusCode(exception);

            context.Result = new ObjectResult(errorResponse)
            {
                StatusCode = statusCode
            };

            context.ExceptionHandled = true;

            _logger.LogError(exception, "An unhandled exception occurred: {ErrorCode} - {Message}",
                errorResponse.ErrorCode, errorResponse.Message);
        }

        private ErrorResponse CreateErrorResponse(Exception exception)
        {
            return exception switch
            {
                DomainException domainEx => new ErrorResponse(
                    domainEx.ErrorCode,
                    domainEx.Message,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                ApplicationException appEx => new ErrorResponse(
                    appEx.ErrorCode,
                    appEx.Message,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                InfrastructureException infraEx => new ErrorResponse(
                    infraEx.ErrorCode,
                    infraEx.Message,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                FluentValidation.ValidationException validationEx => new ErrorResponse(
                    "VALIDATION_ERROR",
                    "Validation failed",
                    _environment.IsDevelopment() ? string.Join("; ", validationEx.Errors.Select(e => e.ErrorMessage)) : null,
                    _environment.IsDevelopment() ? exception.StackTrace : null),

                _ => new ErrorResponse(
                    "INTERNAL_SERVER_ERROR",
                    _environment.IsDevelopment() ? exception.Message : "An unexpected error occurred",
                    null,
                    _environment.IsDevelopment() ? exception.StackTrace : null)
            };
        }

        private int GetStatusCode(Exception exception)
        {
            return exception switch
            {
                EntityNotFoundException => StatusCodes.Status404NotFound,
                ValidationException => StatusCodes.Status400BadRequest,
                BusinessRuleException => StatusCodes.Status409Conflict,
                ConcurrencyException => StatusCodes.Status409Conflict,
                UnauthorizedOperationException => StatusCodes.Status403Forbidden,
                FluentValidation.ValidationException => StatusCodes.Status400BadRequest,
                ApiException apiEx when apiEx.StatusCode == 404 => StatusCodes.Status404NotFound,
                ApiException apiEx when apiEx.StatusCode == 400 => StatusCodes.Status400BadRequest,
                ApiException apiEx when apiEx.StatusCode == 401 => StatusCodes.Status401Unauthorized,
                ApiException apiEx when apiEx.StatusCode == 403 => StatusCodes.Status403Forbidden,
                ApiException => StatusCodes.Status502BadGateway,
                ExternalServiceException => StatusCodes.Status502BadGateway,
                DatabaseException => StatusCodes.Status500InternalServerError,
                _ => StatusCodes.Status500InternalServerError
            };
        }
    }

    public class ErrorResponse
    {
        public string ErrorCode { get; set; }
        public string Message { get; set; }
        public string Details { get; set; }
        public string StackTrace { get; set; }
        public DateTime Timestamp { get; set; }

        public ErrorResponse(string errorCode, string message, string details = null, string stackTrace = null)
        {
            ErrorCode = errorCode;
            Message = message;
            Details = details;
            StackTrace = stackTrace;
            Timestamp = DateTime.UtcNow;
        }
    }
}
```

## Result Pattern Implementation

### Result and Error Types

```csharp
// Application/Common/Result.cs
using System;
using System.Collections.Generic;
using System.Linq;

namespace Application.Common
{
    public class Result
    {
        public bool IsSuccess { get; }
        public bool IsFailure => !IsSuccess;
        public string ErrorCode { get; }
        public string ErrorMessage { get; }
        public object[] ErrorParameters { get; }

        protected Result(bool isSuccess, string errorCode = null, string errorMessage = null, params object[] errorParameters)
        {
            IsSuccess = isSuccess;
            ErrorCode = errorCode;
            ErrorMessage = errorMessage;
            ErrorParameters = errorParameters;
        }

        public static Result Success() => new Result(true);

        public static Result Failure(string errorCode, string errorMessage, params object[] errorParameters)
            => new Result(false, errorCode, errorMessage, errorParameters);

        public static Result<T> Success<T>(T value) => Result<T>.Success(value);

        public static Result<T> Failure<T>(string errorCode, string errorMessage, params object[] errorParameters)
            => Result<T>.Failure(errorCode, errorMessage, errorParameters);
    }

    public class Result<T> : Result
    {
        public T Value { get; }

        protected Result(T value, bool isSuccess, string errorCode = null, string errorMessage = null, params object[] errorParameters)
            : base(isSuccess, errorCode, errorMessage, errorParameters)
        {
            Value = value;
        }

        public static Result<T> Success(T value) => new Result<T>(value, true);

        public static Result<T> Failure(string errorCode, string errorMessage, params object[] errorParameters)
            => new Result<T>(default, false, errorCode, errorMessage, errorParameters);

        public Result<T> OnSuccess(Func<T, Result<T>> func)
        {
            return IsSuccess ? func(Value) : this;
        }

        public Result<U> OnSuccess<U>(Func<T, Result<U>> func)
        {
            return IsSuccess ? func(Value) : Result<U>.Failure(ErrorCode, ErrorMessage, ErrorParameters);
        }

        public Result<T> OnFailure(Func<Result<T>> func)
        {
            return IsFailure ? func() : this;
        }

        public T OnBoth(Func<Result<T>, T> func)
        {
            return func(this);
        }
    }
}

// Application/Common/ResultExtensions.cs
using System;
using System.Threading.Tasks;

namespace Application.Common
{
    public static class ResultExtensions
    {
        public static Result<T> ToResult<T>(this T value)
        {
            return Result<T>.Success(value);
        }

        public static Result<T> ToResult<T>(this T value, Func<T, bool> predicate, string errorCode, string errorMessage)
        {
            return predicate(value) ? Result<T>.Success(value) : Result<T>.Failure(errorCode, errorMessage);
        }

        public static async Task<Result<T>> ToResultAsync<T>(this Task<T> task)
        {
            try
            {
                var value = await task;
                return Result<T>.Success(value);
            }
            catch (Exception ex)
            {
                return Result<T>.Failure("OPERATION_FAILED", ex.Message);
            }
        }

        public static Result<T> Ensure<T>(this Result<T> result, Func<T, bool> predicate, string errorCode, string errorMessage)
        {
            if (result.IsFailure)
                return result;

            return predicate(result.Value) ? result : Result<T>.Failure(errorCode, errorMessage);
        }

        public static Result<T> Map<T, U>(this Result<U> result, Func<U, T> mapper)
        {
            return result.IsSuccess ? Result<T>.Success(mapper(result.Value)) : Result<T>.Failure(result.ErrorCode, result.ErrorMessage, result.ErrorParameters);
        }

        public static async Task<Result<T>> MapAsync<T, U>(this Result<U> result, Func<U, Task<T>> mapper)
        {
            return result.IsSuccess ? Result<T>.Success(await mapper(result.Value)) : Result<T>.Failure(result.ErrorCode, result.ErrorMessage, result.ErrorParameters);
        }

        public static Result<T> Bind<T, U>(this Result<U> result, Func<U, Result<T>> binder)
        {
            return result.IsSuccess ? binder(result.Value) : Result<T>.Failure(result.ErrorCode, result.ErrorMessage, result.ErrorParameters);
        }

        public static async Task<Result<T>> BindAsync<T, U>(this Result<U> result, Func<U, Task<Result<T>>> binder)
        {
            return result.IsSuccess ? await binder(result.Value) : Result<T>.Failure(result.ErrorCode, result.ErrorMessage, result.ErrorParameters);
        }
    }
}
```

### Result-Based Command Handler

```csharp
// Application/Commands/CreateUserCommand.cs
using Application.Common;
using MediatR;

namespace Application.Commands
{
    public class CreateUserCommand : IRequest<Result<Guid>>
    {
        public string Email { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Password { get; set; }
    }

    public class CreateUserCommandHandler : IRequestHandler<CreateUserCommand, Result<Guid>>
    {
        private readonly IUserRepository _userRepository;
        private readonly IPasswordHasher _passwordHasher;
        private readonly ILogger<CreateUserCommandHandler> _logger;

        public CreateUserCommandHandler(
            IUserRepository userRepository,
            IPasswordHasher passwordHasher,
            ILogger<CreateUserCommandHandler> logger)
        {
            _userRepository = userRepository;
            _passwordHasher = passwordHasher;
            _logger = logger;
        }

        public async Task<Result<Guid>> Handle(CreateUserCommand request, CancellationToken cancellationToken)
        {
            try
            {
                _logger.LogInformation("Creating user with email {Email}", request.Email);

                // Validate input
                var validationResult = await ValidateRequest(request);
                if (validationResult.IsFailure)
                    return validationResult;

                // Check if user already exists
                var existingUser = await _userRepository.GetByEmailAsync(request.Email);
                if (existingUser != null)
                {
                    return Result<Guid>.Failure("USER_ALREADY_EXISTS",
                        $"User with email '{request.Email}' already exists");
                }

                // Hash password
                var passwordHash = await _passwordHasher.HashPasswordAsync(request.Password);

                // Create user
                var user = new User(request.Email, request.FirstName, request.LastName, passwordHash);

                await _userRepository.AddAsync(user);
                await _userRepository.SaveChangesAsync();

                _logger.LogInformation("User created with ID {UserId}", user.Id);

                return Result<Guid>.Success(user.Id);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error during user creation");
                return Result<Guid>.Failure("USER_CREATION_FAILED", "Failed to create user");
            }
        }

        private async Task<Result<Guid>> ValidateRequest(CreateUserCommand request)
        {
            if (string.IsNullOrWhiteSpace(request.Email))
                return Result<Guid>.Failure("VALIDATION_ERROR", "Email is required");

            if (string.IsNullOrWhiteSpace(request.FirstName))
                return Result<Guid>.Failure("VALIDATION_ERROR", "First name is required");

            if (string.IsNullOrWhiteSpace(request.LastName))
                return Result<Guid>.Failure("VALIDATION_ERROR", "Last name is required");

            if (string.IsNullOrWhiteSpace(request.Password) || request.Password.Length < 8)
                return Result<Guid>.Failure("VALIDATION_ERROR", "Password must be at least 8 characters long");

            // Additional validation logic...
            return Result<Guid>.Success(Guid.Empty); // Placeholder for success
        }
    }
}
```

## Error Context and Logging

### Structured Error Context

```csharp
// Application/Common/ErrorContext.cs
using System;
using System.Collections.Generic;
using System.Linq;

namespace Application.Common
{
    public class ErrorContext
    {
        public string Operation { get; set; }
        public string UserId { get; set; }
        public string CorrelationId { get; set; }
        public Dictionary<string, object> AdditionalData { get; } = new();
        public List<string> Tags { get; } = new();

        public ErrorContext(string operation, string userId = null, string correlationId = null)
        {
            Operation = operation;
            UserId = userId;
            CorrelationId = correlationId ?? Guid.NewGuid().ToString();
        }

        public ErrorContext WithTag(string tag)
        {
            Tags.Add(tag);
            return this;
        }

        public ErrorContext WithData(string key, object value)
        {
            AdditionalData[key] = value;
            return this;
        }

        public override string ToString()
        {
            var parts = new List<string>
            {
                $"Operation: {Operation}",
                $"CorrelationId: {CorrelationId}"
            };

            if (!string.IsNullOrEmpty(UserId))
                parts.Add($"UserId: {UserId}");

            if (Tags.Any())
                parts.Add($"Tags: {string.Join(", ", Tags)}");

            if (AdditionalData.Any())
                parts.Add($"Data: {string.Join(", ", AdditionalData.Select(kv => $"{kv.Key}={kv.Value}"))}");

            return string.Join(" | ", parts);
        }
    }
}

// Application/Common/ErrorContextExtensions.cs
using System;
using Microsoft.Extensions.Logging;

namespace Application.Common
{
    public static class ErrorContextExtensions
    {
        public static void LogErrorWithContext(this ILogger logger, Exception exception,
            string message, ErrorContext context)
        {
            using (logger.BeginScope(context.ToString()))
            {
                logger.LogError(exception, message);
            }
        }

        public static void LogWarningWithContext(this ILogger logger, string message, ErrorContext context)
        {
            using (logger.BeginScope(context.ToString()))
            {
                logger.LogWarning(message);
            }
        }

        public static void LogInformationWithContext(this ILogger logger, string message, ErrorContext context)
        {
            using (logger.BeginScope(context.ToString()))
            {
                logger.LogInformation(message);
            }
        }
    }
}
```

### Enhanced Exception with Context

```csharp
// Domain/Exceptions/ContextualException.cs
using System;
using Application.Common;

namespace Domain.Exceptions
{
    public abstract class ContextualException : DomainException
    {
        public ErrorContext Context { get; }

        protected ContextualException(string errorCode, string message, ErrorContext context, params object[] parameters)
            : base(errorCode, message, parameters)
        {
            Context = context;
        }

        protected ContextualException(string errorCode, string message, ErrorContext context,
            Exception innerException, params object[] parameters)
            : base(errorCode, message, innerException, parameters)
        {
            Context = context;
        }
    }

    public class ContextualValidationException : ContextualException
    {
        public ContextualValidationException(string fieldName, string validationMessage, ErrorContext context)
            : base("VALIDATION_ERROR", $"Validation failed for field '{fieldName}': {validationMessage}", context)
        {
        }
    }

    public class ContextualBusinessRuleException : ContextualException
    {
        public ContextualBusinessRuleException(string ruleName, string message, ErrorContext context)
            : base("BUSINESS_RULE_VIOLATION", $"Business rule '{ruleName}' violated: {message}", context)
        {
        }
    }
}
```

This comprehensive guide covers C# error handling patterns including custom exception hierarchies, retry and circuit breaker patterns with Polly, global exception handling middleware and filters, result pattern implementation, and structured error context and logging for robust .NET applications.