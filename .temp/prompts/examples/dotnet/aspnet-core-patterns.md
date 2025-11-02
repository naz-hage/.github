# ASP.NET Core Patterns and Best Practices

This guide covers comprehensive patterns and best practices for ASP.NET Core applications, including layered architecture, dependency injection, middleware, API design, and enterprise application patterns.

## Project Setup and Dependencies

### Project Structure

```
src/
├── Api/
│   ├── Controllers/
│   ├── Filters/
│   ├── Middleware/
│   └── Program.cs
├── Application/
│   ├── Commands/
│   ├── Queries/
│   ├── Handlers/
│   ├── Services/
│   ├── DTOs/
│   └── Interfaces/
├── Domain/
│   ├── Entities/
│   ├── ValueObjects/
│   ├── Interfaces/
│   └── Events/
├── Infrastructure/
│   ├── Data/
│   ├── External/
│   ├── Identity/
│   └── Logging/
└── Tests/
    ├── Unit/
    ├── Integration/
    └── EndToEnd/
```

### NuGet Packages

```xml
<!-- Api/Api.csproj -->
<PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="7.0.0" />
<PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
<PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="7.0.0" />
<PackageReference Include="Microsoft.AspNetCore.Cors" Version="7.0.0" />
<PackageReference Include="Serilog.AspNetCore" Version="7.0.0" />
<PackageReference Include="FluentValidation.AspNetCore" Version="11.3.0" />
<PackageReference Include="MediatR" Version="12.0.1" />
<PackageReference Include="AutoMapper" Version="12.0.1" />
```

```xml
<!-- Application/Application.csproj -->
<PackageReference Include="MediatR" Version="12.0.1" />
<PackageReference Include="FluentValidation" Version="11.3.0" />
<PackageReference Include="AutoMapper" Version="12.0.1" />
<PackageReference Include="Microsoft.Extensions.Logging.Abstractions" Version="7.0.0" />
```

```xml
<!-- Infrastructure/Infrastructure.csproj -->
<PackageReference Include="Microsoft.EntityFrameworkCore" Version="7.0.0" />
<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="7.0.0" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="7.0.0" />
<PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="7.0.0" />
<PackageReference Include="Polly" Version="8.0.0" />
<PackageReference Include="StackExchange.Redis" Version="2.6.122" />
```

## Domain Layer

### Entities and Value Objects

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
        public DateTime? LastLoginAt { get; private set; }

        // Navigation properties
        private readonly List<UserRole> _userRoles = new();
        public IReadOnlyCollection<UserRole> UserRoles => _userRoles.AsReadOnly();

        private readonly List<RefreshToken> _refreshTokens = new();
        public IReadOnlyCollection<RefreshToken> RefreshTokens => _refreshTokens.AsReadOnly();

        protected User() { } // EF Core constructor

        public User(string email, string firstName, string lastName)
        {
            Email = email ?? throw new ArgumentNullException(nameof(email));
            FirstName = firstName ?? throw new ArgumentNullException(nameof(firstName));
            LastName = lastName ?? throw new ArgumentNullException(nameof(lastName));
            IsActive = true;
            CreatedAt = DateTime.UtcNow;

            // Raise domain event
            AddDomainEvent(new UserCreatedEvent(Id, email));
        }

        public void UpdateProfile(string firstName, string lastName)
        {
            if (string.IsNullOrWhiteSpace(firstName))
                throw new ArgumentException("First name cannot be empty", nameof(firstName));
            if (string.IsNullOrWhiteSpace(lastName))
                throw new ArgumentException("Last name cannot be empty", nameof(lastName));

            FirstName = firstName;
            LastName = lastName;

            AddDomainEvent(new UserProfileUpdatedEvent(Id));
        }

        public void Deactivate()
        {
            if (!IsActive)
                throw new InvalidOperationException("User is already inactive");

            IsActive = false;
            AddDomainEvent(new UserDeactivatedEvent(Id));
        }

        public void RecordLogin()
        {
            LastLoginAt = DateTime.UtcNow;
        }

        public string GetFullName() => $"{FirstName} {LastName}";
    }
}

