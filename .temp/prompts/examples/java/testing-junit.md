# JUnit Testing Patterns for Java/Spring Boot

This guide covers comprehensive testing patterns using JUnit 5 for Java and Spring Boot applications, including unit tests, integration tests, mocking strategies, and best practices.

## Project Setup and Configuration

### Maven Dependencies

```xml
<!-- pom.xml -->
<dependencies>
    <!-- JUnit 5 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.9.2</version>
        <scope>test</scope>
    </dependency>

    <!-- Spring Boot Test -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

    <!-- Mockito for mocking -->
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.1.1</version>
        <scope>test</scope>
    </dependency>

    <!-- AssertJ for fluent assertions -->
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>3.24.2</version>
        <scope>test</scope>
    </dependency>

    <!-- Testcontainers for integration tests -->
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>1.17.6</version>
        <scope>test</scope>
    </dependency>

    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>postgresql</artifactId>
        <version>1.17.6</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0</version>
            <configuration>
                <includes>
                    <include>**/*Test.java</include>
                    <include>**/*Tests.java</include>
                </includes>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### Test Configuration

```java
// src/test/java/com/example/demo/TestConfig.java
package com.example.demo;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@TestConfiguration
public class TestConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}

// src/test/java/com/example/demo/BaseTest.java
package com.example.demo;

import org.junit.jupiter.api.BeforeEach;
import org.springframework.test.context.ActiveProfiles;

@ActiveProfiles("test")
public abstract class BaseTest {

    @BeforeEach
    void setUp() {
        // Common setup for all tests
    }
}

// src/test/resources/application-test.yml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:

  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.H2Dialect

  h2:
    console:
      enabled: true

logging:
  level:
    com.example.demo: DEBUG
    org.springframework.security: DEBUG
```

## Unit Testing Patterns

### Testing Utility Classes

```java
// src/main/java/com/example/demo/utils/StringUtils.java
package com.example.demo.utils;

public class StringUtils {

    public static String capitalize(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        return str.substring(0, 1).toUpperCase() + str.substring(1).toLowerCase();
    }

    public static String truncate(String str, int maxLength) {
        if (str == null || str.length() <= maxLength) {
            return str;
        }
        return str.substring(0, maxLength - 3) + "...";
    }

    public static String slugify(String str) {
        if (str == null) {
            return null;
        }
        return str.toLowerCase()
                  .trim()
                  .replaceAll("[^a-z0-9\\s-]", "")
                  .replaceAll("\\s+", "-")
                  .replaceAll("-+", "-")
                  .replaceAll("^-|-$", "");
    }

    public static boolean isPalindrome(String str) {
        if (str == null) {
            return false;
        }
        String clean = str.replaceAll("[^a-zA-Z0-9]", "").toLowerCase();
        String reversed = new StringBuilder(clean).reverse().toString();
        return clean.equals(reversed);
    }
}

// src/test/java/com/example/demo/utils/StringUtilsTest.java
package com.example.demo.utils;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.assertj.core.api.Assertions.*;

@DisplayName("StringUtils Unit Tests")
class StringUtilsTest {

    @Nested
    @DisplayName("capitalize method")
    class CapitalizeTests {

        @Test
        @DisplayName("should capitalize first letter and lowercase rest")
        void shouldCapitalizeFirstLetter() {
            assertThat(StringUtils.capitalize("hello")).isEqualTo("Hello");
            assertThat(StringUtils.capitalize("HELLO")).isEqualTo("Hello");
            assertThat(StringUtils.capitalize("hELLO")).isEqualTo("Hello");
        }

        @ParameterizedTest
        @NullAndEmptySource
        @ValueSource(strings = {"", " ", "\t", "\n"})
        @DisplayName("should handle null and empty strings")
        void shouldHandleNullAndEmptyStrings(String input) {
            assertThat(StringUtils.capitalize(input)).isEqualTo(input);
        }

        @Test
        @DisplayName("should handle single character strings")
        void shouldHandleSingleCharacter() {
            assertThat(StringUtils.capitalize("a")).isEqualTo("A");
            assertThat(StringUtils.capitalize("A")).isEqualTo("A");
        }
    }

    @Nested
    @DisplayName("truncate method")
    class TruncateTests {

        @Test
        @DisplayName("should not truncate strings shorter than maxLength")
        void shouldNotTruncateShortStrings() {
            assertThat(StringUtils.truncate("hello", 10)).isEqualTo("hello");
            assertThat(StringUtils.truncate("hello", 5)).isEqualTo("hello");
        }

