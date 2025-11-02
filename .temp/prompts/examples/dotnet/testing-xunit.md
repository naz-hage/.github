# Testing Patterns with xUnit for .NET

This guide covers comprehensive testing patterns using xUnit for .NET applications, including unit tests, integration tests, mocking strategies, and best practices.

## Project Setup and Dependencies

### Test Project Structure

```
tests/
├── UnitTests/
│   ├── Application/
│   ├── Domain/
│   ├── Infrastructure/
│   └── Api/
├── IntegrationTests/
│   ├── Api/
│   ├── Database/
│   └── External/
└── EndToEndTests/
    ├── Api/
    └── Scenarios/
```

### NuGet Packages

```xml
<!-- UnitTests/UnitTests.csproj -->
<PackageReference Include="xunit" Version="2.5.0" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.5.0" />
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.6.0" />
<PackageReference Include="Moq" Version="4.18.4" />
<PackageReference Include="FluentAssertions" Version="6.11.0" />
<PackageReference Include="AutoFixture" Version="4.18.0" />
<PackageReference Include="AutoFixture.AutoMoq" Version="4.18.0" />
<PackageReference Include="coverlet.collector" Version="6.0.0" />
```

```xml
<!-- IntegrationTests/IntegrationTests.csproj -->
<PackageReference Include="xunit" Version="2.5.0" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.5.0" />
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.6.0" />
<PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="7.0.0" />
<PackageReference Include="Testcontainers.PostgreSql" Version="3.4.0" />
<PackageReference Include="Respawn" Version="6.0.0" />
<PackageReference Include="FluentAssertions" Version="6.11.0" />
<PackageReference Include="coverlet.collector" Version="6.0.0" />
```

```xml
<!-- EndToEndTests/EndToEndTests.csproj -->
<PackageReference Include="xunit" Version="2.5.0" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.5.0" />
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.6.0" />
<PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="7.0.0" />
<PackageReference Include="FluentAssertions" Version="6.11.0" />
<PackageReference Include="coverlet.collector" Version="6.0.0" />
```

## Unit Testing Patterns

### Testing Domain Entities