// Domain/Entities/BaseEntity.cs
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using MediatR;

namespace Domain.Entities
{
    public abstract class BaseEntity : IEntity
    {
        public Guid Id { get; protected set; } = Guid.NewGuid();

        [NotMapped]
        private readonly List<INotification> _domainEvents = new();

        [NotMapped]
        public IReadOnlyCollection<INotification> DomainEvents => _domainEvents.AsReadOnly();

        public void AddDomainEvent(INotification eventItem)
        {
            _domainEvents.Add(eventItem);
        }

        public void RemoveDomainEvent(INotification eventItem)
        {
            _domainEvents.Remove(eventItem);
        }

        public void ClearDomainEvents()
        {
            _domainEvents.Clear();
        }

        public override bool Equals(object obj)
        {
            if (obj is not BaseEntity other)
                return false;

            if (ReferenceEquals(this, other))
                return true;

            if (GetType() != other.GetType())
                return false;

            return Id.Equals(other.Id);
        }

        public override int GetHashCode() => Id.GetHashCode();
    }
}

// Domain/ValueObjects/Email.cs
using System;
using System.Text.RegularExpressions;

namespace Domain.ValueObjects
{
    public class Email : IEquatable<Email>
    {
        private static readonly Regex EmailRegex = new(
            @"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
            RegexOptions.Compiled);

        public string Value { get; }

        public Email(string value)
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Email cannot be empty", nameof(value));

            if (!EmailRegex.IsMatch(value))
                throw new ArgumentException("Invalid email format", nameof(value));

            Value = value.ToLowerInvariant();
        }

        public override bool Equals(object obj) => Equals(obj as Email);

        public bool Equals(Email other) => other != null && Value == other.Value;

        public override int GetHashCode() => Value.GetHashCode();

        public override string ToString() => Value;

        public static implicit operator string(Email email) => email.Value;
        public static explicit operator Email(string email) => new(email);
    }
}
```

### Domain Events

```csharp
// Domain/Events/UserCreatedEvent.cs
using MediatR;

namespace Domain.Events
{
    public class UserCreatedEvent : INotification
    {
        public Guid UserId { get; }
        public string Email { get; }

        public UserCreatedEvent(Guid userId, string email)
        {
            UserId = userId;
            Email = email;
        }
    }
}

// Domain/Events/UserProfileUpdatedEvent.cs
using MediatR;

namespace Domain.Events
{
    public class UserProfileUpdatedEvent : INotification
    {
        public Guid UserId { get; }

        public UserProfileUpdatedEvent(Guid userId)
        {
            UserId = userId;
        }
    }
}
```

## Application Layer

### Commands and Queries (CQRS)

```csharp
// Application/Commands/CreateUserCommand.cs
using MediatR;

namespace Application.Commands
{
    public class CreateUserCommand : IRequest<Guid>
    {
        public string Email { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Password { get; set; }
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

        public async Task<Guid> Handle(CreateUserCommand request, CancellationToken cancellationToken)
        {
            _logger.LogInformation("Creating user with email {Email}", request.Email);

            // Check if user already exists
            var existingUser = await _userRepository.GetByEmailAsync(request.Email);
            if (existingUser != null)
            {
                throw new UserAlreadyExistsException(request.Email);
            }

            // Hash password
            var hashedPassword = _passwordHasher.HashPassword(request.Password);

            // Create user
            var user = new User(request.Email, request.FirstName, request.LastName);
            // Note: In real implementation, password would be set through a separate method
            // or handled by identity framework

            await _userRepository.AddAsync(user);
            await _userRepository.SaveChangesAsync();

            _logger.LogInformation("User created with ID {UserId}", user.Id);

            return user.Id;
        }
    }
}

// Application/Queries/GetUserQuery.cs
using MediatR;

namespace Application.Queries
{
    public class GetUserQuery : IRequest<UserDto>
    {
        public Guid UserId { get; set; }
    }
}

// Application/Queries/GetUserQueryHandler.cs
using System.Threading;
using System.Threading.Tasks;
using AutoMapper;
using Domain.Interfaces;
using MediatR;
using Microsoft.Extensions.Logging;

namespace Application.Queries
{
    public class GetUserQueryHandler : IRequestHandler<GetUserQuery, UserDto>
    {
        private readonly IUserRepository _userRepository;
        private readonly IMapper _mapper;
        private readonly ILogger<GetUserQueryHandler> _logger;

