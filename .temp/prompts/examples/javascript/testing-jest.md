# Jest Testing Patterns for JavaScript/TypeScript

This guide covers comprehensive testing patterns using Jest for JavaScript and TypeScript applications, including unit tests, integration tests, mocking strategies, and best practices.

## Project Setup and Configuration

### Jest Configuration with TypeScript

```javascript
// jest.config.js
module.exports = {
  // Test environment
  testEnvironment: 'node',
  testEnvironmentOptions: {
    NODE_ENV: 'test'
  },

  // Test files
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.test.(js|jsx|ts|tsx)',
    '<rootDir>/src/**/?(*.)(test|spec).(js|jsx|ts|tsx)',
    '<rootDir>/tests/**/*.test.(js|jsx|ts|tsx)'
  ],

  // Module resolution
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@services/(.*)$': '<rootDir>/src/services/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1'
  },

  // Transform files
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
    '^.+\\.(js|jsx)$': 'babel-jest'
  },

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],

  // Coverage
  collectCoverageFrom: [
    'src/**/*.(ts|tsx|js|jsx)',
    '!src/**/*.d.ts',
    '!src/index.ts',
    '!src/**/*.stories.(ts|tsx)'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html', 'json'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },

  // Test timeouts
  testTimeout: 10000,

  // Clear mocks between tests
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true,

  // Verbose output
  verbose: true,

  // Error handling
  bail: false,
  detectOpenHandles: true,
  forceExit: true,

  // Global setup/teardown
  globalSetup: '<rootDir>/tests/globalSetup.ts',
  globalTeardown: '<rootDir>/tests/globalTeardown.ts'
};
```

### Test Setup File

```typescript
// tests/setup.ts
import { jest } from '@jest/globals';

// Mock console methods to reduce noise during tests
global.console = {
  ...console,
  // Keep log and warn for debugging, suppress info and debug
  info: jest.fn(),
  debug: jest.fn(),
};

// Set up global test utilities
global.testUtils = {
  // Generate random test data
  generateId: () => Math.random().toString(36).substr(2, 9),

  // Create test user
  createTestUser: (overrides = {}) => ({
    id: global.testUtils.generateId(),
    name: 'Test User',
    email: 'test@example.com',
    role: 'user',
    createdAt: new Date(),
    ...overrides
  }),

  // Mock timers
  useFakeTimers: () => {
    jest.useFakeTimers();
    return () => jest.useRealTimers();
  },

  // Mock date
  mockDate: (date: Date) => {
    const originalDate = Date;
    global.Date = jest.fn(() => date) as any;
    global.Date.now = jest.fn(() => date.getTime());
    return () => {
      global.Date = originalDate;
    };
  }
};

// Custom matchers
expect.extend({
  toBeValidDate(received) {
    const pass = received instanceof Date && !isNaN(received.getTime());
    return {
      message: () => `expected ${received} to be a valid Date`,
      pass
    };
  },

  toBeValidEmail(received) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const pass = emailRegex.test(received);
    return {
      message: () => `expected ${received} to be a valid email`,
      pass
    };
  }
});

// Clean up after each test
afterEach(() => {
  jest.clearAllMocks();
  jest.clearAllTimers();
});

// Global error handler for unhandled rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});
```

## Unit Testing Patterns

### Testing Utility Functions