        @Test
        @DisplayName("should truncate strings longer than maxLength")
        void shouldTruncateLongStrings() {
            assertThat(StringUtils.truncate("hello world", 8)).isEqualTo("hello...");
            assertThat(StringUtils.truncate("this is a very long string", 10)).isEqualTo("this is...");
        }

        @ParameterizedTest
        @CsvSource({
            "'', 5, ''",
            "'hello', 5, 'hello'",
            "'hello', 3, 'h...'",
            "'a', 1, 'a'"
        })
        @DisplayName("should handle various truncation scenarios")
        void shouldHandleVariousScenarios(String input, int maxLength, String expected) {
            assertThat(StringUtils.truncate(input, maxLength)).isEqualTo(expected);
        }

        @Test
        @DisplayName("should handle null input")
        void shouldHandleNullInput() {
            assertThat(StringUtils.truncate(null, 5)).isNull();
        }
    }

    @Nested
    @DisplayName("slugify method")
    class SlugifyTests {

        @ParameterizedTest
        @CsvSource({
            "'Hello World', 'hello-world'",
            "'This is a TEST!', 'this-is-a-test'",
            "'Multiple   Spaces', 'multiple-spaces'",
            "'Café & Restaurant', 'cafe-restaurant'"
        })
        @DisplayName("should convert strings to URL-friendly slugs")
        void shouldCreateSlugs(String input, String expected) {
            assertThat(StringUtils.slugify(input)).isEqualTo(expected);
        }

        @Test
        @DisplayName("should handle special characters")
        void shouldHandleSpecialCharacters() {
            assertThat(StringUtils.slugify("Hello@World!")).isEqualTo("helloworld");
            assertThat(StringUtils.slugify("Test#123")).isEqualTo("test123");
        }

        @ParameterizedTest
        @NullAndEmptySource
        @DisplayName("should handle null and empty strings")
        void shouldHandleNullAndEmpty(String input) {
            assertThat(StringUtils.slugify(input)).isEqualTo(input);
        }

        @Test
        @DisplayName("should remove leading and trailing hyphens")
        void shouldRemoveLeadingTrailingHyphens() {
            assertThat(StringUtils.slugify("-hello-")).isEqualTo("hello");
            assertThat(StringUtils.slugify("---hello---")).isEqualTo("hello");
        }
    }

    @Nested
    @DisplayName("isPalindrome method")
    class IsPalindromeTests {

        @ParameterizedTest
        @ValueSource(strings = {"radar", "level", "A man a plan a canal Panama", "12321"})
        @DisplayName("should return true for palindromes")
        void shouldReturnTrueForPalindromes(String input) {
            assertThat(StringUtils.isPalindrome(input)).isTrue();
        }

        @ParameterizedTest
        @ValueSource(strings = {"hello", "world", "not a palindrome"})
        @DisplayName("should return false for non-palindromes")
        void shouldReturnFalseForNonPalindromes(String input) {
            assertThat(StringUtils.isPalindrome(input)).isFalse();
        }

        @Test
        @DisplayName("should ignore case and special characters")
        void shouldIgnoreCaseAndSpecialChars() {
            assertThat(StringUtils.isPalindrome("A man, a plan, a canal: Panama")).isTrue();
            assertThat(StringUtils.isPalindrome("Race car")).isTrue();
        }

        @Test
        @DisplayName("should return false for null input")
        void shouldReturnFalseForNull() {
            assertThat(StringUtils.isPalindrome(null)).isFalse();
        }