```csharp
// Domain/Entities/User.cs
using System;
using System.Collections.Generic;

namespace Domain.Entities
{
    public class User : BaseEntity
    {
        public string Email { get; private set; }
        public string FirstName { get; private set; }
        public string LastName { get; private set; }
        public bool IsActive { get; private set; }
        public DateTime CreatedAt { get; private set; }

        protected User() { } // EF Core constructor

        public User(string email, string firstName, string lastName)
        {
            Email = email ?? throw new ArgumentNullException(nameof(email));
            FirstName = firstName ?? throw new ArgumentNullException(nameof(firstName));
            LastName = lastName ?? throw new ArgumentNullException(nameof(lastName));
            IsActive = true;
            CreatedAt = DateTime.UtcNow;
        }

        public void UpdateProfile(string firstName, string lastName)
        {
            if (string.IsNullOrWhiteSpace(firstName))
                throw new ArgumentException("First name cannot be empty", nameof(firstName));
            if (string.IsNullOrWhiteSpace(lastName))
                throw new ArgumentException("Last name cannot be empty", nameof(lastName));

            FirstName = firstName;
            LastName = lastName;
        }

        public void Deactivate()
        {
            if (!IsActive)
                throw new InvalidOperationException("User is already inactive");

            IsActive = false;
        }

        public string GetFullName() => $"{FirstName} {LastName}";
    }
}

// tests/UnitTests/Domain/UserTests.cs
using System;
using AutoFixture;
using Domain.Entities;
using FluentAssertions;
using Xunit;

namespace UnitTests.Domain
{
    public class UserTests
    {
        private readonly Fixture _fixture;

        public UserTests()
        {
            _fixture = new Fixture();
        }

        [Fact]
        public void Constructor_ShouldCreateUser_WhenValidParameters()
        {
            // Arrange
            var email = "john.doe@example.com";
            var firstName = "John";
            var lastName = "Doe";

            // Act
            var user = new User(email, firstName, lastName);

            // Assert
            user.Email.Should().Be(email);
            user.FirstName.Should().Be(firstName);
            user.LastName.Should().Be(lastName);
            user.IsActive.Should().BeTrue();
            user.CreatedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(1));
        }

        [Theory]
        [InlineData(null)]
        [InlineData("")]
        [InlineData("   ")]
        public void Constructor_ShouldThrowArgumentNullException_WhenEmailIsNullOrEmpty(string email)
        {
            // Act
            Action act = () => new User(email, "John", "Doe");

            // Assert
            act.Should().Throw<ArgumentNullException>()
               .WithParameterName("email");
        }

        [Theory]
        [InlineData(null)]
        [InlineData("")]
        [InlineData("   ")]
        public void Constructor_ShouldThrowArgumentNullException_WhenFirstNameIsNullOrEmpty(string firstName)
        {
            // Act
            Action act = () => new User("john@example.com", firstName, "Doe");

            // Assert
            act.Should().Throw<ArgumentNullException>()
               .WithParameterName("firstName");
        }

        [Fact]
        public void UpdateProfile_ShouldUpdateNames_WhenValidParameters()
        {
            // Arrange
            var user = new User("john@example.com", "John", "Doe");
            var newFirstName = "Jane";
            var newLastName = "Smith";

            // Act
            user.UpdateProfile(newFirstName, newLastName);

            // Assert
            user.FirstName.Should().Be(newFirstName);
            user.LastName.Should().Be(newLastName);
        }

        [Theory]
        [InlineData(null)]
        [InlineData("")]
        [InlineData("   ")]
        public void UpdateProfile_ShouldThrowArgumentException_WhenFirstNameIsInvalid(string firstName)
        {
            // Arrange
            var user = new User("john@example.com", "John", "Doe");

            // Act
            Action act = () => user.UpdateProfile(firstName, "Smith");

            // Assert
            act.Should().Throw<ArgumentException>()
               .WithParameterName("firstName")
               .WithMessage("First name cannot be empty*");
        }

        [Fact]
        public void Deactivate_ShouldSetIsActiveToFalse_WhenUserIsActive()
        {
            // Arrange
            var user = new User("john@example.com", "John", "Doe");

            // Act
            user.Deactivate();

            // Assert
            user.IsActive.Should().BeFalse();
        }

        [Fact]
        public void Deactivate_ShouldThrowInvalidOperationException_WhenUserIsAlreadyInactive()
        {
            // Arrange
            var user = new User("john@example.com", "John", "Doe");
            user.Deactivate();

            // Act
            Action act = () => user.Deactivate();

            // Assert
            act.Should().Throw<InvalidOperationException>()
               .WithMessage("User is already inactive");
        }

        [Fact]
        public void GetFullName_ShouldReturnFormattedFullName()
        {
            // Arrange
            var user = new User("john@example.com", "John", "Doe");

            // Act
            var fullName = user.GetFullName();

            // Assert
            fullName.Should().Be("John Doe");
        }

        [Fact]
        public void User_ShouldBeEqual_WhenSameId()
        {
            // Arrange
            var user1 = _fixture.Create<User>();
            var user2 = new User(user1.Email, user1.FirstName, user1.LastName)
            {
                Id = user1.Id // Manually set same ID
            };

            // Act & Assert
            user1.Should().Be(user2);
            user1.GetHashCode().Should().Be(user2.GetHashCode());
        }

        [Fact]
        public void User_ShouldNotBeEqual_WhenDifferentId()
        {
            // Arrange
            var user1 = _fixture.Create<User>();
            var user2 = _fixture.Create<User>();

            // Act & Assert
            user1.Should().NotBe(user2);
        }
    }
}
```

### Testing Application Services