```typescript
// src/utils/stringUtils.ts
export const capitalize = (str: string): string => {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

export const truncate = (str: string, maxLength: number): string => {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - 3) + '...';
};

export const slugify = (str: string): string => {
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
};

// src/utils/__tests__/stringUtils.test.ts
import { capitalize, truncate, slugify } from '../stringUtils';

describe('String Utils', () => {
  describe('capitalize', () => {
    it('should capitalize the first letter of a string', () => {
      expect(capitalize('hello')).toBe('Hello');
      expect(capitalize('HELLO')).toBe('Hello');
      expect(capitalize('hELLO')).toBe('Hello');
    });

    it('should handle empty strings', () => {
      expect(capitalize('')).toBe('');
    });

    it('should handle single character strings', () => {
      expect(capitalize('a')).toBe('A');
      expect(capitalize('A')).toBe('A');
    });

    it('should handle strings with numbers and special characters', () => {
      expect(capitalize('123abc')).toBe('123abc');
      expect(capitalize('!hello')).toBe('!hello');
    });
  });

  describe('truncate', () => {
    it('should not truncate strings shorter than maxLength', () => {
      expect(truncate('hello', 10)).toBe('hello');
    });

    it('should truncate strings longer than maxLength', () => {
      expect(truncate('hello world', 8)).toBe('hello...');
      expect(truncate('this is a very long string', 10)).toBe('this is...');
    });

    it('should handle edge cases', () => {
      expect(truncate('', 5)).toBe('');
      expect(truncate('abc', 3)).toBe('abc');
      expect(truncate('abcd', 3)).toBe('a...');
    });
  });

  describe('slugify', () => {
    it('should convert strings to URL-friendly slugs', () => {
      expect(slugify('Hello World')).toBe('hello-world');
      expect(slugify('This is a TEST!')).toBe('this-is-a-test');
      expect(slugify('Multiple   Spaces')).toBe('multiple-spaces');
    });

    it('should handle special characters', () => {
      expect(slugify('Hello@World!')).toBe('helloworld');
      expect(slugify('Café & Restaurant')).toBe('cafe-restaurant');
    });

    it('should handle empty and whitespace strings', () => {
      expect(slugify('')).toBe('');
      expect(slugify('   ')).toBe('');
      expect(slugify('\t\n')).toBe('');
    });

    it('should remove leading and trailing hyphens', () => {
      expect(slugify('-hello-')).toBe('hello');
      expect(slugify('---hello---')).toBe('hello');
    });
  });
});
```

### Testing Classes with Dependencies