        @ParameterizedTest
        @ValueSource(strings = {"", "a", "aa", "aba"})
        @DisplayName("should handle edge cases")
        void shouldHandleEdgeCases(String input) {
            boolean expected = input != null && input.length() > 0;
            assertThat(StringUtils.isPalindrome(input)).isEqualTo(expected);
        }
    }
}
```

### Testing Services with Mockito

```java
// src/main/java/com/example/demo/service/UserService.java
package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.entity.UserRole;
import com.example.demo.repository.UserRepository;
import com.example.demo.dto.UserDTO;
import com.example.demo.exception.UserNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Transactional(readOnly = true)
    public UserDTO getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + id));
        return convertToDTO(user);
    }

    @Transactional(readOnly = true)
    public List<UserDTO> getAllUsers() {
        return userRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public UserDTO createUser(String name, String email, String password) {
        User user = new User();
        user.setName(name);
        user.setEmail(email);
        user.setPassword(password); // In real app, this would be hashed
        user.setRole(UserRole.USER);

        User savedUser = userRepository.save(user);
        return convertToDTO(savedUser);
    }

    @Transactional
    public UserDTO updateUser(Long id, String name, String email) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + id));

        user.setName(name);
        user.setEmail(email);

        User updatedUser = userRepository.save(user);
        return convertToDTO(updatedUser);
    }

    @Transactional
    public void deleteUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + id));
        userRepository.delete(user);
    }

    private UserDTO convertToDTO(User user) {
        UserDTO dto = new UserDTO();
        dto.setId(user.getId());
        dto.setName(user.getName());
        dto.setEmail(user.getEmail());
        dto.setRole(user.getRole());
        return dto;
    }
}

