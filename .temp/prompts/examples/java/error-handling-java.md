# Error Handling Patterns for Java

This guide covers comprehensive error handling patterns for Java applications, including custom exceptions, retry mechanisms, circuit breaker patterns, and best practices for enterprise applications.

## Project Setup and Dependencies

### Maven Dependencies

```xml
<!-- pom.xml -->
<dependencies>
    <!-- Resilience4j for circuit breaker and retry -->
    <dependency>
        <groupId>io.github.resilience4j</groupId>
        <artifactId>resilience4j-spring-boot2</artifactId>
        <version>1.7.1</version>
    </dependency>

    <!-- Spring Boot Validation -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>

    <!-- Logging -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-log4j2</artifactId>
    </dependency>

    <!-- Testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

    <!-- Resilience4j Test -->
    <dependency>
        <groupId>io.github.resilience4j</groupId>
        <artifactId>resilience4j-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Gradle Dependencies

```gradle
// build.gradle
dependencies {
    // Resilience4j for circuit breaker and retry
    implementation 'io.github.resilience4j:resilience4j-spring-boot2:1.7.1'

    // Spring Boot Validation
    implementation 'org.springframework.boot:spring-boot-starter-validation'

    // Logging
    implementation 'org.springframework.boot:spring-boot-starter-log4j2'

    // Testing
    testImplementation 'org.springframework.boot:spring-boot-starter-test'

    // Resilience4j Test
    testImplementation 'io.github.resilience4j:resilience4j-test'
}
```

## Custom Exception Hierarchy

### Base Exception Classes

```java
// src/main/java/com/example/common/exception/BaseException.java
package com.example.common.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Base exception class for all application exceptions.
 * Provides consistent error handling and logging across the application.
 */
@Getter
public abstract class BaseException extends RuntimeException {

    private final String errorCode;
    private final HttpStatus httpStatus;
    private final LocalDateTime timestamp;
    private final Map<String, Object> context;

    protected BaseException(String message, String errorCode, HttpStatus httpStatus) {
        this(message, errorCode, httpStatus, null, null);
    }

    protected BaseException(String message, String errorCode, HttpStatus httpStatus,
                           Map<String, Object> context) {
        this(message, errorCode, httpStatus, context, null);
    }

    protected BaseException(String message, String errorCode, HttpStatus httpStatus,
                           Map<String, Object> context, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
        this.httpStatus = httpStatus;
        this.timestamp = LocalDateTime.now();
        this.context = context;
    }

    /**
     * Returns a detailed error message including context information.
     */
    public String getDetailedMessage() {
        StringBuilder sb = new StringBuilder();
        sb.append("Error Code: ").append(errorCode).append("\n");
        sb.append("Message: ").append(getMessage()).append("\n");
        sb.append("Timestamp: ").append(timestamp).append("\n");

        if (context != null && !context.isEmpty()) {
            sb.append("Context:\n");
            context.forEach((key, value) ->
                sb.append("  ").append(key).append(": ").append(value).append("\n"));
        }

        if (getCause() != null) {
            sb.append("Cause: ").append(getCause().getMessage()).append("\n");
        }

        return sb.toString();
    }
}

// src/main/java/com/example/common/exception/BusinessException.java
package com.example.common.exception;

import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Exception for business logic violations.
 * These are client errors that should not be retried.
 */
public class BusinessException extends BaseException {

    public BusinessException(String message) {
        super(message, "BUSINESS_ERROR", HttpStatus.BAD_REQUEST);
    }

    public BusinessException(String message, Map<String, Object> context) {
        super(message, "BUSINESS_ERROR", HttpStatus.BAD_REQUEST, context);
    }

    public BusinessException(String message, Throwable cause) {
        super(message, "BUSINESS_ERROR", HttpStatus.BAD_REQUEST, null, cause);
    }
}

// src/main/java/com/example/common/exception/ValidationException.java
package com.example.common.exception;

import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Exception for validation errors.
 * Used when input data fails validation rules.
 */
public class ValidationException extends BaseException {

    public ValidationException(String message) {
        super(message, "VALIDATION_ERROR", HttpStatus.BAD_REQUEST);
    }

    public ValidationException(String message, Map<String, Object> context) {
        super(message, "VALIDATION_ERROR", HttpStatus.BAD_REQUEST, context);
    }
}

// src/main/java/com/example/common/exception/ResourceNotFoundException.java
package com.example.common.exception;

import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Exception for resources that cannot be found.
 */
public class ResourceNotFoundException extends BaseException {