```typescript
// src/services/UserService.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  createdAt: Date;
}

export interface CreateUserData {
  name: string;
  email: string;
  password: string;
}

export class UserService {
  constructor(
    private userRepository: any,
    private passwordHasher: any,
    private emailService: any
  ) {}

  async createUser(userData: CreateUserData): Promise<User> {
    // Validate input
    if (!userData.name || !userData.email || !userData.password) {
      throw new Error('Name, email, and password are required');
    }

    // Check if user exists
    const existingUser = await this.userRepository.findByEmail(userData.email);
    if (existingUser) {
      throw new Error('User already exists');
    }

    // Hash password
    const hashedPassword = await this.passwordHasher.hash(userData.password);

    // Create user
    const user = await this.userRepository.create({
      ...userData,
      password: hashedPassword,
      role: 'user',
      createdAt: new Date()
    });

    // Send welcome email
    await this.emailService.sendWelcomeEmail(user.email, user.name);

    return user;
  }

  async authenticateUser(email: string, password: string): Promise<User | null> {
    const user = await this.userRepository.findByEmail(email);
    if (!user) return null;

    const isValid = await this.passwordHasher.verify(password, user.password);
    if (!isValid) return null;

    // Remove password from response
    const { password: _, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }
}

// src/services/__tests__/UserService.test.ts
import { UserService } from '../UserService';

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: any;
  let mockPasswordHasher: any;
  let mockEmailService: any;

  beforeEach(() => {
    // Create mocks
    mockUserRepository = {
      findByEmail: jest.fn(),
      create: jest.fn()
    };

    mockPasswordHasher = {
      hash: jest.fn(),
      verify: jest.fn()
    };

    mockEmailService = {
      sendWelcomeEmail: jest.fn()
    };

    // Create service with mocks
    userService = new UserService(
      mockUserRepository,
      mockPasswordHasher,
      mockEmailService
    );
  });

  describe('createUser', () => {
    const validUserData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    };

    it('should create a user successfully', async () => {
      // Arrange
      const hashedPassword = 'hashedPassword123';
      const createdUser = {
        id: 'user123',
        ...validUserData,
        password: hashedPassword,
        role: 'user',
        createdAt: new Date()
      };

      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockPasswordHasher.hash.mockResolvedValue(hashedPassword);
      mockUserRepository.create.mockResolvedValue(createdUser);
      mockEmailService.sendWelcomeEmail.mockResolvedValue(undefined);

      // Act
      const result = await userService.createUser(validUserData);

      // Assert
      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(validUserData.email);
      expect(mockPasswordHasher.hash).toHaveBeenCalledWith(validUserData.password);
      expect(mockUserRepository.create).toHaveBeenCalledWith({
        ...validUserData,
        password: hashedPassword,
        role: 'user',
        createdAt: expect.any(Date)
      });
      expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(
        validUserData.email,
        validUserData.name
      );
      expect(result).toEqual(createdUser);
    });

    it('should throw error if required fields are missing', async () => {
      // Test missing name
      await expect(userService.createUser({
        ...validUserData,
        name: ''
      })).rejects.toThrow('Name, email, and password are required');

      // Test missing email
      await expect(userService.createUser({
        ...validUserData,
        email: ''
      })).rejects.toThrow('Name, email, and password are required');

      // Test missing password
      await expect(userService.createUser({
        ...validUserData,
        password: ''
      })).rejects.toThrow('Name, email, and password are required');
    });

    it('should throw error if user already exists', async () => {
      // Arrange
      const existingUser = { id: 'existing', email: validUserData.email };
      mockUserRepository.findByEmail.mockResolvedValue(existingUser);

      // Act & Assert
      await expect(userService.createUser(validUserData))
        .rejects.toThrow('User already exists');

      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(validUserData.email);
      expect(mockPasswordHasher.hash).not.toHaveBeenCalled();
    });

    it('should handle password hashing errors', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockPasswordHasher.hash.mockRejectedValue(new Error('Hashing failed'));

      // Act & Assert
      await expect(userService.createUser(validUserData))
        .rejects.toThrow('Hashing failed');

      expect(mockEmailService.sendWelcomeEmail).not.toHaveBeenCalled();
    });
  });

  describe('authenticateUser', () => {
    const validCredentials = {
      email: 'john@example.com',
      password: 'password123'
    };

    it('should authenticate user successfully', async () => {
      // Arrange
      const user = {
        id: 'user123',
        name: 'John Doe',
        email: validCredentials.email,
        password: 'hashedPassword',
        role: 'user'
      };

      mockUserRepository.findByEmail.mockResolvedValue(user);
      mockPasswordHasher.verify.mockResolvedValue(true);

      // Act
      const result = await userService.authenticateUser(
        validCredentials.email,
        validCredentials.password
      );

      // Assert
      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(validCredentials.email);
      expect(mockPasswordHasher.verify).toHaveBeenCalledWith(
        validCredentials.password,
        user.password
      );
      expect(result).toEqual({
        id: 'user123',
        name: 'John Doe',
        email: validCredentials.email,
        role: 'user'
      });
      expect(result).not.toHaveProperty('password');
    });

    it('should return null if user does not exist', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockResolvedValue(null);

      // Act
      const result = await userService.authenticateUser(
        validCredentials.email,
        validCredentials.password
      );

      // Assert
      expect(result).toBeNull();
      expect(mockPasswordHasher.verify).not.toHaveBeenCalled();
    });

    it('should return null if password is invalid', async () => {
      // Arrange
      const user = {
        id: 'user123',
        email: validCredentials.email,
        password: 'hashedPassword'
      };

      mockUserRepository.findByEmail.mockResolvedValue(user);
      mockPasswordHasher.verify.mockResolvedValue(false);

      // Act
      const result = await userService.authenticateUser(
        validCredentials.email,
        validCredentials.password
      );

      // Assert
      expect(result).toBeNull();
    });
  });
});
```

## Integration Testing Patterns

### Testing Express Routes