// src/test/java/com/example/demo/service/UserServiceTest.java
package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.entity.UserRole;
import com.example.demo.repository.UserRepository;
import com.example.demo.dto.UserDTO;
import com.example.demo.exception.UserNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserService Unit Tests")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = new User();
        testUser.setId(1L);
        testUser.setName("John Doe");
        testUser.setEmail("john@example.com");
        testUser.setPassword("password123");
        testUser.setRole(UserRole.USER);
    }

    @Nested
    @DisplayName("getUserById method")
    class GetUserByIdTests {

        @Test
        @DisplayName("should return user DTO when user exists")
        void shouldReturnUserWhenExists() {
            // Arrange
            when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));

            // Act
            UserDTO result = userService.getUserById(1L);

            // Assert
            assertThat(result).isNotNull();
            assertThat(result.getId()).isEqualTo(1L);
            assertThat(result.getName()).isEqualTo("John Doe");
            assertThat(result.getEmail()).isEqualTo("john@example.com");
            assertThat(result.getRole()).isEqualTo(UserRole.USER);

            verify(userRepository).findById(1L);
        }

        @Test
        @DisplayName("should throw UserNotFoundException when user does not exist")
        void shouldThrowExceptionWhenUserNotFound() {
            // Arrange
            when(userRepository.findById(999L)).thenReturn(Optional.empty());

            // Act & Assert
            assertThatThrownBy(() -> userService.getUserById(999L))
                    .isInstanceOf(UserNotFoundException.class)
                    .hasMessage("User not found with id: 999");

            verify(userRepository).findById(999L);
        }
    }

    @Nested
    @DisplayName("getAllUsers method")
    class GetAllUsersTests {

        @Test
        @DisplayName("should return list of user DTOs")
        void shouldReturnAllUsers() {
            // Arrange
            User user2 = new User();
            user2.setId(2L);
            user2.setName("Jane Doe");
            user2.setEmail("jane@example.com");
            user2.setPassword("password456");
            user2.setRole(UserRole.ADMIN);

            when(userRepository.findAll()).thenReturn(Arrays.asList(testUser, user2));

            // Act
            List<UserDTO> result = userService.getAllUsers();

            // Assert
            assertThat(result).hasSize(2);

            UserDTO firstUser = result.get(0);
            assertThat(firstUser.getId()).isEqualTo(1L);
            assertThat(firstUser.getName()).isEqualTo("John Doe");

            UserDTO secondUser = result.get(1);
            assertThat(secondUser.getId()).isEqualTo(2L);
            assertThat(secondUser.getName()).isEqualTo("Jane Doe");

            verify(userRepository).findAll();
        }

        @Test
        @DisplayName("should return empty list when no users exist")
        void shouldReturnEmptyListWhenNoUsers() {
            // Arrange
            when(userRepository.findAll()).thenReturn(Arrays.asList());

            // Act
            List<UserDTO> result = userService.getAllUsers();

            // Assert
            assertThat(result).isEmpty();
            verify(userRepository).findAll();
        }
    }

    @Nested
    @DisplayName("createUser method")
    class CreateUserTests {

        @Test
        @DisplayName("should create and return new user")
        void shouldCreateUser() {
            // Arrange
            User savedUser = new User();
            savedUser.setId(1L);
            savedUser.setName("John Doe");
            savedUser.setEmail("john@example.com");
            savedUser.setPassword("password123");
            savedUser.setRole(UserRole.USER);

            when(userRepository.save(any(User.class))).thenReturn(savedUser);

            // Act
            UserDTO result = userService.createUser("John Doe", "john@example.com", "password123");

            // Assert
            assertThat(result).isNotNull();
            assertThat(result.getId()).isEqualTo(1L);
            assertThat(result.getName()).isEqualTo("John Doe");
            assertThat(result.getEmail()).isEqualTo("john@example.com");
            assertThat(result.getRole()).isEqualTo(UserRole.USER);

            verify(userRepository).save(argThat(user ->
                user.getName().equals("John Doe") &&
                user.getEmail().equals("john@example.com") &&
                user.getPassword().equals("password123") &&
                user.getRole().equals(UserRole.USER)
            ));
        }
    }

    @Nested
    @DisplayName("updateUser method")
    class UpdateUserTests {

        @Test
        @DisplayName("should update and return updated user")
        void shouldUpdateUser() {
            // Arrange
            when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));

            User updatedUser = new User();
            updatedUser.setId(1L);
            updatedUser.setName("John Smith");
            updatedUser.setEmail("johnsmith@example.com");
            updatedUser.setPassword("password123");
            updatedUser.setRole(UserRole.USER);

            when(userRepository.save(any(User.class))).thenReturn(updatedUser);

            // Act
            UserDTO result = userService.updateUser(1L, "John Smith", "johnsmith@example.com");

            // Assert
            assertThat(result).isNotNull();
            assertThat(result.getId()).isEqualTo(1L);
            assertThat(result.getName()).isEqualTo("John Smith");
            assertThat(result.getEmail()).isEqualTo("johnsmith@example.com");

            verify(userRepository).findById(1L);
            verify(userRepository).save(argThat(user ->
                user.getName().equals("John Smith") &&
                user.getEmail().equals("johnsmith@example.com")
            ));
        }

        @Test
        @DisplayName("should throw exception when updating non-existent user")
        void shouldThrowExceptionWhenUpdatingNonExistentUser() {
            // Arrange
            when(userRepository.findById(999L)).thenReturn(Optional.empty());

            // Act & Assert
            assertThatThrownBy(() -> userService.updateUser(999L, "New Name", "new@example.com"))
                    .isInstanceOf(UserNotFoundException.class)
                    .hasMessage("User not found with id: 999");

            verify(userRepository).findById(999L);
            verify(userRepository, never()).save(any(User.class));
        }
    }

    @Nested
    @DisplayName("deleteUser method")
    class DeleteUserTests {

        @Test
        @DisplayName("should delete existing user")
        void shouldDeleteUser() {
            // Arrange
            when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));

            // Act
            userService.deleteUser(1L);

            // Assert
            verify(userRepository).findById(1L);
            verify(userRepository).delete(testUser);
        }

        @Test
        @DisplayName("should throw exception when deleting non-existent user")
        void shouldThrowExceptionWhenDeletingNonExistentUser() {
            // Arrange
            when(userRepository.findById(999L)).thenReturn(Optional.empty());

            // Act & Assert
            assertThatThrownBy(() -> userService.deleteUser(999L))
                    .isInstanceOf(UserNotFoundException.class)
                    .hasMessage("User not found with id: 999");

            verify(userRepository).findById(999L);
            verify(userRepository, never()).delete(any(User.class));
        }
    }
}
```

## Integration Testing Patterns

### Testing Controllers with Spring Boot Test

```java
// src/test/java/com/example/demo/controller/UserControllerIntegrationTest.java
package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.entity.UserRole;
import com.example.demo.repository.UserRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureWebMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import java.util.Optional;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.assertj.core.api.Assertions.*;

@SpringBootTest
@AutoConfigureWebMvc
@DisplayName("UserController Integration Tests")
class UserControllerIntegrationTest {