    public ResourceNotFoundException(String resourceType, String resourceId) {
        super(String.format("%s with id '%s' not found", resourceType, resourceId),
              "RESOURCE_NOT_FOUND", HttpStatus.NOT_FOUND,
              Map.of("resourceType", resourceType, "resourceId", resourceId));
    }

    public ResourceNotFoundException(String message) {
        super(message, "RESOURCE_NOT_FOUND", HttpStatus.NOT_FOUND);
    }
}

// src/main/java/com/example/common/exception/SystemException.java
package com.example.common.exception;

import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Exception for system-level errors (database, external services, etc.).
 * These are server errors that might be retried.
 */
public class SystemException extends BaseException {

    public SystemException(String message) {
        super(message, "SYSTEM_ERROR", HttpStatus.INTERNAL_SERVER_ERROR);
    }

    public SystemException(String message, Throwable cause) {
        super(message, "SYSTEM_ERROR", HttpStatus.INTERNAL_SERVER_ERROR, null, cause);
    }

    public SystemException(String message, Map<String, Object> context, Throwable cause) {
        super(message, "SYSTEM_ERROR", HttpStatus.INTERNAL_SERVER_ERROR, context, cause);
    }
}

// src/main/java/com/example/common/exception/ExternalServiceException.java
package com.example.common.exception;

import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Exception for external service failures.
 * Used when calling external APIs or services.
 */
public class ExternalServiceException extends BaseException {

    public ExternalServiceException(String serviceName, String operation) {
        super(String.format("External service '%s' failed during '%s'", serviceName, operation),
              "EXTERNAL_SERVICE_ERROR", HttpStatus.BAD_GATEWAY,
              Map.of("serviceName", serviceName, "operation", operation));
    }

    public ExternalServiceException(String serviceName, String operation, Throwable cause) {
        super(String.format("External service '%s' failed during '%s'", serviceName, operation),
              "EXTERNAL_SERVICE_ERROR", HttpStatus.BAD_GATEWAY,
              Map.of("serviceName", serviceName, "operation", operation), cause);
    }
}
```

### Domain-Specific Exceptions

```java
// src/main/java/com/example/user/exception/UserException.java
package com.example.user.exception;

import com.example.common.exception.BaseException;
import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Base exception for user domain errors.
 */
public abstract class UserException extends BaseException {

    protected UserException(String message, String errorCode, HttpStatus httpStatus) {
        super(message, errorCode, httpStatus);
    }

    protected UserException(String message, String errorCode, HttpStatus httpStatus,
                           Map<String, Object> context) {
        super(message, errorCode, httpStatus, context);
    }

    protected UserException(String message, String errorCode, HttpStatus httpStatus,
                           Map<String, Object> context, Throwable cause) {
        super(message, errorCode, httpStatus, context, cause);
    }
}

// src/main/java/com/example/user/exception/UserNotFoundException.java
package com.example.user.exception;

import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Exception thrown when a user cannot be found.
 */
public class UserNotFoundException extends UserException {

    public UserNotFoundException(String userId) {
        super(String.format("User with id '%s' not found", userId),
              "USER_NOT_FOUND", HttpStatus.NOT_FOUND,
              Map.of("userId", userId));
    }

    public UserNotFoundException(String userId, Throwable cause) {
        super(String.format("User with id '%s' not found", userId),
              "USER_NOT_FOUND", HttpStatus.NOT_FOUND,
              Map.of("userId", userId), cause);
    }
}

// src/main/java/com/example/user/exception/UserAlreadyExistsException.java
package com.example.user.exception;

import org.springframework.http.HttpStatus;

import java.util.Map;

/**
 * Exception thrown when attempting to create a user that already exists.
 */
public class UserAlreadyExistsException extends UserException {

    public UserAlreadyExistsException(String email) {
        super(String.format("User with email '%s' already exists", email),
              "USER_ALREADY_EXISTS", HttpStatus.CONFLICT,
              Map.of("email", email));
    }
}

// src/main/java/com/example/user/exception/InvalidCredentialsException.java
package com.example.user.exception;

import org.springframework.http.HttpStatus;

/**
 * Exception thrown when user credentials are invalid.
 */
public class InvalidCredentialsException extends UserException {

    public InvalidCredentialsException() {
        super("Invalid email or password", "INVALID_CREDENTIALS", HttpStatus.UNAUTHORIZED);
    }
}
```

## Global Exception Handler

### Spring Boot Global Exception Handler

```java
// src/main/java/com/example/common/exception/GlobalExceptionHandler.java
package com.example.common.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;