```csharp
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
            _logger.LogInformation("Creating user with email {Email}", request.Email);

            // Check if user already exists
            var existingUser = await _userRepository.GetByEmailAsync(request.Email);
            if (existingUser != null)
            {
                throw new UserAlreadyExistsException(request.Email);
            }

            // Create user
            var user = new User(request.Email, request.FirstName, request.LastName);

            await _userRepository.AddAsync(user);
            await _userRepository.SaveChangesAsync();

            _logger.LogInformation("User created with ID {UserId}", user.Id);

            return user.Id;
        }
    }
}

// tests/UnitTests/Application/CreateUserCommandHandlerTests.cs
using System;
using System.Threading;
using System.Threading.Tasks;
using Application.Commands;
using AutoFixture;
using Domain.Entities;
using Domain.Interfaces;
using FluentAssertions;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace UnitTests.Application
{
    public class CreateUserCommandHandlerTests
    {
        private readonly Mock<IUserRepository> _userRepositoryMock;
        private readonly Mock<ILogger<CreateUserCommandHandler>> _loggerMock;
        private readonly CreateUserCommandHandler _handler;
        private readonly Fixture _fixture;

        public CreateUserCommandHandlerTests()
        {
            _fixture = new Fixture();
            _userRepositoryMock = new Mock<IUserRepository>();
            _loggerMock = new Mock<ILogger<CreateUserCommandHandler>>();
            _handler = new CreateUserCommandHandler(
                _userRepositoryMock.Object,
                _loggerMock.Object);
        }

        [Fact]
        public async Task Handle_ShouldCreateUser_WhenUserDoesNotExist()
        {
            // Arrange
            var command = _fixture.Create<CreateUserCommand>();
            var expectedUserId = Guid.NewGuid();

            _userRepositoryMock
                .Setup(x => x.GetByEmailAsync(command.Email))
                .ReturnsAsync((User)null);

            _userRepositoryMock
                .Setup(x => x.AddAsync(It.IsAny<User>()))
                .Callback<User>(user => user.Id = expectedUserId)
                .Returns(Task.CompletedTask);

            _userRepositoryMock
                .Setup(x => x.SaveChangesAsync())
                .ReturnsAsync(1);

            // Act
            var result = await _handler.Handle(command, CancellationToken.None);

            // Assert
            result.Should().Be(expectedUserId);

            _userRepositoryMock.Verify(x => x.GetByEmailAsync(command.Email), Times.Once);
            _userRepositoryMock.Verify(x => x.AddAsync(It.Is<User>(u =>
                u.Email == command.Email &&
                u.FirstName == command.FirstName &&
                u.LastName == command.LastName)), Times.Once);
            _userRepositoryMock.Verify(x => x.SaveChangesAsync(), Times.Once);
        }

        [Fact]
        public async Task Handle_ShouldThrowUserAlreadyExistsException_WhenUserExists()
        {
            // Arrange
            var command = _fixture.Create<CreateUserCommand>();
            var existingUser = _fixture.Create<User>();

            _userRepositoryMock
                .Setup(x => x.GetByEmailAsync(command.Email))
                .ReturnsAsync(existingUser);

            // Act
            Func<Task> act = () => _handler.Handle(command, CancellationToken.None);

            // Assert
            await act.Should().ThrowAsync<UserAlreadyExistsException>()
                .WithMessage($"*'{command.Email}'*");

            _userRepositoryMock.Verify(x => x.GetByEmailAsync(command.Email), Times.Once);
            _userRepositoryMock.Verify(x => x.AddAsync(It.IsAny<User>()), Times.Never);
            _userRepositoryMock.Verify(x => x.SaveChangesAsync(), Times.Never);
        }

        [Fact]
        public async Task Handle_ShouldLogInformation_WhenCreatingUser()
        {
            // Arrange
            var command = _fixture.Create<CreateUserCommand>();

            _userRepositoryMock
                .Setup(x => x.GetByEmailAsync(command.Email))
                .ReturnsAsync((User)null);

            _userRepositoryMock
                .Setup(x => x.AddAsync(It.IsAny<User>()))
                .Returns(Task.CompletedTask);

            _userRepositoryMock
                .Setup(x => x.SaveChangesAsync())
                .ReturnsAsync(1);

            // Act
            await _handler.Handle(command, CancellationToken.None);

            // Assert
            _loggerMock.VerifyLog(logger => logger.LogInformation("Creating user with email {Email}", command.Email));
            _loggerMock.VerifyLog(logger => logger.LogInformation("User created with ID {UserId}", It.IsAny<Guid>()));
        }

        [Fact]
        public async Task Handle_ShouldHandleCancellation_WhenCancellationRequested()
        {
            // Arrange
            var command = _fixture.Create<CreateUserCommand>();
            var cancellationToken = new CancellationToken(true);

            // Act
            Func<Task> act = () => _handler.Handle(command, cancellationToken);

            // Assert
            await act.Should().ThrowAsync<OperationCanceledException>();
        }
    }
}
```

### Testing Infrastructure Components