        public GetUserQueryHandler(
            IUserRepository userRepository,
            IMapper mapper,
            ILogger<GetUserQueryHandler> logger)
        {
            _userRepository = userRepository;
            _mapper = mapper;
            _logger = logger;
        }

        public async Task<UserDto> Handle(GetUserQuery request, CancellationToken cancellationToken)
        {
            _logger.LogInformation("Getting user with ID {UserId}", request.UserId);

            var user = await _userRepository.GetByIdAsync(request.UserId);
            if (user == null)
            {
                throw new UserNotFoundException(request.UserId);
            }

            return _mapper.Map<UserDto>(user);
        }
    }
}
```

### DTOs and Mapping

```csharp
// Application/DTOs/UserDto.cs
using System;

namespace Application.DTOs
{
    public class UserDto
    {
        public Guid Id { get; set; }
        public string Email { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string FullName { get; set; }
        public bool IsActive { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? LastLoginAt { get; set; }
    }
}

// Application/DTOs/CreateUserDto.cs
using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    public class CreateUserDto
    {
        [Required]
        [EmailAddress]
        [StringLength(256)]
        public string Email { get; set; }

        [Required]
        [StringLength(100)]
        public string FirstName { get; set; }

        [Required]
        [StringLength(100)]
        public string LastName { get; set; }

        [Required]
        [StringLength(100, MinimumLength = 8)]
        public string Password { get; set; }
    }
}

// Application/MappingProfiles/UserProfile.cs
using Application.DTOs;
using AutoMapper;
using Domain.Entities;

namespace Application.MappingProfiles
{
    public class UserProfile : Profile
    {
        public UserProfile()
        {
            CreateMap<User, UserDto>()
                .ForMember(dest => dest.FullName, opt => opt.MapFrom(src => src.GetFullName()));

            CreateMap<CreateUserDto, User>()
                .ForMember(dest => dest.Email, opt => opt.MapFrom(src => src.Email))
                .ForMember(dest => dest.FirstName, opt => opt.MapFrom(src => src.FirstName))
                .ForMember(dest => dest.LastName, opt => opt.MapFrom(src => src.LastName));
        }
    }
}
```

### Validation

```csharp
// Application/Validators/CreateUserDtoValidator.cs
using Application.DTOs;
using FluentValidation;
using Domain.Interfaces;

namespace Application.Validators
{
    public class CreateUserDtoValidator : AbstractValidator<CreateUserDto>
    {
        public CreateUserDtoValidator(IUserRepository userRepository)
        {
            RuleFor(x => x.Email)
                .NotEmpty().WithMessage("Email is required")
                .EmailAddress().WithMessage("Invalid email format")
                .MaximumLength(256).WithMessage("Email must not exceed 256 characters")
                .MustAsync(async (email, cancellation) =>
                {
                    var existingUser = await userRepository.GetByEmailAsync(email);
                    return existingUser == null;
                }).WithMessage("Email is already registered");

            RuleFor(x => x.FirstName)
                .NotEmpty().WithMessage("First name is required")
                .MaximumLength(100).WithMessage("First name must not exceed 100 characters")
                .Matches(@"^[a-zA-Z\s]+$").WithMessage("First name can only contain letters and spaces");

            RuleFor(x => x.LastName)
                .NotEmpty().WithMessage("Last name is required")
                .MaximumLength(100).WithMessage("Last name must not exceed 100 characters")
                .Matches(@"^[a-zA-Z\s]+$").WithMessage("Last name can only contain letters and spaces");

            RuleFor(x => x.Password)
                .NotEmpty().WithMessage("Password is required")
                .MinimumLength(8).WithMessage("Password must be at least 8 characters long")
                .MaximumLength(100).WithMessage("Password must not exceed 100 characters")
                .Matches(@"[A-Z]").WithMessage("Password must contain at least one uppercase letter")
                .Matches(@"[a-z]").WithMessage("Password must contain at least one lowercase letter")
                .Matches(@"[0-9]").WithMessage("Password must contain at least one number")
                .Matches(@"[^a-zA-Z0-9]").WithMessage("Password must contain at least one special character");
        }
    }
}
```

## Infrastructure Layer

### Repository Pattern

```csharp
// Infrastructure/Data/AppDbContext.cs
using Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<UserRole> UserRoles { get; set; }
        public DbSet<Role> Roles { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure entities
            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Email).IsRequired().HasMaxLength(256);
                entity.Property(e => e.FirstName).IsRequired().HasMaxLength(100);
                entity.Property(e => e.LastName).IsRequired().HasMaxLength(100);
                entity.Property(e => e.IsActive).HasDefaultValue(true);
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("GETUTCDATE()");