import javax.validation.ConstraintViolation;
import javax.validation.ConstraintViolationException;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Global exception handler for all REST controllers.
 * Provides consistent error responses across the application.
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handle custom BaseException and its subclasses.
     */
    @ExceptionHandler(BaseException.class)
    public ResponseEntity<ErrorResponse> handleBaseException(BaseException ex, WebRequest request) {
        log.error("BaseException occurred: {}", ex.getDetailedMessage(), ex);

        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(ex.getTimestamp())
                .status(ex.getHttpStatus().value())
                .error(ex.getHttpStatus().getReasonPhrase())
                .message(ex.getMessage())
                .errorCode(ex.getErrorCode())
                .path(request.getDescription(false).replace("uri=", ""))
                .context(ex.getContext())
                .build();

        return new ResponseEntity<>(errorResponse, ex.getHttpStatus());
    }

    /**
     * Handle validation errors from @Valid annotations.
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex, WebRequest request) {

        Map<String, String> fieldErrors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach(error -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            fieldErrors.put(fieldName, errorMessage);
        });

        log.warn("Validation error: {}", fieldErrors);

        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message("Validation failed")
                .errorCode("VALIDATION_ERROR")
                .path(request.getDescription(false).replace("uri=", ""))
                .context(Map.of("fieldErrors", fieldErrors))
                .build();

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    /**
     * Handle constraint violations from method parameters.
     */
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolationException(
            ConstraintViolationException ex, WebRequest request) {

        Map<String, String> violations = new HashMap<>();
        Set<ConstraintViolation<?>> constraintViolations = ex.getConstraintViolations();

        for (ConstraintViolation<?> violation : constraintViolations) {
            String propertyPath = violation.getPropertyPath().toString();
            String message = violation.getMessage();
            violations.put(propertyPath, message);
        }

        log.warn("Constraint violation: {}", violations);

        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message("Constraint violation")
                .errorCode("CONSTRAINT_VIOLATION")
                .path(request.getDescription(false).replace("uri=", ""))
                .context(Map.of("violations", violations))
                .build();

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    /**
     * Handle all other exceptions.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex, WebRequest request) {
        log.error("Unexpected error occurred", ex);

        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                .error(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase())
                .message("An unexpected error occurred")
                .errorCode("INTERNAL_ERROR")
                .path(request.getDescription(false).replace("uri=", ""))
                .build();

        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}

// src/main/java/com/example/common/exception/ErrorResponse.java
package com.example.common.exception;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Standard error response format for all API errors.
 */
@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {

    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String errorCode;
    private String path;
    private Map<String, Object> context;
}
```

## Retry and Circuit Breaker Patterns

### Retry Configuration

```java
// src/main/java/com/example/common/config/ResilienceConfig.java
package com.example.common.config;

import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import io.github.resilience4j.retry.RetryRegistry;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;

/**
 * Configuration for resilience patterns (retry, circuit breaker, etc.).
 */
@Configuration
public class ResilienceConfig {

    @Bean
    public RetryRegistry retryRegistry() {
        return RetryRegistry.ofDefaults();
    }

    @Bean
    public Retry externalServiceRetry() {
        RetryConfig config = RetryConfig.custom()
                .maxAttempts(3)
                .waitDuration(Duration.ofMillis(100))
                .retryOnException(throwable ->
                    throwable instanceof ExternalServiceException ||
                    throwable instanceof java.net.SocketTimeoutException ||
                    throwable instanceof java.io.IOException)
                .build();

        return Retry.of("externalServiceRetry", config);
    }

    @Bean
    public Retry databaseRetry() {
        RetryConfig config = RetryConfig.custom()
                .maxAttempts(2)
                .waitDuration(Duration.ofMillis(50))
                .retryOnException(throwable ->
                    throwable.getMessage().contains("connection") ||
                    throwable.getMessage().contains("timeout"))
                .build();

        return Retry.of("databaseRetry", config);
    }
}
```

### Circuit Breaker Configuration

```java
// src/main/java/com/example/common/config/CircuitBreakerConfig.java
package com.example.common.config;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;

/**
 * Circuit breaker configuration for external service calls.
 */
@Configuration
public class CircuitBreakerConfig {

    @Bean
    public CircuitBreakerRegistry circuitBreakerRegistry() {
        return CircuitBreakerRegistry.ofDefaults();
    }

    @Bean
    public CircuitBreaker externalServiceCircuitBreaker() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
                .failureRateThreshold(50) // Open circuit if 50% of calls fail
                .waitDurationInOpenState(Duration.ofMillis(1000)) // Wait 1 second in open state
                .slidingWindowSize(10) // Consider last 10 calls
                .permittedNumberOfCallsInHalfOpenState(3) // Allow 3 calls in half-open state
                .automaticTransitionFromOpenToHalfOpenEnabled(true)
                .build();

        return CircuitBreaker.of("externalServiceCircuitBreaker", config);
    }
}
```

### Service with Retry and Circuit Breaker

```java
// src/main/java/com/example/user/service/EmailService.java
package com.example.user.service;