```typescript
// src/routes/userRoutes.ts
import express from 'express';
import { UserService } from '../services/UserService';

const router = express.Router();
const userService = new UserService(); // Injected in real app

router.post('/users', async (req, res) => {
  try {
    const user = await userService.createUser(req.body);
    res.status(201).json({ success: true, data: user });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});

router.get('/users/:id', async (req, res) => {
  try {
    const user = await userService.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ success: false, error: 'User not found' });
    }
    res.json({ success: true, data: user });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

export default router;

// tests/integration/userRoutes.test.ts
import request from 'supertest';
import express from 'express';
import userRoutes from '../../src/routes/userRoutes';

// Mock the UserService
jest.mock('../../src/services/UserService');
import { UserService } from '../../src/services/UserService';

describe('User Routes Integration', () => {
  let app: express.Application;
  let mockUserService: jest.Mocked<UserService>;

  beforeEach(() => {
    // Clear all mocks
    jest.clearAllMocks();

    // Create Express app
    app = express();
    app.use(express.json());
    app.use('/api', userRoutes);

    // Get the mocked service
    mockUserService = UserService.prototype as jest.Mocked<UserService>;
  });

  describe('POST /api/users', () => {
    const validUserData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    };

    it('should create a user successfully', async () => {
      // Arrange
      const createdUser = {
        id: 'user123',
        ...validUserData,
        role: 'user',
        createdAt: new Date()
      };

      mockUserService.createUser.mockResolvedValue(createdUser);

      // Act
      const response = await request(app)
        .post('/api/users')
        .send(validUserData)
        .expect(201);

      // Assert
      expect(response.body).toEqual({
        success: true,
        data: createdUser
      });
      expect(mockUserService.createUser).toHaveBeenCalledWith(validUserData);
    });

    it('should handle validation errors', async () => {
      // Arrange
      const invalidUserData = {
        name: '',
        email: 'invalid-email',
        password: '123'
      };

      mockUserService.createUser.mockRejectedValue(
        new Error('Name, email, and password are required')
      );

      // Act
      const response = await request(app)
        .post('/api/users')
        .send(invalidUserData)
        .expect(400);

      // Assert
      expect(response.body).toEqual({
        success: false,
        error: 'Name, email, and password are required'
      });
    });

    it('should handle malformed JSON', async () => {
      // Act
      const response = await request(app)
        .post('/api/users')
        .set('Content-Type', 'application/json')
        .send('{ invalid json }')
        .expect(400);

      // Assert
      expect(response.body.success).toBe(false);
      expect(response.body.error).toBeDefined();
    });
  });

  describe('GET /api/users/:id', () => {
    it('should return user when found', async () => {
      // Arrange
      const user = {
        id: 'user123',
        name: 'John Doe',
        email: 'john@example.com',
        role: 'user'
      };

      mockUserService.getUserById.mockResolvedValue(user);

      // Act
      const response = await request(app)
        .get('/api/users/user123')
        .expect(200);

      // Assert
      expect(response.body).toEqual({
        success: true,
        data: user
      });
      expect(mockUserService.getUserById).toHaveBeenCalledWith('user123');
    });

    it('should return 404 when user not found', async () => {
      // Arrange
      mockUserService.getUserById.mockResolvedValue(null);

      // Act
      const response = await request(app)
        .get('/api/users/nonexistent')
        .expect(404);

      // Assert
      expect(response.body).toEqual({
        success: false,
        error: 'User not found'
      });
    });

    it('should handle service errors', async () => {
      // Arrange
      mockUserService.getUserById.mockRejectedValue(
        new Error('Database connection failed')
      );

      // Act
      const response = await request(app)
        .get('/api/users/user123')
        .expect(500);

      // Assert
      expect(response.body).toEqual({
        success: false,
        error: 'Database connection failed'
      });
    });
  });
});
```

## Mocking Patterns

### HTTP Request Mocking