                entity.HasIndex(e => e.Email).IsUnique();

                // Configure relationships
                entity.HasMany(e => e.UserRoles)
                    .WithOne(ur => ur.User)
                    .HasForeignKey(ur => ur.UserId)
                    .OnDelete(DeleteBehavior.Cascade);
            });

            modelBuilder.Entity<Role>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Name).IsRequired().HasMaxLength(50);
                entity.Property(e => e.Description).HasMaxLength(500);

                entity.HasIndex(e => e.Name).IsUnique();
            });

            modelBuilder.Entity<UserRole>(entity =>
            {
                entity.HasKey(ur => new { ur.UserId, ur.RoleId });

                entity.HasOne(ur => ur.User)
                    .WithMany(u => u.UserRoles)
                    .HasForeignKey(ur => ur.UserId);

                entity.HasOne(ur => ur.Role)
                    .WithMany(r => r.UserRoles)
                    .HasForeignKey(ur => ur.RoleId);
            });
        }
    }
}

// Infrastructure/Repositories/UserRepository.cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.Entities;
using Domain.Interfaces;
using Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace Infrastructure.Repositories
{
    public class UserRepository : IUserRepository
    {
        private readonly AppDbContext _context;
        private readonly ILogger<UserRepository> _logger;

        public UserRepository(AppDbContext context, ILogger<UserRepository> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<User> GetByIdAsync(Guid id)
        {
            return await _context.Users
                .Include(u => u.UserRoles)
                .ThenInclude(ur => ur.Role)
                .FirstOrDefaultAsync(u => u.Id == id);
        }

        public async Task<User> GetByEmailAsync(string email)
        {
            return await _context.Users
                .Include(u => u.UserRoles)
                .ThenInclude(ur => ur.Role)
                .FirstOrDefaultAsync(u => u.Email == email);
        }

        public async Task<IEnumerable<User>> GetAllAsync()
        {
            return await _context.Users
                .Include(u => u.UserRoles)
                .ThenInclude(ur => ur.Role)
                .ToListAsync();
        }

        public async Task<IEnumerable<User>> GetActiveUsersAsync()
        {
            return await _context.Users
                .Where(u => u.IsActive)
                .Include(u => u.UserRoles)
                .ThenInclude(ur => ur.Role)
                .ToListAsync();
        }

        public async Task AddAsync(User user)
        {
            await _context.Users.AddAsync(user);
            _logger.LogInformation("User {UserId} added to repository", user.Id);
        }

        public void Update(User user)
        {
            _context.Users.Update(user);
            _logger.LogInformation("User {UserId} updated in repository", user.Id);
        }

        public void Delete(User user)
        {
            _context.Users.Remove(user);
            _logger.LogInformation("User {UserId} marked for deletion", user.Id);
        }

        public async Task<bool> ExistsAsync(Guid id)
        {
            return await _context.Users.AnyAsync(u => u.Id == id);
        }

        public async Task<int> SaveChangesAsync()
        {
            var result = await _context.SaveChangesAsync();
            _logger.LogInformation("Saved {Count} changes to database", result);
            return result;
        }
    }
}
```

### External Services

```csharp
// Infrastructure/External/EmailService.cs
using System.Net;
using System.Net.Mail;
using System.Threading.Tasks;
using Application.Interfaces;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Polly;
using Polly.Retry;

namespace Infrastructure.External
{
    public class EmailService : IEmailService
    {
        private readonly EmailSettings _emailSettings;
        private readonly ILogger<EmailService> _logger;
        private readonly AsyncRetryPolicy _retryPolicy;

        public EmailService(
            IOptions<EmailSettings> emailSettings,
            ILogger<EmailService> logger)
        {
            _emailSettings = emailSettings.Value;
            _logger = logger;

            // Configure retry policy for email sending
            _retryPolicy = Policy
                .Handle<Exception>()
                .WaitAndRetryAsync(
                    3,
                    retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
                    (exception, timeSpan, retryCount, context) =>
                    {
                        _logger.LogWarning(exception,
                            "Email sending failed. Retry {RetryCount} after {TimeSpan}",
                            retryCount, timeSpan);
                    });
        }

        public async Task SendEmailAsync(string to, string subject, string body)
        {
            await _retryPolicy.ExecuteAsync(async () =>
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
            });
        }

        public async Task SendWelcomeEmailAsync(string to, string userName)
        {
            var subject = "Welcome to Our Platform!";
            var body = $@"
                <h1>Welcome {userName}!</h1>
                <p>Thank you for joining our platform. Your account has been created successfully.</p>
                <p>You can now log in and start using our services.</p>
                <br>
                <p>Best regards,<br>The Team</p>
            ";

            await SendEmailAsync(to, subject, body);
        }

        public async Task SendPasswordResetEmailAsync(string to, string resetToken)
        {
            var subject = "Password Reset Request";
            var body = $@"
                <h1>Password Reset</h1>
                <p>You have requested to reset your password.</p>
                <p>Please use the following token to reset your password: <strong>{resetToken}</strong></p>
                <p>This token will expire in 24 hours.</p>
                <br>
                <p>If you didn't request this reset, please ignore this email.</p>
                <br>
                <p>Best regards,<br>The Team</p>
            ";

            await SendEmailAsync(to, subject, body);
        }
    }

    public class EmailSettings
    {
        public string SmtpServer { get; set; }
        public int Port { get; set; }
        public string Username { get; set; }
        public string Password { get; set; }
        public bool EnableSsl { get; set; }
        public string FromEmail { get; set; }
        public string FromName { get; set; }
    }
}
```

## API Layer

### Controllers

```csharp
// Api/Controllers/UsersController.cs
using System;
using System.Threading.Tasks;
using Application.Commands;
using Application.DTOs;
using Application.Queries;
using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class UsersController : ControllerBase
    {
        private readonly IMediator _mediator;
        private readonly ILogger<UsersController> _logger;

        public UsersController(IMediator mediator, ILogger<UsersController> logger)
        {
            _mediator = mediator;
            _logger = logger;
        }

        [HttpGet("{id}")]
        [ProducesResponseType(typeof(UserDto), 200)]
        [ProducesResponseType(404)]
        public async Task<ActionResult<UserDto>> GetUser(Guid id)
        {
            _logger.LogInformation("Getting user with ID {UserId}", id);

            var query = new GetUserQuery { UserId = id };
            var user = await _mediator.Send(query);

            return Ok(user);
        }

        [HttpPost]
        [AllowAnonymous]
        [ProducesResponseType(typeof(Guid), 201)]
        [ProducesResponseType(400)]
        public async Task<ActionResult<Guid>> CreateUser(CreateUserDto createUserDto)
        {
            _logger.LogInformation("Creating user with email {Email}", createUserDto.Email);

            var command = new CreateUserCommand
            {
                Email = createUserDto.Email,
                FirstName = createUserDto.FirstName,
                LastName = createUserDto.LastName,
                Password = createUserDto.Password
            };

            var userId = await _mediator.Send(command);

            _logger.LogInformation("User created with ID {UserId}", userId);

            return CreatedAtAction(nameof(GetUser), new { id = userId }, userId);
        }

        [HttpPut("{id}")]
        [ProducesResponseType(204)]
        [ProducesResponseType(404)]
        public async Task<IActionResult> UpdateUser(Guid id, UpdateUserDto updateUserDto)
        {
            _logger.LogInformation("Updating user {UserId}", id);

            var command = new UpdateUserCommand
            {
                UserId = id,
                FirstName = updateUserDto.FirstName,
                LastName = updateUserDto.LastName
            };

            await _mediator.Send(command);

            return NoContent();
        }

        [HttpDelete("{id}")]
        [ProducesResponseType(204)]
        [ProducesResponseType(404)]
        public async Task<IActionResult> DeleteUser(Guid id)
        {
            _logger.LogInformation("Deleting user {UserId}", id);

            var command = new DeleteUserCommand { UserId = id };
            await _mediator.Send(command);

            return NoContent();
        }
    }
}
```

### Middleware

```csharp
// Api/Middleware/ExceptionHandlingMiddleware.cs
using System;
using System.Net;
using System.Text.Json;
using System.Threading.Tasks;
using Application.Exceptions;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace Api.Middleware
{
    public class ExceptionHandlingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ExceptionHandlingMiddleware> _logger;

        public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
        {
            _next = next;
            _logger = logger;
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
            var (statusCode, errorCode, message) = exception switch
            {
                UserNotFoundException => ((int)HttpStatusCode.NotFound, "USER_NOT_FOUND", exception.Message),
                UserAlreadyExistsException => ((int)HttpStatusCode.Conflict, "USER_ALREADY_EXISTS", exception.Message),
                ValidationException => ((int)HttpStatusCode.BadRequest, "VALIDATION_ERROR", exception.Message),
                UnauthorizedAccessException => ((int)HttpStatusCode.Unauthorized, "UNAUTHORIZED", "Access denied"),
                _ => ((int)HttpStatusCode.InternalServerError, "INTERNAL_ERROR", "An unexpected error occurred")
            };

            _logger.LogError(exception, "An error occurred: {ErrorCode} - {Message}", errorCode, message);

            context.Response.ContentType = "application/json";
            context.Response.StatusCode = statusCode;

            var errorResponse = new
            {
                timestamp = DateTime.UtcNow,
                status = statusCode,
                error = errorCode,
                message = message,
                path = context.Request.Path
            };

            await context.Response.WriteAsync(JsonSerializer.Serialize(errorResponse));
        }
    }

    public static class ExceptionHandlingMiddlewareExtensions
    {
        public static IApplicationBuilder UseExceptionHandling(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<ExceptionHandlingMiddleware>();
        }
    }
}