import com.example.common.exception.ExternalServiceException;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.retry.Retry;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.function.Supplier;

/**
 * Email service with retry and circuit breaker patterns.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class EmailService {

    private final CircuitBreaker circuitBreaker;
    private final Retry retry;

    /**
     * Send welcome email with retry and circuit breaker protection.
     */
    public void sendWelcomeEmail(String email, String name) {
        Supplier<Void> emailSupplier = () -> {
            try {
                // Simulate external API call
                callExternalEmailService(email, "Welcome " + name);
                log.info("Welcome email sent to {}", email);
                return null;
            } catch (Exception e) {
                log.error("Failed to send welcome email to {}: {}", email, e.getMessage());
                throw new ExternalServiceException("EmailService", "sendWelcomeEmail", e);
            }
        };

        // Apply circuit breaker and retry
        Supplier<Void> decoratedSupplier = CircuitBreaker
                .decorateSupplier(circuitBreaker, emailSupplier);

        decoratedSupplier = Retry
                .decorateSupplier(retry, decoratedSupplier);

        try {
            decoratedSupplier.get();
        } catch (Exception e) {
            log.error("Failed to send welcome email after retries: {}", e.getMessage());
            // Don't rethrow - email failure shouldn't break user registration
        }
    }

    /**
     * Send password reset email.
     */
    public void sendPasswordResetEmail(String email, String resetToken) {
        Supplier<Void> emailSupplier = () -> {
            try {
                callExternalEmailService(email, "Password reset token: " + resetToken);
                log.info("Password reset email sent to {}", email);
                return null;
            } catch (Exception e) {
                log.error("Failed to send password reset email to {}: {}", email, e.getMessage());
                throw new ExternalServiceException("EmailService", "sendPasswordResetEmail", e);
            }
        };

        // Apply circuit breaker and retry
        Supplier<Void> decoratedSupplier = CircuitBreaker
                .decorateSupplier(circuitBreaker, emailSupplier);

        decoratedSupplier = Retry
                .decorateSupplier(retry, decoratedSupplier);

        decoratedSupplier.get(); // This will throw if all retries fail
    }

    private void callExternalEmailService(String email, String content) throws Exception {
        // Simulate external service call that might fail
        if (Math.random() < 0.1) { // 10% failure rate
            throw new RuntimeException("External email service unavailable");
        }

        // Simulate network delay
        Thread.sleep(100);
    }
}
```

## Error Handling in Services

### Service Layer Error Handling

```java
// src/main/java/com/example/user/service/UserService.java
package com.example.user.service;