```csharp
// Infrastructure/External/EmailService.cs
using System.Net;
using System.Net.Mail;
using System.Threading.Tasks;
using Application.Interfaces;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace Infrastructure.External
{
    public class EmailService : IEmailService
    {
        private readonly EmailSettings _emailSettings;
        private readonly ILogger<EmailService> _logger;

        public EmailService(IOptions<EmailSettings> emailSettings, ILogger<EmailService> logger)
        {
            _emailSettings = emailSettings.Value;
            _logger = logger;
        }

        public async Task SendEmailAsync(string to, string subject, string body)
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
    }
}

// tests/UnitTests/Infrastructure/EmailServiceTests.cs
using System;
using System.Net.Mail;
using System.Threading.Tasks;
using AutoFixture;
using FluentAssertions;
using Infrastructure.External;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Moq;
using Xunit;

namespace UnitTests.Infrastructure
{
    public class EmailServiceTests : IDisposable
    {
        private readonly Mock<IOptions<EmailSettings>> _emailSettingsMock;
        private readonly Mock<ILogger<EmailService>> _loggerMock;
        private readonly EmailService _emailService;
        private readonly Fixture _fixture;

        public EmailServiceTests()
        {
            _fixture = new Fixture();
            _emailSettingsMock = new Mock<IOptions<EmailSettings>>();
            _loggerMock = new Mock<ILogger<EmailService>>();

            var emailSettings = new EmailSettings
            {
                SmtpServer = "smtp.gmail.com",
                Port = 587,
                Username = "test@example.com",
                Password = "password",
                EnableSsl = true,
                FromEmail = "noreply@example.com",
                FromName = "Test App"
            };

            _emailSettingsMock.Setup(x => x.Value).Returns(emailSettings);

            _emailService = new EmailService(_emailSettingsMock.Object, _loggerMock.Object);
        }

        [Fact]
        public void Constructor_ShouldInitializeCorrectly()
        {
            // Assert
            _emailService.Should().NotBeNull();
        }

        [Fact]
        public async Task SendEmailAsync_ShouldSendEmail_WhenValidParameters()
        {
            // Arrange
            var to = "recipient@example.com";
            var subject = "Test Subject";
            var body = "<h1>Test Body</h1>";

            // Note: In a real test, you would mock SmtpClient or use a test SMTP server
            // This test demonstrates the structure but would need additional setup for SMTP mocking

            // Act & Assert
            // This would normally work with a proper SMTP mock or test server
            await Assert.ThrowsAsync<SmtpException>(() =>
                _emailService.SendEmailAsync(to, subject, body));

            // Verify logging
            _loggerMock.VerifyLog(logger => logger.LogInformation(
                "Email sent to {To} with subject '{Subject}'", to, subject), Times.Never);
        }

        [Theory]
        [InlineData(null)]
        [InlineData("")]
        [InlineData("   ")]
        public async Task SendEmailAsync_ShouldHandleInvalidEmailAddresses(string invalidEmail)
        {
            // Arrange
            var subject = "Test Subject";
            var body = "Test Body";

            // Act & Assert
            await Assert.ThrowsAsync<ArgumentException>(() =>
                _emailService.SendEmailAsync(invalidEmail, subject, body));
        }

        public void Dispose()
        {
            // Clean up resources if needed
        }
    }
}
```

## Integration Testing Patterns

### Testing Controllers with WebApplicationFactory