// Api/Middleware/RequestLoggingMiddleware.cs
using System;
using System.Diagnostics;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace Api.Middleware
{
    public class RequestLoggingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<RequestLoggingMiddleware> _logger;

        public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            var stopwatch = Stopwatch.StartNew();

            _logger.LogInformation("Request started: {Method} {Path}",
                context.Request.Method, context.Request.Path);

            await _next(context);

            stopwatch.Stop();

            _logger.LogInformation("Request completed: {Method} {Path} - {StatusCode} in {ElapsedMs}ms",
                context.Request.Method, context.Request.Path, context.Response.StatusCode, stopwatch.ElapsedMilliseconds);
        }
    }

    public static class RequestLoggingMiddlewareExtensions
    {
        public static IApplicationBuilder UseRequestLogging(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<RequestLoggingMiddleware>();
        }
    }
}
```

### Program.cs and Startup

```csharp
// Api/Program.cs
using System;
using System.IO;
using Api.Middleware;
using Application.MappingProfiles;
using FluentValidation.AspNetCore;
using Infrastructure.Data;
using Infrastructure.External;
using MediatR;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .WriteTo.File("logs/log-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();

builder.Host.UseSerilog();

// Add services to the container
builder.Services.AddControllers()
    .AddFluentValidation(fv =>
    {
        fv.RegisterValidatorsFromAssemblyContaining<CreateUserDtoValidator>();
        fv.AutomaticValidationEnabled = false; // We'll handle validation manually
    });

// Add MediatR
builder.Services.AddMediatR(typeof(CreateUserCommand).Assembly);

// Add AutoMapper
builder.Services.AddAutoMapper(typeof(UserProfile).Assembly);

// Add DbContext
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Add repositories
builder.Services.AddScoped<IUserRepository, UserRepository>();

// Add external services
builder.Services.Configure<EmailSettings>(builder.Configuration.GetSection("Email"));
builder.Services.AddScoped<IEmailService, EmailService>();

// Add Swagger
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "User Management API",
        Version = "v1",
        Description = "API for managing users"
    });

    // Include XML comments
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    c.IncludeXmlComments(xmlPath);
});

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Add health checks
builder.Services.AddHealthChecks();