import com.example.common.exception.SystemException;
import com.example.user.exception.UserAlreadyExistsException;
import com.example.user.exception.UserNotFoundException;
import com.example.user.exception.InvalidCredentialsException;
import com.example.user.model.User;
import com.example.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * User service with comprehensive error handling.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final EmailService emailService;

    /**
     * Create a new user with validation and error handling.
     */
    @Transactional
    public User createUser(String name, String email, String password) {
        log.info("Creating user with email: {}", email);

        try {
            // Validate input
            validateUserData(name, email, password);

            // Check if user already exists
            if (userRepository.existsByEmail(email)) {
                log.warn("Attempted to create user with existing email: {}", email);
                throw new UserAlreadyExistsException(email);
            }

            // Create user
            User user = User.builder()
                    .name(name)
                    .email(email)
                    .password(passwordEncoder.encode(password))
                    .active(true)
                    .build();

            User savedUser = userRepository.save(user);
            log.info("User created successfully with id: {}", savedUser.getId());

            // Send welcome email (async, don't fail the operation)
            try {
                emailService.sendWelcomeEmail(email, name);
            } catch (Exception e) {
                log.error("Failed to send welcome email to {}: {}", email, e.getMessage());
                // Don't throw - user creation was successful
            }

            return savedUser;

        } catch (DataIntegrityViolationException e) {
            log.error("Database constraint violation while creating user: {}", e.getMessage());
            throw new SystemException("Failed to create user due to data constraint violation", e);
        } catch (Exception e) {
            log.error("Unexpected error while creating user: {}", e.getMessage(), e);
            throw new SystemException("Failed to create user", e);
        }
    }

    /**
     * Authenticate user with proper error handling.
     */
    public User authenticateUser(String email, String password) {
        log.debug("Authenticating user with email: {}", email);

        try {
            Optional<User> userOpt = userRepository.findByEmail(email);

            if (userOpt.isEmpty()) {
                log.warn("Authentication failed: user not found for email: {}", email);
                throw new InvalidCredentialsException();
            }

            User user = userOpt.get();

            if (!passwordEncoder.matches(password, user.getPassword())) {
                log.warn("Authentication failed: invalid password for email: {}", email);
                throw new InvalidCredentialsException();
            }

            if (!user.isActive()) {
                log.warn("Authentication failed: inactive user for email: {}", email);
                throw new InvalidCredentialsException();
            }

            log.info("User authenticated successfully: {}", email);
            return user;

        } catch (InvalidCredentialsException e) {
            throw e; // Re-throw as-is
        } catch (Exception e) {
            log.error("Unexpected error during authentication: {}", e.getMessage(), e);
            throw new SystemException("Authentication failed due to system error", e);
        }
    }

    /**
     * Get user by ID with error handling.
     */
    public User getUserById(String userId) {
        log.debug("Getting user by id: {}", userId);

        try {
            return userRepository.findById(userId)
                    .orElseThrow(() -> new UserNotFoundException(userId));
        } catch (UserNotFoundException e) {
            throw e; // Re-throw as-is
        } catch (Exception e) {
            log.error("Error retrieving user {}: {}", userId, e.getMessage(), e);
            throw new SystemException("Failed to retrieve user", e);
        }
    }

    /**
     * Get all users with pagination and error handling.
     */
    public List<User> getAllUsers(int page, int size) {
        log.debug("Getting users page: {}, size: {}", page, size);

        try {
            // Validate pagination parameters
            if (page < 0) {
                throw new IllegalArgumentException("Page number cannot be negative");
            }
            if (size <= 0 || size > 100) {
                throw new IllegalArgumentException("Page size must be between 1 and 100");
            }

            return userRepository.findAll(PageRequest.of(page, size)).getContent();

        } catch (IllegalArgumentException e) {
            log.warn("Invalid pagination parameters: page={}, size={}", page, size);
            throw new ValidationException("Invalid pagination parameters: " + e.getMessage());
        } catch (Exception e) {
            log.error("Error retrieving users: {}", e.getMessage(), e);
            throw new SystemException("Failed to retrieve users", e);
        }
    }

    /**
     * Update user with optimistic locking and error handling.
     */
    @Transactional
    public User updateUser(String userId, String name, String email) {
        log.info("Updating user {}: name={}, email={}", userId, name, email);

        try {
            User user = getUserById(userId); // This will throw if not found

            // Check if email change conflicts with existing user
            if (!user.getEmail().equals(email) && userRepository.existsByEmail(email)) {
                throw new UserAlreadyExistsException(email);
            }

            user.setName(name);
            user.setEmail(email);

            User savedUser = userRepository.save(user);
            log.info("User updated successfully: {}", userId);

            return savedUser;

        } catch (UserNotFoundException | UserAlreadyExistsException e) {
            throw e; // Re-throw domain exceptions
        } catch (DataIntegrityViolationException e) {
            log.error("Database constraint violation while updating user {}: {}", userId, e.getMessage());
            throw new SystemException("Failed to update user due to data constraint violation", e);
        } catch (Exception e) {
            log.error("Unexpected error while updating user {}: {}", userId, e.getMessage(), e);
            throw new SystemException("Failed to update user", e);
        }
    }

    /**
     * Delete user with proper error handling.
     */
    @Transactional
    public void deleteUser(String userId) {
        log.info("Deleting user: {}", userId);

        try {
            User user = getUserById(userId); // This will throw if not found

            userRepository.delete(user);
            log.info("User deleted successfully: {}", userId);

        } catch (UserNotFoundException e) {
            throw e; // Re-throw as-is
        } catch (DataIntegrityViolationException e) {
            log.error("Cannot delete user {} due to data constraints: {}", userId, e.getMessage());
            throw new BusinessException("Cannot delete user due to existing references");
        } catch (Exception e) {
            log.error("Unexpected error while deleting user {}: {}", userId, e.getMessage(), e);
            throw new SystemException("Failed to delete user", e);
        }
    }

    private void validateUserData(String name, String email, String password) {
        if (name == null || name.trim().isEmpty()) {
            throw new ValidationException("Name is required");
        }
        if (name.length() > 100) {
            throw new ValidationException("Name must be less than 100 characters");
        }

        if (email == null || email.trim().isEmpty()) {
            throw new ValidationException("Email is required");
        }
        if (!email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$")) {
            throw new ValidationException("Invalid email format");
        }

        if (password == null || password.length() < 8) {
            throw new ValidationException("Password must be at least 8 characters long");
        }
    }
}
```

## Async Error Handling

### Async Error Handling with CompletableFuture

```java
// src/main/java/com/example/common/exception/AsyncExceptionHandler.java
package com.example.common.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import java.util.concurrent.CompletableFuture;
import java.util.function.Supplier;