```typescript
// src/services/ApiClient.ts
export class ApiClient {
  constructor(private baseUrl: string, private apiKey: string) {}

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }
}

// src/services/__tests__/ApiClient.test.ts
import { ApiClient } from '../ApiClient';

// Mock fetch globally
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe('ApiClient', () => {
  let apiClient: ApiClient;
  const baseUrl = 'https://api.example.com';
  const apiKey = 'test-api-key';

  beforeEach(() => {
    apiClient = new ApiClient(baseUrl, apiKey);
    mockFetch.mockClear();
  });

  describe('get', () => {
    it('should make GET request with correct headers', async () => {
      // Arrange
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({ data: 'test' })
      };
      mockFetch.mockResolvedValue(mockResponse);

      // Act
      const result = await apiClient.get('/users');

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`${baseUrl}/users`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      });
      expect(mockResponse.json).toHaveBeenCalled();
      expect(result).toEqual({ data: 'test' });
    });

    it('should throw error for non-200 responses', async () => {
      // Arrange
      const mockResponse = {
        ok: false,
        status: 404,
        statusText: 'Not Found'
      };
      mockFetch.mockResolvedValue(mockResponse);

      // Act & Assert
      await expect(apiClient.get('/users')).rejects.toThrow('HTTP 404: Not Found');
    });

    it('should handle network errors', async () => {
      // Arrange
      mockFetch.mockRejectedValue(new Error('Network error'));

      // Act & Assert
      await expect(apiClient.get('/users')).rejects.toThrow('Network error');
    });
  });

  describe('post', () => {
    it('should make POST request with correct headers and body', async () => {
      // Arrange
      const requestData = { name: 'John', email: 'john@example.com' };
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({ id: 'user123', ...requestData })
      };
      mockFetch.mockResolvedValue(mockResponse);

      // Act
      const result = await apiClient.post('/users', requestData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`${baseUrl}/users`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });
      expect(result).toEqual({ id: 'user123', ...requestData });
    });
  });
});
```

### Database Mocking