```csharp
// tests/IntegrationTests/Api/UsersControllerTests.cs
using System;
using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using Application.DTOs;
using FluentAssertions;
using IntegrationTests.TestHelpers;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace IntegrationTests.Api
{
    public class UsersControllerTests : IClassFixture<WebApplicationFactory<Program>>, IDisposable
    {
        private readonly HttpClient _client;
        private readonly WebApplicationFactory<Program> _factory;
        private readonly DatabaseHelper _databaseHelper;

        public UsersControllerTests(WebApplicationFactory<Program> factory)
        {
            _factory = factory.WithWebHostBuilder(builder =>
            {
                builder.ConfigureTestServices(services =>
                {
                    // Configure test services
                    services.AddTestDatabase();
                });
            });

            _client = _factory.CreateClient();
            _databaseHelper = new DatabaseHelper(_factory);
        }

        [Fact]
        public async Task CreateUser_ShouldReturnCreated_WhenValidData()
        {
            // Arrange
            var createUserDto = new
            {
                email = "john.doe@example.com",
                firstName = "John",
                lastName = "Doe",
                password = "Password123!"
            };

            // Act
            var response = await _client.PostAsJsonAsync("/api/users", createUserDto);

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.Created);

            var userId = await response.Content.ReadFromJsonAsync<Guid>();
            userId.Should().NotBeEmpty();

            // Verify user was created in database
            var user = await _databaseHelper.GetUserByIdAsync(userId);
            user.Should().NotBeNull();
            user.Email.Should().Be(createUserDto.email);
            user.FirstName.Should().Be(createUserDto.firstName);
            user.LastName.Should().Be(createUserDto.lastName);
        }

        [Fact]
        public async Task CreateUser_ShouldReturnBadRequest_WhenEmailAlreadyExists()
        {
            // Arrange
            var existingUser = await _databaseHelper.CreateTestUserAsync("existing@example.com");

            var createUserDto = new
            {
                email = "existing@example.com",
                firstName = "Jane",
                lastName = "Smith",
                password = "Password123!"
            };

            // Act
            var response = await _client.PostAsJsonAsync("/api/users", createUserDto);

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.Conflict);

            var errorResponse = await response.Content.ReadFromJsonAsync<ErrorResponse>();
            errorResponse.ErrorCode.Should().Be("USER_ALREADY_EXISTS");
            errorResponse.Message.Should().Contain("existing@example.com");
        }

        [Fact]
        public async Task GetUser_ShouldReturnUser_WhenUserExists()
        {
            // Arrange
            var testUser = await _databaseHelper.CreateTestUserAsync();

            // Act
            var response = await _client.GetAsync($"/api/users/{testUser.Id}");

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.OK);

            var userDto = await response.Content.ReadFromJsonAsync<UserDto>();
            userDto.Should().NotBeNull();
            userDto.Id.Should().Be(testUser.Id);
            userDto.Email.Should().Be(testUser.Email);
            userDto.FirstName.Should().Be(testUser.FirstName);
            userDto.LastName.Should().Be(testUser.LastName);
        }

        [Fact]
        public async Task GetUser_ShouldReturnNotFound_WhenUserDoesNotExist()
        {
            // Arrange
            var nonExistentId = Guid.NewGuid();

            // Act
            var response = await _client.GetAsync($"/api/users/{nonExistentId}");

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.NotFound);

            var errorResponse = await response.Content.ReadFromJsonAsync<ErrorResponse>();
            errorResponse.ErrorCode.Should().Be("USER_NOT_FOUND");
        }

        [Fact]
        public async Task UpdateUser_ShouldReturnNoContent_WhenUpdateSuccessful()
        {
            // Arrange
            var testUser = await _databaseHelper.CreateTestUserAsync();

            var updateDto = new
            {
                firstName = "Updated",
                lastName = "Name"
            };

            // Act
            var response = await _client.PutAsJsonAsync($"/api/users/{testUser.Id}", updateDto);

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.NoContent);

            // Verify user was updated in database
            var updatedUser = await _databaseHelper.GetUserByIdAsync(testUser.Id);
            updatedUser.FirstName.Should().Be(updateDto.firstName);
            updatedUser.LastName.Should().Be(updateDto.lastName);
        }

        [Fact]
        public async Task DeleteUser_ShouldReturnNoContent_WhenDeletionSuccessful()
        {
            // Arrange
            var testUser = await _databaseHelper.CreateTestUserAsync();

            // Act
            var response = await _client.DeleteAsync($"/api/users/{testUser.Id}");

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.NoContent);

            // Verify user was deleted from database
            var deletedUser = await _databaseHelper.GetUserByIdAsync(testUser.Id);
            deletedUser.Should().BeNull();
        }

        public void Dispose()
        {
            _databaseHelper?.Dispose();
            _client?.Dispose();
        }
    }

    public class ErrorResponse
    {
        public string ErrorCode { get; set; }
        public string Message { get; set; }
    }
}
```

### Database Integration Testing