/**
 * Utility class for handling errors in async operations.
 */
@Slf4j
@Component
public class AsyncExceptionHandler {

    /**
     * Execute async operation with error handling.
     */
    @Async
    public <T> CompletableFuture<T> executeAsync(Supplier<T> operation, String operationName) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                log.debug("Starting async operation: {}", operationName);
                T result = operation.get();
                log.debug("Completed async operation: {}", operationName);
                return result;
            } catch (Exception e) {
                log.error("Async operation '{}' failed: {}", operationName, e.getMessage(), e);
                throw new CompletionException(
                    new SystemException("Async operation '" + operationName + "' failed", e));
            }
        });
    }

    /**
     * Execute async operation that doesn't return a value.
     */
    @Async
    public CompletableFuture<Void> executeAsyncRunnable(Runnable operation, String operationName) {
        return CompletableFuture.runAsync(() -> {
            try {
                log.debug("Starting async runnable: {}", operationName);
                operation.run();
                log.debug("Completed async runnable: {}", operationName);
            } catch (Exception e) {
                log.error("Async runnable '{}' failed: {}", operationName, e.getMessage(), e);
                throw new CompletionException(
                    new SystemException("Async runnable '" + operationName + "' failed", e));
            }
        });
    }
}
```

### Service with Async Error Handling

```java
// src/main/java/com/example/user/service/NotificationService.java
package com.example.user.service;

import com.example.common.exception.AsyncExceptionHandler;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * Notification service with async error handling.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationService {

    private final EmailService emailService;
    private final AsyncExceptionHandler asyncExceptionHandler;

    /**
     * Send bulk notifications asynchronously with error handling.
     */
    public CompletableFuture<Void> sendBulkNotifications(List<String> emails, String message) {
        log.info("Sending bulk notifications to {} recipients", emails.size());

        // Create individual notification tasks
        List<CompletableFuture<Void>> notificationTasks = emails.stream()
                .map(email -> asyncExceptionHandler.executeAsyncRunnable(
                    () -> emailService.sendWelcomeEmail(email, message),
                    "sendNotification:" + email))
                .toList();

        // Wait for all notifications to complete, but don't fail if some individual ones fail
        return CompletableFuture.allOf(notificationTasks.toArray(new CompletableFuture[0]))
                .thenRun(() -> log.info("Bulk notification sending completed"))
                .exceptionally(throwable -> {
                    log.error("Some notifications failed during bulk send", throwable);
                    return null; // Don't propagate the error
                });
    }

    /**
     * Send critical notification that must succeed.
     */
    public void sendCriticalNotification(String email, String subject, String message) {
        try {
            asyncExceptionHandler.executeAsyncRunnable(
                () -> emailService.sendPasswordResetEmail(email, message),
                "sendCriticalNotification:" + email)
                .get(); // Wait for completion and re-throw any exceptions
        } catch (Exception e) {
            log.error("Critical notification failed for {}: {}", email, e.getMessage());
            throw new RuntimeException("Failed to send critical notification", e);
        }
    }
}
```

## Testing Error Handling

### Unit Tests for Exception Handling

```java
// src/test/java/com/example/user/service/UserServiceTest.java
package com.example.user.service;