// Build the app
var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
    app.UseSwagger();
    app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "User Management API v1"));
}

app.UseHttpsRedirection();

// Custom middleware
app.UseExceptionHandling();
app.UseRequestLogging();

app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();
app.MapHealthChecks("/health");

try
{
    Log.Information("Starting web host");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Host terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}
```

### Filters

```csharp
// Api/Filters/ValidationFilter.cs
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace Api.Filters
{
    public class ValidationFilter : IActionFilter
    {
        public void OnActionExecuting(ActionExecutingContext context)
        {
            if (!context.ModelState.IsValid)
            {
                var errors = context.ModelState
                    .Where(ms => ms.Value.Errors.Any())
                    .ToDictionary(
                        kvp => kvp.Key,
                        kvp => kvp.Value.Errors.Select(e => e.ErrorMessage).ToArray()
                    );

                context.Result = new BadRequestObjectResult(new
                {
                    errorCode = "VALIDATION_ERROR",
                    message = "Validation failed",
                    errors = errors
                });
            }
        }

        public void OnActionExecuted(ActionExecutedContext context)
        {
            // No action needed after execution
        }
    }
}

// Api/Filters/GlobalExceptionFilter.cs
using System;
using Application.Exceptions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Logging;

namespace Api.Filters
{
    public class GlobalExceptionFilter : IExceptionFilter
    {
        private readonly ILogger<GlobalExceptionFilter> _logger;