    @Autowired
    private WebApplicationContext webApplicationContext;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ObjectMapper objectMapper;

    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).build();
        userRepository.deleteAll(); // Clean up before each test
    }

    @Nested
    @DisplayName("GET /api/users")
    class GetAllUsersTests {

        @Test
        @DisplayName("should return empty list when no users exist")
        void shouldReturnEmptyList() throws Exception {
            mockMvc.perform(get("/api/users"))
                    .andExpect(status().isOk())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$", hasSize(0)));
        }

        @Test
        @DisplayName("should return list of users")
        void shouldReturnUsersList() throws Exception {
            // Arrange
            User user1 = createTestUser("John Doe", "john@example.com");
            User user2 = createTestUser("Jane Doe", "jane@example.com");
            userRepository.save(user1);
            userRepository.save(user2);

            // Act & Assert
            mockMvc.perform(get("/api/users"))
                    .andExpect(status().isOk())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$", hasSize(2)))
                    .andExpect(jsonPath("$[0].name", is("John Doe")))
                    .andExpect(jsonPath("$[0].email", is("john@example.com")))
                    .andExpect(jsonPath("$[1].name", is("Jane Doe")))
                    .andExpect(jsonPath("$[1].email", is("jane@example.com")));
        }
    }

    @Nested
    @DisplayName("GET /api/users/{id}")
    class GetUserByIdTests {

        @Test
        @DisplayName("should return user when exists")
        void shouldReturnUser() throws Exception {
            // Arrange
            User user = createTestUser("John Doe", "john@example.com");
            User savedUser = userRepository.save(user);

            // Act & Assert
            mockMvc.perform(get("/api/users/{id}", savedUser.getId()))
                    .andExpect(status().isOk())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.id", is(savedUser.getId().intValue())))
                    .andExpect(jsonPath("$.name", is("John Doe")))
                    .andExpect(jsonPath("$.email", is("john@example.com")))
                    .andExpect(jsonPath("$.role", is("USER")));
        }

        @Test
        @DisplayName("should return 404 when user does not exist")
        void shouldReturn404WhenUserNotFound() throws Exception {
            mockMvc.perform(get("/api/users/{id}", 999))
                    .andExpect(status().isNotFound())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.status", is(404)))
                    .andExpect(jsonPath("$.error", is("USER_NOT_FOUND")))
                    .andExpect(jsonPath("$.message", containsString("User not found")));
        }
    }

    @Nested
    @DisplayName("POST /api/users")
    class CreateUserTests {

        @Test
        @DisplayName("should create user successfully")
        void shouldCreateUser() throws Exception {
            // Arrange
            String userJson = """
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "password": "password123"
                }
                """;

            // Act & Assert
            mockMvc.perform(post("/api/users")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(userJson))
                    .andExpect(status().isCreated())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.name", is("John Doe")))
                    .andExpect(jsonPath("$.email", is("john@example.com")))
                    .andExpect(jsonPath("$.role", is("USER")));

            // Verify user was saved in database
            Optional<User> savedUser = userRepository.findByEmail("john@example.com");
            assertThat(savedUser).isPresent();
            assertThat(savedUser.get().getName()).isEqualTo("John Doe");
        }

        @Test
        @DisplayName("should return 400 for invalid data")
        void shouldReturn400ForInvalidData() throws Exception {
            // Arrange
            String invalidUserJson = """
                {
                    "name": "",
                    "email": "invalid-email",
                    "password": "123"
                }
                """;

            // Act & Assert
            mockMvc.perform(post("/api/users")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(invalidUserJson))
                    .andExpect(status().isBadRequest())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.status", is(400)))
                    .andExpect(jsonPath("$.error", is("VALIDATION_ERROR")))
                    .andExpect(jsonPath("$.fieldErrors.name", is("Name is required")))
                    .andExpect(jsonPath("$.fieldErrors.email", is("Email should be valid")))
                    .andExpect(jsonPath("$.fieldErrors.password", is("Password must be at least 8 characters")));
        }

        @Test
        @DisplayName("should return 409 for duplicate email")
        void shouldReturn409ForDuplicateEmail() throws Exception {
            // Arrange
            User existingUser = createTestUser("Existing User", "john@example.com");
            userRepository.save(existingUser);

            String userJson = """
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "password": "password123"
                }
                """;

            // Act & Assert
            mockMvc.perform(post("/api/users")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(userJson))
                    .andExpect(status().isConflict())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.status", is(409)))
                    .andExpect(jsonPath("$.error", is("EMAIL_ALREADY_EXISTS")));
        }
    }

    @Nested
    @DisplayName("PUT /api/users/{id}")
    class UpdateUserTests {

        @Test
        @DisplayName("should update user successfully")
        void shouldUpdateUser() throws Exception {
            // Arrange
            User user = createTestUser("John Doe", "john@example.com");
            User savedUser = userRepository.save(user);

            String updateJson = """
                {
                    "name": "John Smith",
                    "email": "johnsmith@example.com"
                }
                """;

            // Act & Assert
            mockMvc.perform(put("/api/users/{id}", savedUser.getId())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(updateJson))
                    .andExpect(status().isOk())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.id", is(savedUser.getId().intValue())))
                    .andExpect(jsonPath("$.name", is("John Smith")))
                    .andExpect(jsonPath("$.email", is("johnsmith@example.com")));

            // Verify user was updated in database
            Optional<User> updatedUser = userRepository.findById(savedUser.getId());
            assertThat(updatedUser).isPresent();
            assertThat(updatedUser.get().getName()).isEqualTo("John Smith");
            assertThat(updatedUser.get().getEmail()).isEqualTo("johnsmith@example.com");
        }

        @Test
        @DisplayName("should return 404 when updating non-existent user")
        void shouldReturn404WhenUpdatingNonExistentUser() throws Exception {
            String updateJson = """
                {
                    "name": "John Smith",
                    "email": "johnsmith@example.com"
                }
                """;

            mockMvc.perform(put("/api/users/{id}", 999)
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(updateJson))
                    .andExpect(status().isNotFound())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.status", is(404)))
                    .andExpect(jsonPath("$.error", is("USER_NOT_FOUND")));
        }
    }

    @Nested
    @DisplayName("DELETE /api/users/{id}")
    class DeleteUserTests {

        @Test
        @DisplayName("should delete user successfully")
        void shouldDeleteUser() throws Exception {
            // Arrange
            User user = createTestUser("John Doe", "john@example.com");
            User savedUser = userRepository.save(user);

            // Act & Assert
            mockMvc.perform(delete("/api/users/{id}", savedUser.getId()))
                    .andExpect(status().isNoContent());

            // Verify user was deleted from database
            Optional<User> deletedUser = userRepository.findById(savedUser.getId());
            assertThat(deletedUser).isNotPresent();
        }

        @Test
        @DisplayName("should return 404 when deleting non-existent user")
        void shouldReturn404WhenDeletingNonExistentUser() throws Exception {
            mockMvc.perform(delete("/api/users/{id}", 999))
                    .andExpect(status().isNotFound())
                    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.status", is(404)))
                    .andExpect(jsonPath("$.error", is("USER_NOT_FOUND")));
        }
    }

    private User createTestUser(String name, String email) {
        User user = new User();
        user.setName(name);
        user.setEmail(email);
        user.setPassword("password123");
        user.setRole(UserRole.USER);
        return user;
    }
}
```

## Testing with Testcontainers

```java
// src/test/java/com/example/demo/repository/UserRepositoryIntegrationTest.java
package com.example.demo.repository;