import com.example.common.exception.SystemException;
import com.example.user.exception.UserAlreadyExistsException;
import com.example.user.exception.UserNotFoundException;
import com.example.user.exception.InvalidCredentialsException;
import com.example.user.model.User;
import com.example.user.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserService userService;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .id("user123")
                .name("John Doe")
                .email("john@example.com")
                .password("hashedPassword")
                .active(true)
                .build();
    }

    @Test
    void createUser_shouldCreateUserSuccessfully() {
        // Given
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(passwordEncoder.encode(anyString())).thenReturn("hashedPassword");
        when(userRepository.save(any(User.class))).thenReturn(testUser);
        doNothing().when(emailService).sendWelcomeEmail(anyString(), anyString());

        // When
        User result = userService.createUser("John Doe", "john@example.com", "password123");

        // Then
        assertThat(result).isEqualTo(testUser);
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail("john@example.com", "John Doe");
    }

    @Test
    void createUser_shouldThrowUserAlreadyExistsException_whenEmailExists() {
        // Given
        when(userRepository.existsByEmail("john@example.com")).thenReturn(true);

        // When & Then
        assertThatThrownBy(() ->
            userService.createUser("John Doe", "john@example.com", "password123"))
            .isInstanceOf(UserAlreadyExistsException.class)
            .hasMessage("User with email 'john@example.com' already exists");

        verify(userRepository, never()).save(any(User.class));
        verify(emailService, never()).sendWelcomeEmail(anyString(), anyString());
    }

    @Test
    void createUser_shouldThrowSystemException_whenDatabaseErrorOccurs() {
        // Given
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(passwordEncoder.encode(anyString())).thenReturn("hashedPassword");
        when(userRepository.save(any(User.class)))
            .thenThrow(new DataIntegrityViolationException("Constraint violation"));

        // When & Then
        assertThatThrownBy(() ->
            userService.createUser("John Doe", "john@example.com", "password123"))
            .isInstanceOf(SystemException.class)
            .hasMessage("Failed to create user due to data constraint violation");

        verify(emailService, never()).sendWelcomeEmail(anyString(), anyString());
    }

    @Test
    void createUser_shouldNotFail_whenEmailServiceFails() {
        // Given
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(passwordEncoder.encode(anyString())).thenReturn("hashedPassword");
        when(userRepository.save(any(User.class))).thenReturn(testUser);
        doThrow(new RuntimeException("Email service down"))
            .when(emailService).sendWelcomeEmail(anyString(), anyString());

        // When
        User result = userService.createUser("John Doe", "john@example.com", "password123");

        // Then
        assertThat(result).isEqualTo(testUser);
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail("john@example.com", "John Doe");
    }

    @Test
    void authenticateUser_shouldReturnUser_whenCredentialsAreValid() {
        // Given
        when(userRepository.findByEmail("john@example.com")).thenReturn(Optional.of(testUser));
        when(passwordEncoder.matches("password123", "hashedPassword")).thenReturn(true);

        // When
        User result = userService.authenticateUser("john@example.com", "password123");

        // Then
        assertThat(result).isEqualTo(testUser);
    }

    @Test
    void authenticateUser_shouldThrowInvalidCredentialsException_whenUserNotFound() {
        // Given
        when(userRepository.findByEmail("unknown@example.com")).thenReturn(Optional.empty());

        // When & Then
        assertThatThrownBy(() ->
            userService.authenticateUser("unknown@example.com", "password123"))
            .isInstanceOf(InvalidCredentialsException.class);
    }

    @Test
    void authenticateUser_shouldThrowInvalidCredentialsException_whenPasswordInvalid() {
        // Given
        when(userRepository.findByEmail("john@example.com")).thenReturn(Optional.of(testUser));
        when(passwordEncoder.matches("wrongpassword", "hashedPassword")).thenReturn(false);

        // When & Then
        assertThatThrownBy(() ->
            userService.authenticateUser("john@example.com", "wrongpassword"))
            .isInstanceOf(InvalidCredentialsException.class);
    }

    @Test
    void getUserById_shouldReturnUser_whenUserExists() {
        // Given
        when(userRepository.findById("user123")).thenReturn(Optional.of(testUser));

        // When
        User result = userService.getUserById("user123");

        // Then
        assertThat(result).isEqualTo(testUser);
    }

    @Test
    void getUserById_shouldThrowUserNotFoundException_whenUserDoesNotExist() {
        // Given
        when(userRepository.findById("nonexistent")).thenReturn(Optional.empty());

        // When & Then
        assertThatThrownBy(() -> userService.getUserById("nonexistent"))
            .isInstanceOf(UserNotFoundException.class)
            .hasMessage("User with id 'nonexistent' not found");
    }

    @Test
    void updateUser_shouldUpdateUserSuccessfully() {
        // Given
        when(userRepository.findById("user123")).thenReturn(Optional.of(testUser));
        when(userRepository.existsByEmail("newemail@example.com")).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(testUser);

        // When
        User result = userService.updateUser("user123", "Jane Doe", "newemail@example.com");

        // Then
        assertThat(result).isEqualTo(testUser);
        verify(userRepository).save(testUser);
    }

    @Test
    void deleteUser_shouldDeleteUserSuccessfully() {
        // Given
        when(userRepository.findById("user123")).thenReturn(Optional.of(testUser));
        doNothing().when(userRepository).delete(testUser);

        // When
        userService.deleteUser("user123");

        // Then
        verify(userRepository).delete(testUser);
    }

    @Test
    void deleteUser_shouldThrowUserNotFoundException_whenUserDoesNotExist() {
        // Given
        when(userRepository.findById("nonexistent")).thenReturn(Optional.empty());

        // When & Then
        assertThatThrownBy(() -> userService.deleteUser("nonexistent"))
            .isInstanceOf(UserNotFoundException.class);
    }
}
```

### Integration Tests for Error Handling

```java
// src/test/java/com/example/user/controller/UserControllerIntegrationTest.java
package com.example.user.controller;