```csharp
// tests/IntegrationTests/TestHelpers/DatabaseHelper.cs
using System;
using System.Threading.Tasks;
using Domain.Entities;
using Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace IntegrationTests.TestHelpers
{
    public class DatabaseHelper : IDisposable
    {
        private readonly IServiceScope _scope;
        private readonly AppDbContext _context;

        public DatabaseHelper(WebApplicationFactory<Program> factory)
        {
            _scope = factory.Services.CreateScope();
            _context = _scope.ServiceProvider.GetRequiredService<AppDbContext>();
        }

        public async Task<User> CreateTestUserAsync(string email = null)
        {
            var user = new User(
                email ?? $"test.{Guid.NewGuid()}@example.com",
                "Test",
                "User"
            );

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            return user;
        }

        public async Task<User> GetUserByIdAsync(Guid id)
        {
            return await _context.Users.FindAsync(id);
        }

        public async Task<User> GetUserByEmailAsync(string email)
        {
            return await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
        }

        public async Task ResetDatabaseAsync()
        {
            // Reset database state between tests
            await _context.Database.ExecuteSqlRawAsync("DELETE FROM UserRoles");
            await _context.Database.ExecuteSqlRawAsync("DELETE FROM Users");
            await _context.SaveChangesAsync();
        }

        public void Dispose()
        {
            _scope?.Dispose();
        }
    }
}

// tests/IntegrationTests/Database/UserRepositoryTests.cs
using System;
using System.Linq;
using System.Threading.Tasks;
using Domain.Entities;
using FluentAssertions;
using Infrastructure.Repositories;
using IntegrationTests.TestHelpers;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace IntegrationTests.Database
{
    public class UserRepositoryTests : IClassFixture<WebApplicationFactory<Program>>, IDisposable
    {
        private readonly WebApplicationFactory<Program> _factory;
        private readonly DatabaseHelper _databaseHelper;
        private readonly UserRepository _userRepository;

        public UserRepositoryTests(WebApplicationFactory<Program> factory)
        {
            _factory = factory.WithWebHostBuilder(builder =>
            {
                builder.ConfigureTestServices(services =>
                {
                    services.AddTestDatabase();
                });
            });

            var scope = _factory.Services.CreateScope();
            _databaseHelper = new DatabaseHelper(_factory);
            _userRepository = scope.ServiceProvider.GetRequiredService<UserRepository>();
        }

        [Fact]
        public async Task AddAsync_ShouldAddUserToDatabase()
        {
            // Arrange
            var user = new User("john@example.com", "John", "Doe");

            // Act
            await _userRepository.AddAsync(user);
            await _userRepository.SaveChangesAsync();

            // Assert
            var savedUser = await _databaseHelper.GetUserByIdAsync(user.Id);
            savedUser.Should().NotBeNull();
            savedUser.Email.Should().Be(user.Email);
            savedUser.FirstName.Should().Be(user.FirstName);
            savedUser.LastName.Should().Be(user.LastName);
        }

        [Fact]
        public async Task GetByIdAsync_ShouldReturnUser_WhenUserExists()
        {
            // Arrange
            var testUser = await _databaseHelper.CreateTestUserAsync();

            // Act
            var result = await _userRepository.GetByIdAsync(testUser.Id);

            // Assert
            result.Should().NotBeNull();
            result.Id.Should().Be(testUser.Id);
            result.Email.Should().Be(testUser.Email);
        }

        [Fact]
        public async Task GetByIdAsync_ShouldReturnNull_WhenUserDoesNotExist()
        {
            // Arrange
            var nonExistentId = Guid.NewGuid();

            // Act
            var result = await _userRepository.GetByIdAsync(nonExistentId);

            // Assert
            result.Should().BeNull();
        }

        [Fact]
        public async Task GetByEmailAsync_ShouldReturnUser_WhenEmailExists()
        {
            // Arrange
            var testUser = await _databaseHelper.CreateTestUserAsync("unique@example.com");

            // Act
            var result = await _userRepository.GetByEmailAsync("unique@example.com");

            // Assert
            result.Should().NotBeNull();
            result.Id.Should().Be(testUser.Id);
            result.Email.Should().Be("unique@example.com");
        }

        [Fact]
        public async Task GetAllAsync_ShouldReturnAllUsers()
        {
            // Arrange
            await _databaseHelper.ResetDatabaseAsync();
            var user1 = await _databaseHelper.CreateTestUserAsync();
            var user2 = await _databaseHelper.CreateTestUserAsync();

            // Act
            var result = await _userRepository.GetAllAsync();

            // Assert
            result.Should().HaveCount(2);
            result.Should().Contain(u => u.Id == user1.Id);
            result.Should().Contain(u => u.Id == user2.Id);
        }

        [Fact]
        public async Task GetActiveUsersAsync_ShouldReturnOnlyActiveUsers()
        {
            // Arrange
            await _databaseHelper.ResetDatabaseAsync();
            var activeUser = await _databaseHelper.CreateTestUserAsync();
            var inactiveUser = await _databaseHelper.CreateTestUserAsync();
            inactiveUser.Deactivate();

            await _userRepository.Update(inactiveUser);
            await _userRepository.SaveChangesAsync();

            // Act
            var result = await _userRepository.GetActiveUsersAsync();

            // Assert
            result.Should().HaveCount(1);
            result.First().Id.Should().Be(activeUser.Id);
        }

        [Fact]
        public async Task Update_ShouldModifyUserInDatabase()
        {
            // Arrange
            var testUser = await _databaseHelper.CreateTestUserAsync();
            testUser.UpdateProfile("Updated", "Name");

            // Act
            _userRepository.Update(testUser);
            await _userRepository.SaveChangesAsync();

            // Assert
            var updatedUser = await _databaseHelper.GetUserByIdAsync(testUser.Id);
            updatedUser.FirstName.Should().Be("Updated");
            updatedUser.LastName.Should().Be("Name");
        }

        [Fact]
        public async Task Delete_ShouldRemoveUserFromDatabase()
        {
            // Arrange
            var testUser = await _databaseHelper.CreateTestUserAsync();

            // Act
            _userRepository.Delete(testUser);
            await _userRepository.SaveChangesAsync();

            // Assert
            var deletedUser = await _databaseHelper.GetUserByIdAsync(testUser.Id);
            deletedUser.Should().BeNull();
        }

        public void Dispose()
        {
            _databaseHelper?.Dispose();
        }
    }
}
```

### Test Fixtures and Collections