        public GlobalExceptionFilter(ILogger<GlobalExceptionFilter> logger)
        {
            _logger = logger;
        }

        public void OnException(ExceptionContext context)
        {
            var exception = context.Exception;

            var (statusCode, errorCode, message) = exception switch
            {
                UserNotFoundException => (404, "USER_NOT_FOUND", exception.Message),
                UserAlreadyExistsException => (409, "USER_ALREADY_EXISTS", exception.Message),
                ValidationException => (400, "VALIDATION_ERROR", exception.Message),
                UnauthorizedAccessException => (401, "UNAUTHORIZED", "Access denied"),
                _ => (500, "INTERNAL_ERROR", "An unexpected error occurred")
            };

            _logger.LogError(exception, "An error occurred: {ErrorCode} - {Message}", errorCode, message);

            context.Result = new ObjectResult(new
            {
                timestamp = DateTime.UtcNow,
                status = statusCode,
                error = errorCode,
                message = message,
                path = context.HttpContext.Request.Path
            })
            {
                StatusCode = statusCode
            };

            context.ExceptionHandled = true;
        }
    }
}
```

This comprehensive guide covers ASP.NET Core patterns and best practices, including domain-driven design, CQRS with MediatR, repository pattern, dependency injection, middleware, filters, and enterprise application architecture.