import com.example.demo.entity.User;
import com.example.demo.entity.UserRole;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
@DisplayName("UserRepository Integration Tests")
class UserRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:14-alpine")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private UserRepository userRepository;

    private User testUser;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();

        testUser = new User();
        testUser.setName("John Doe");
        testUser.setEmail("john@example.com");
        testUser.setPassword("password123");
        testUser.setRole(UserRole.USER);
    }

    @Test
    @DisplayName("should save and retrieve user")
    void shouldSaveAndRetrieveUser() {
        // Act
        User savedUser = userRepository.save(testUser);

        // Assert
        assertThat(savedUser.getId()).isNotNull();
        assertThat(savedUser.getName()).isEqualTo("John Doe");
        assertThat(savedUser.getEmail()).isEqualTo("john@example.com");

        Optional<User> retrievedUser = userRepository.findById(savedUser.getId());
        assertThat(retrievedUser).isPresent();
        assertThat(retrievedUser.get().getName()).isEqualTo("John Doe");
    }

    @Test
    @DisplayName("should find user by email")
    void shouldFindUserByEmail() {
        // Arrange
        userRepository.save(testUser);

        // Act
        Optional<User> foundUser = userRepository.findByEmail("john@example.com");

        // Assert
        assertThat(foundUser).isPresent();
        assertThat(foundUser.get().getName()).isEqualTo("John Doe");
    }

    @Test
    @DisplayName("should return empty when user not found by email")
    void shouldReturnEmptyWhenUserNotFoundByEmail() {
        // Act
        Optional<User> foundUser = userRepository.findByEmail("nonexistent@example.com");

        // Assert
        assertThat(foundUser).isEmpty();
    }

    @Test
    @DisplayName("should find all users")
    void shouldFindAllUsers() {
        // Arrange
        userRepository.save(testUser);

        User user2 = new User();
        user2.setName("Jane Doe");
        user2.setEmail("jane@example.com");
        user2.setPassword("password456");
        user2.setRole(UserRole.ADMIN);
        userRepository.save(user2);

        // Act
        List<User> allUsers = userRepository.findAll();

        // Assert
        assertThat(allUsers).hasSize(2);
        assertThat(allUsers).extracting(User::getName)
                .containsExactlyInAnyOrder("John Doe", "Jane Doe");
    }

    @Test
    @DisplayName("should update user")
    void shouldUpdateUser() {
        // Arrange
        User savedUser = userRepository.save(testUser);

        // Act
        savedUser.setName("John Smith");
        User updatedUser = userRepository.save(savedUser);

        // Assert
        assertThat(updatedUser.getName()).isEqualTo("John Smith");
        assertThat(updatedUser.getId()).isEqualTo(savedUser.getId());
    }

    @Test
    @DisplayName("should delete user")
    void shouldDeleteUser() {
        // Arrange
        User savedUser = userRepository.save(testUser);

        // Act
        userRepository.delete(savedUser);

        // Assert
        Optional<User> deletedUser = userRepository.findById(savedUser.getId());
        assertThat(deletedUser).isEmpty();
    }

    @Test
    @DisplayName("should check if email exists")
    void shouldCheckIfEmailExists() {
        // Arrange
        userRepository.save(testUser);

        // Act & Assert
        assertThat(userRepository.existsByEmail("john@example.com")).isTrue();
        assertThat(userRepository.existsByEmail("nonexistent@example.com")).isFalse();
    }
}
```

## Testing Custom Components

### Testing Custom Validators

```java
// src/main/java/com/example/demo/validation/StrongPasswordValidator.java
package com.example.demo.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.util.regex.Pattern;