```typescript
// src/repositories/UserRepository.ts
export interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  role: string;
  createdAt: Date;
}

export class UserRepository {
  constructor(private db: any) {} // Database connection

  async create(userData: Omit<User, 'id' | 'createdAt'>): Promise<User> {
    const user: User = {
      ...userData,
      id: this.generateId(),
      createdAt: new Date()
    };

    await this.db.collection('users').insertOne(user);
    return user;
  }

  async findById(id: string): Promise<User | null> {
    return await this.db.collection('users').findOne({ id });
  }

  async findByEmail(email: string): Promise<User | null> {
    return await this.db.collection('users').findOne({ email });
  }

  async update(id: string, updateData: Partial<User>): Promise<User> {
    const result = await this.db.collection('users').findOneAndUpdate(
      { id },
      { $set: { ...updateData, updatedAt: new Date() } },
      { returnDocument: 'after' }
    );

    if (!result.value) {
      throw new Error('User not found');
    }

    return result.value;
  }

  private generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }
}

// src/repositories/__tests__/UserRepository.test.ts
import { UserRepository } from '../UserRepository';

describe('UserRepository', () => {
  let userRepository: UserRepository;
  let mockDb: any;
  let mockCollection: any;

  beforeEach(() => {
    // Create mock database
    mockCollection = {
      insertOne: jest.fn(),
      findOne: jest.fn(),
      findOneAndUpdate: jest.fn()
    };

    mockDb = {
      collection: jest.fn().mockReturnValue(mockCollection)
    };

    userRepository = new UserRepository(mockDb);
  });

  describe('create', () => {
    it('should create a user and return it', async () => {
      // Arrange
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'hashedPassword',
        role: 'user'
      };

      const insertedUser = {
        ...userData,
        id: expect.any(String),
        createdAt: expect.any(Date)
      };

      mockCollection.insertOne.mockResolvedValue({ acknowledged: true });

      // Act
      const result = await userRepository.create(userData);

      // Assert
      expect(mockDb.collection).toHaveBeenCalledWith('users');
      expect(mockCollection.insertOne).toHaveBeenCalledWith(insertedUser);
      expect(result).toMatchObject({
        ...userData,
        id: expect.any(String),
        createdAt: expect.any(Date)
      });
    });

    it('should handle database errors', async () => {
      // Arrange
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'hashedPassword',
        role: 'user'
      };

      mockCollection.insertOne.mockRejectedValue(new Error('Database error'));

      // Act & Assert
      await expect(userRepository.create(userData)).rejects.toThrow('Database error');
    });
  });

  describe('findById', () => {
    it('should return user when found', async () => {
      // Arrange
      const userId = 'user123';
      const user = {
        id: userId,
        name: 'John Doe',
        email: 'john@example.com',
        password: 'hashedPassword',
        role: 'user',
        createdAt: new Date()
      };

      mockCollection.findOne.mockResolvedValue(user);

      // Act
      const result = await userRepository.findById(userId);

      // Assert
      expect(mockCollection.findOne).toHaveBeenCalledWith({ id: userId });
      expect(result).toEqual(user);
    });

    it('should return null when user not found', async () => {
      // Arrange
      mockCollection.findOne.mockResolvedValue(null);

      // Act
      const result = await userRepository.findById('nonexistent');

      // Assert
      expect(result).toBeNull();
    });
  });

  describe('findByEmail', () => {
    it('should return user when found by email', async () => {
      // Arrange
      const email = 'john@example.com';
      const user = {
        id: 'user123',
        name: 'John Doe',
        email,
        password: 'hashedPassword',
        role: 'user'
      };

      mockCollection.findOne.mockResolvedValue(user);

      // Act
      const result = await userRepository.findByEmail(email);

      // Assert
      expect(mockCollection.findOne).toHaveBeenCalledWith({ email });
      expect(result).toEqual(user);
    });
  });

  describe('update', () => {
    it('should update user and return updated version', async () => {
      // Arrange
      const userId = 'user123';
      const updateData = { name: 'Jane Doe', role: 'admin' };
      const updatedUser = {
        id: userId,
        name: 'Jane Doe',
        email: 'john@example.com',
        password: 'hashedPassword',
        role: 'admin',
        createdAt: new Date(),
        updatedAt: new Date()
      };

      mockCollection.findOneAndUpdate.mockResolvedValue({
        value: updatedUser
      });

      // Act
      const result = await userRepository.update(userId, updateData);

      // Assert
      expect(mockCollection.findOneAndUpdate).toHaveBeenCalledWith(
        { id: userId },
        { $set: { ...updateData, updatedAt: expect.any(Date) } },
        { returnDocument: 'after' }
      );
      expect(result).toEqual(updatedUser);
    });

    it('should throw error when user not found', async () => {
      // Arrange
      mockCollection.findOneAndUpdate.mockResolvedValue({ value: null });

      // Act & Assert
      await expect(userRepository.update('nonexistent', { name: 'Test' }))
        .rejects.toThrow('User not found');
    });
  });
});
```

## Testing React Components (with React Testing Library)