```csharp
// tests/IntegrationTests/TestCollection.cs
using Xunit;

namespace IntegrationTests
{
    [CollectionDefinition("Database collection")]
    public class DatabaseCollection : ICollectionFixture<WebApplicationFactory<Program>>
    {
        // This class has no code, and is never created. Its purpose is simply
        // to be the place to apply [CollectionDefinition] and all the
        // ICollectionFixture<> interfaces.
    }
}

// tests/IntegrationTests/TestHelpers/TestWebApplicationFactory.cs
using System;
using Infrastructure.Data;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace IntegrationTests.TestHelpers
{
    public class TestWebApplicationFactory<TStartup> : WebApplicationFactory<TStartup> where TStartup : class
    {
        protected override void ConfigureWebHost(IWebHostBuilder builder)
        {
            builder.ConfigureServices(services =>
            {
                // Remove the app's DbContext registration
                var descriptor = services.SingleOrDefault(
                    d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));

                if (descriptor != null)
                {
                    services.Remove(descriptor);
                }

                // Add DbContext using an in-memory database for testing
                services.AddDbContext<AppDbContext>(options =>
                {
                    options.UseInMemoryDatabase("TestDb");
                });

                // Build the service provider
                var sp = services.BuildServiceProvider();

                // Create a scope to obtain a reference to the database context
                using var scope = sp.CreateScope();
                var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

                // Ensure the database is created
                db.Database.EnsureCreated();
            });
        }
    }
}

// tests/IntegrationTests/Api/UsersApiTests.cs
using System.Net;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FluentAssertions;
using IntegrationTests.TestHelpers;
using Xunit;

namespace IntegrationTests.Api
{
    [Collection("Database collection")]
    public class UsersApiTests : IAsyncLifetime
    {
        private readonly TestWebApplicationFactory<Program> _factory;
        private readonly HttpClient _client;
        private readonly DatabaseHelper _databaseHelper;

        public UsersApiTests(TestWebApplicationFactory<Program> factory)
        {
            _factory = factory;
            _client = _factory.CreateClient();
            _databaseHelper = new DatabaseHelper(_factory);
        }

        public async Task InitializeAsync()
        {
            // Reset database before each test
            await _databaseHelper.ResetDatabaseAsync();
        }

        public Task DisposeAsync()
        {
            _client?.Dispose();
            return Task.CompletedTask;
        }

        [Fact]
        public async Task GetUsers_ShouldReturnEmptyList_WhenNoUsersExist()
        {
            // Act
            var response = await _client.GetAsync("/api/users");

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.OK);

            var users = await response.Content.ReadFromJsonAsync<UserDto[]>();
            users.Should().BeEmpty();
        }

        [Fact]
        public async Task GetUsers_ShouldReturnUsers_WhenUsersExist()
        {
            // Arrange
            var user1 = await _databaseHelper.CreateTestUserAsync();
            var user2 = await _databaseHelper.CreateTestUserAsync();

            // Act
            var response = await _client.GetAsync("/api/users");

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.OK);

            var users = await response.Content.ReadFromJsonAsync<UserDto[]>();
            users.Should().HaveCount(2);
            users.Should().Contain(u => u.Id == user1.Id);
            users.Should().Contain(u => u.Id == user2.Id);
        }
    }
}
```

## End-to-End Testing

### E2E Test with Real Dependencies