import com.example.common.exception.ErrorResponse;
import com.example.user.model.User;
import com.example.user.repository.UserRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureWebMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@AutoConfigureWebMvc
@Transactional
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ObjectMapper objectMapper;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .name("John Doe")
                .email("john@example.com")
                .password("hashedPassword")
                .active(true)
                .build();
    }

    @Test
    void createUser_shouldReturn201_whenUserCreatedSuccessfully() throws Exception {
        // Given
        String requestBody = """
            {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123"
            }
            """;

        // When & Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(requestBody))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("John Doe"))
                .andExpect(jsonPath("$.email").value("john@example.com"));
    }

    @Test
    void createUser_shouldReturn400_whenValidationFails() throws Exception {
        // Given
        String requestBody = """
            {
                "name": "",
                "email": "invalid-email",
                "password": "123"
            }
            """;

        // When & Then
        String responseBody = mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(requestBody))
                .andExpect(status().isBadRequest())
                .andReturn()
                .getResponse()
                .getContentAsString();

        ErrorResponse errorResponse = objectMapper.readValue(responseBody, ErrorResponse.class);
        assertThat(errorResponse.getErrorCode()).isEqualTo("VALIDATION_ERROR");
        assertThat(errorResponse.getMessage()).isEqualTo("Validation failed");
    }

    @Test
    void getUser_shouldReturn404_whenUserNotFound() throws Exception {
        // When & Then
        String responseBody = mockMvc.perform(get("/api/users/nonexistent"))
                .andExpect(status().isNotFound())
                .andReturn()
                .getResponse()
                .getContentAsString();

        ErrorResponse errorResponse = objectMapper.readValue(responseBody, ErrorResponse.class);
        assertThat(errorResponse.getErrorCode()).isEqualTo("USER_NOT_FOUND");
        assertThat(errorResponse.getMessage()).isEqualTo("User with id 'nonexistent' not found");
    }

    @Test
    void updateUser_shouldReturn404_whenUserNotFound() throws Exception {
        // Given
        String requestBody = """
            {
                "name": "Jane Doe",
                "email": "jane@example.com"
            }
            """;

        // When & Then
        String responseBody = mockMvc.perform(put("/api/users/nonexistent")
                .contentType(MediaType.APPLICATION_JSON)
                .content(requestBody))
                .andExpect(status().isNotFound())
                .andReturn()
                .getResponse()
                .getContentAsString();

        ErrorResponse errorResponse = objectMapper.readValue(responseBody, ErrorResponse.class);
        assertThat(errorResponse.getErrorCode()).isEqualTo("USER_NOT_FOUND");
    }

    @Test
    void deleteUser_shouldReturn404_whenUserNotFound() throws Exception {
        // When & Then
        String responseBody = mockMvc.perform(delete("/api/users/nonexistent"))
                .andExpect(status().isNotFound())
                .andReturn()
                .getResponse()
                .getContentAsString();

        ErrorResponse errorResponse = objectMapper.readValue(responseBody, ErrorResponse.class);
        assertThat(errorResponse.getErrorCode()).isEqualTo("USER_NOT_FOUND");
    }
}
```

This comprehensive guide covers error handling patterns for Java applications, including custom exceptions, global exception handlers, retry and circuit breaker patterns, service layer error handling, async error handling, and comprehensive testing strategies.