```typescript
// src/components/UserProfile.tsx
import React, { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface UserProfileProps {
  userId: string;
  onEdit?: (user: User) => void;
  onDelete?: (userId: string) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({
  userId,
  onEdit,
  onDelete
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        // In real app, this would be an API call
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch user');
        }
        const userData = await response.json();
        setUser(userData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  if (loading) {
    return <div data-testid="loading">Loading...</div>;
  }

  if (error) {
    return <div data-testid="error" role="alert">{error}</div>;
  }

  if (!user) {
    return <div data-testid="not-found">User not found</div>;
  }

  return (
    <div data-testid="user-profile">
      <h2>{user.name}</h2>
      <p data-testid="user-email">{user.email}</p>
      <p data-testid="user-role">Role: {user.role}</p>

      <div>
        {onEdit && (
          <button
            data-testid="edit-button"
            onClick={() => onEdit(user)}
          >
            Edit
          </button>
        )}

        {onDelete && (
          <button
            data-testid="delete-button"
            onClick={() => onDelete(user.id)}
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
};

// src/components/__tests__/UserProfile.test.tsx
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { UserProfile } from '../UserProfile';

// Mock fetch
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe('UserProfile', () => {
  const mockUser = {
    id: 'user123',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin'
  };

  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('should show loading state initially', () => {
    // Arrange
    mockFetch.mockImplementation(() => new Promise(() => {})); // Never resolves

    // Act
    render(<UserProfile userId="user123" />);

    // Assert
    expect(screen.getByTestId('loading')).toBeInTheDocument();
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should display user information when loaded successfully', async () => {
    // Arrange
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockUser)
    });

    // Act
    render(<UserProfile userId="user123" />);

    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('user-profile')).toBeInTheDocument();
    });

    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('John Doe');
    expect(screen.getByTestId('user-email')).toHaveTextContent('john@example.com');
    expect(screen.getByTestId('user-role')).toHaveTextContent('Role: admin');
  });

  it('should show error message when fetch fails', async () => {
    // Arrange
    mockFetch.mockResolvedValueOnce({
      ok: false,
      statusText: 'Not Found'
    });

    // Act
    render(<UserProfile userId="user123" />);

    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('error')).toBeInTheDocument();
    });

    expect(screen.getByRole('alert')).toHaveTextContent('Failed to fetch user');
  });

  it('should show not found message when user is null', async () => {
    // Arrange
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(null)
    });

    // Act
    render(<UserProfile userId="user123" />);

    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('not-found')).toBeInTheDocument();
    });

    expect(screen.getByText('User not found')).toBeInTheDocument();
  });

  it('should call onEdit when edit button is clicked', async () => {
    // Arrange
    const mockOnEdit = jest.fn();
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockUser)
    });

    // Act
    render(<UserProfile userId="user123" onEdit={mockOnEdit} />);

    await waitFor(() => {
      expect(screen.getByTestId('user-profile')).toBeInTheDocument();
    });

    const editButton = screen.getByTestId('edit-button');
    fireEvent.click(editButton);

    // Assert
    expect(mockOnEdit).toHaveBeenCalledWith(mockUser);
  });

  it('should call onDelete when delete button is clicked', async () => {
    // Arrange
    const mockOnDelete = jest.fn();
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockUser)
    });

    // Act
    render(<UserProfile userId="user123" onDelete={mockOnDelete} />);

    await waitFor(() => {
      expect(screen.getByTestId('user-profile')).toBeInTheDocument();
    });

    const deleteButton = screen.getByTestId('delete-button');
    fireEvent.click(deleteButton);

    // Assert
    expect(mockOnDelete).toHaveBeenCalledWith('user123');
  });

  it('should not show edit/delete buttons when handlers not provided', async () => {
    // Arrange
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockUser)
    });

    // Act
    render(<UserProfile userId="user123" />);

    await waitFor(() => {
      expect(screen.getByTestId('user-profile')).toBeInTheDocument();
    });

    // Assert
    expect(screen.queryByTestId('edit-button')).not.toBeInTheDocument();
    expect(screen.queryByTestId('delete-button')).not.toBeInTheDocument();
  });

  it('should refetch user when userId changes', async () => {
    // Arrange
    const { rerender } = render(<UserProfile userId="user123" />);
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockUser)
    });

    await waitFor(() => {
      expect(screen.getByTestId('user-profile')).toBeInTheDocument();
    });

    // Act - change userId
    const newUser = { ...mockUser, id: 'user456', name: 'Jane Doe' };
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(newUser)
    });

    rerender(<UserProfile userId="user456" />);

    // Assert
    await waitFor(() => {
      expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Jane Doe');
    });

    expect(mockFetch).toHaveBeenCalledTimes(2);
  });
});
```

This comprehensive guide covers Jest testing patterns for JavaScript/TypeScript applications, including unit tests, integration tests, mocking strategies, and React component testing with React Testing Library.