```csharp
// tests/EndToEndTests/UserWorkflowTests.cs
using System.Net;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace EndToEndTests
{
    public class UserWorkflowTests : IClassFixture<WebApplicationFactory<Program>>, IDisposable
    {
        private readonly HttpClient _client;
        private readonly WebApplicationFactory<Program> _factory;

        public UserWorkflowTests(WebApplicationFactory<Program> factory)
        {
            _factory = factory;
            _client = _factory.CreateClient();
        }

        [Fact]
        public async Task CompleteUserWorkflow_ShouldWorkEndToEnd()
        {
            // Step 1: Create a user
            var createUserDto = new
            {
                email = "workflow.test@example.com",
                firstName = "Workflow",
                lastName = "Test",
                password = "Password123!"
            };

            var createResponse = await _client.PostAsJsonAsync("/api/users", createUserDto);
            createResponse.StatusCode.Should().Be(HttpStatusCode.Created);

            var userId = await createResponse.Content.ReadFromJsonAsync<Guid>();
            userId.Should().NotBeEmpty();

            // Step 2: Get the created user
            var getResponse = await _client.GetAsync($"/api/users/{userId}");
            getResponse.StatusCode.Should().Be(HttpStatusCode.OK);

            var user = await getResponse.Content.ReadFromJsonAsync<UserDto>();
            user.Should().NotBeNull();
            user.Id.Should().Be(userId);
            user.Email.Should().Be(createUserDto.email);
            user.FirstName.Should().Be(createUserDto.firstName);
            user.LastName.Should().Be(createUserDto.lastName);

            // Step 3: Update the user
            var updateDto = new
            {
                firstName = "Updated",
                lastName = "Workflow"
            };

            var updateResponse = await _client.PutAsJsonAsync($"/api/users/{userId}", updateDto);
            updateResponse.StatusCode.Should().Be(HttpStatusCode.NoContent);

            // Step 4: Verify the update
            var getUpdatedResponse = await _client.GetAsync($"/api/users/{userId}");
            getUpdatedResponse.StatusCode.Should().Be(HttpStatusCode.OK);

            var updatedUser = await getUpdatedResponse.Content.ReadFromJsonAsync<UserDto>();
            updatedUser.FirstName.Should().Be(updateDto.firstName);
            updatedUser.LastName.Should().Be(updateDto.lastName);

            // Step 5: Delete the user
            var deleteResponse = await _client.DeleteAsync($"/api/users/{userId}");
            deleteResponse.StatusCode.Should().Be(HttpStatusCode.NoContent);

            // Step 6: Verify the user is deleted
            var getDeletedResponse = await _client.GetAsync($"/api/users/{userId}");
            getDeletedResponse.StatusCode.Should().Be(HttpStatusCode.NotFound);
        }

        [Fact]
        public async Task HealthCheck_ShouldReturnHealthy()
        {
            // Act
            var response = await _client.GetAsync("/health");

            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.OK);

            var healthStatus = await response.Content.ReadAsStringAsync();
            healthStatus.Should().Contain("Healthy");
        }

        public void Dispose()
        {
            _client?.Dispose();
        }
    }
}
```

## Test Configuration and Utilities

### Test Startup Configuration

```csharp
// tests/IntegrationTests/TestStartup.cs
using Infrastructure.Data;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace IntegrationTests
{
    public class TestStartup
    {
        public TestStartup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        public void ConfigureServices(IServiceCollection services)
        {
            // Use in-memory database for tests
            services.AddDbContext<AppDbContext>(options =>
                options.UseInMemoryDatabase("TestDb"));

            // Add other services...
            services.AddMediatR(typeof(CreateUserCommand).Assembly);
            services.AddAutoMapper(typeof(UserProfile).Assembly);
            services.AddScoped<IUserRepository, UserRepository>();

            // Configure test email service
            services.AddScoped<IEmailService, TestEmailService>();

            services.AddControllers();
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            app.UseRouting();
            app.UseAuthorization();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}

// tests/IntegrationTests/TestEmailService.cs
using System.Threading.Tasks;
using Application.Interfaces;

namespace IntegrationTests
{
    public class TestEmailService : IEmailService
    {
        public List<EmailMessage> SentEmails { get; } = new();

        public Task SendEmailAsync(string to, string subject, string body)
        {
            SentEmails.Add(new EmailMessage(to, subject, body));
            return Task.CompletedTask;
        }

        public void Clear() => SentEmails.Clear();
    }

    public record EmailMessage(string To, string Subject, string Body);
}
```

### Custom Test Extensions

```csharp
// tests/UnitTests/TestExtensions/LoggerExtensions.cs
using Microsoft.Extensions.Logging;
using Moq;

namespace UnitTests.TestExtensions
{
    public static class LoggerExtensions
    {
        public static void VerifyLog<T>(this Mock<ILogger<T>> loggerMock,
            Expression<Action<ILogger<T>>> expression, Times? times = null)
        {
            loggerMock.Verify(expression, times ?? Times.Once());
        }

        public static void VerifyLog<T>(this Mock<ILogger<T>> loggerMock,
            Func<ILogger<T>, bool> predicate, Times? times = null)
        {
            loggerMock.Verify(logger => predicate(logger), times ?? Times.Once());
        }
    }
}

// tests/UnitTests/TestExtensions/ServiceCollectionExtensions.cs
using Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace UnitTests.TestExtensions
{
    public static class ServiceCollectionExtensions
    {
        public static IServiceCollection AddTestDatabase(this IServiceCollection services)
        {
            // Remove existing DbContext registration
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));

            if (descriptor != null)
            {
                services.Remove(descriptor);
            }

            // Add test database
            services.AddDbContext<AppDbContext>(options =>
                options.UseInMemoryDatabase("TestDb"));

            return services;
        }
    }
}
```

This comprehensive guide covers xUnit testing patterns for .NET applications, including unit tests, integration tests, database testing, mocking strategies, and end-to-end testing with proper test organization and utilities.