public class StrongPasswordValidator implements ConstraintValidator<StrongPassword, String> {

    private static final Pattern PASSWORD_PATTERN =
        Pattern.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$");

    @Override
    public void initialize(StrongPassword constraintAnnotation) {
        // No initialization needed
    }

    @Override
    public boolean isValid(String password, ConstraintValidatorContext context) {
        if (password == null) {
            return false;
        }

        return PASSWORD_PATTERN.matcher(password).matches();
    }
}

// src/main/java/com/example/demo/validation/StrongPassword.java
package com.example.demo.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.*;

@Documented
@Constraint(validatedBy = StrongPasswordValidator.class)
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
public @interface StrongPassword {

    String message() default "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}

// src/test/java/com/example/demo/validation/StrongPasswordValidatorTest.java
package com.example.demo.validation;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import javax.validation.ConstraintValidatorContext;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@DisplayName("StrongPasswordValidator Tests")
class StrongPasswordValidatorTest {

    private StrongPasswordValidator validator;
    private ConstraintValidatorContext context;

    @BeforeEach
    void setUp() {
        validator = new StrongPasswordValidator();
        context = mock(ConstraintValidatorContext.class);
    }

    @Test
    @DisplayName("should initialize without errors")
    void shouldInitialize() {
        StrongPassword annotation = mock(StrongPassword.class);
        assertThatCode(() -> validator.initialize(annotation)).doesNotThrowAnyException();
    }

    @ParameterizedTest
    @ValueSource(strings = {
        "Password123!",
        "Strong@Pass1",
        "MySecure#2023",
        "Complex$Password9"
    })
    @DisplayName("should validate strong passwords")
    void shouldValidateStrongPasswords(String password) {
        assertThat(validator.isValid(password, context)).isTrue();
    }

    @ParameterizedTest
    @ValueSource(strings = {
        "password",      // no uppercase, numbers, special chars
        "PASSWORD",      // no lowercase, numbers, special chars
        "Password",      // no numbers, special chars
        "Password123",   // no special chars
        "Pass!",         // too short
        "",              // empty
        "12345678"       // only numbers
    })
    @DisplayName("should reject weak passwords")
    void shouldRejectWeakPasswords(String password) {
        assertThat(validator.isValid(password, context)).isFalse();
    }

    @Test
    @DisplayName("should return false for null password")
    void shouldReturnFalseForNullPassword() {
        assertThat(validator.isValid(null, context)).isFalse();
    }
}
```

This comprehensive guide covers JUnit testing patterns for Java/Spring Boot applications, including unit tests, integration tests, mocking strategies, and testing with Testcontainers.