# Node.js API Patterns

This guide covers comprehensive patterns for building robust Node.js APIs, focusing on Express.js, middleware patterns, error handling, and best practices for scalable backend services.

## Express.js Application Structure

### Base API Server with TypeScript

```typescript
import express, { Request, Response, NextFunction, Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import { createServer, Server } from 'http';

// Types
interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  meta?: {
    timestamp: string;
    requestId: string;
    pagination?: {
      page: number;
      limit: number;
      total: number;
      totalPages: number;
    };
  };
}

interface ApiError extends Error {
  statusCode: number;
  errorCode: string;
  details?: any;
}

// Custom error classes
export class ValidationError extends Error implements ApiError {
  statusCode = 400;
  errorCode = 'VALIDATION_ERROR';

  constructor(message: string, details?: any) {
    super(message);
    this.name = 'ValidationError';
    this.details = details;
  }
}

export class NotFoundError extends Error implements ApiError {
  statusCode = 404;
  errorCode = 'NOT_FOUND';

  constructor(resource: string) {
    super(`${resource} not found`);
    this.name = 'NotFoundError';
  }
}

export class AuthenticationError extends Error implements ApiError {
  statusCode = 401;
  errorCode = 'AUTHENTICATION_ERROR';

  constructor(message: string = 'Authentication required') {
    super(message);
    this.name = 'AuthenticationError';
  }
}

// Middleware
const requestIdMiddleware = (req: Request, res: Response, next: NextFunction) => {
  req.id = req.headers['x-request-id'] as string || generateRequestId();
  res.setHeader('x-request-id', req.id);
  next();
};

const errorHandlerMiddleware = (
  error: ApiError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const statusCode = error.statusCode || 500;
  const errorCode = error.errorCode || 'INTERNAL_ERROR';

  const response: ApiResponse = {
    success: false,
    error: {
      code: errorCode,
      message: error.message,
      details: error.details
    },
    meta: {
      timestamp: new Date().toISOString(),
      requestId: req.id
    }
  };

  // Log error
  console.error(`[${req.id}] ${statusCode} ${errorCode}: ${error.message}`, {
    stack: error.stack,
    details: error.details,
    url: req.url,
    method: req.method,
    ip: req.ip
  });

  res.status(statusCode).json(response);
};

const asyncHandler = (fn: Function) => (req: Request, res: Response, next: NextFunction) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// Main application class
export class ApiServer {
  private app: Application;
  private server: Server | null = null;
  private port: number;

  constructor(port: number = 3000) {
    this.port = port;
    this.app = express();

    this.setupMiddleware();
    this.setupRoutes();
    this.setupErrorHandling();
  }

  private setupMiddleware(): void {
    // Security middleware
    this.app.use(helmet());

    // CORS
    this.app.use(cors({
      origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
      credentials: true
    }));

    // Compression
    this.app.use(compression());

    // Body parsing
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true }));

    // Request ID
    this.app.use(requestIdMiddleware);

    // Logging
    this.app.use(morgan('combined', {
      stream: {
        write: (message: string) => {
          console.log(`[${new Date().toISOString()}] ${message.trim()}`);
        }
      }
    }));
  }

  private setupRoutes(): void {
    // Health check
    this.app.get('/health', (req: Request, res: Response) => {
      res.json({
        success: true,
        data: { status: 'healthy', timestamp: new Date().toISOString() },
        meta: { requestId: req.id }
      });
    });

    // API routes
    this.app.use('/api/v1', this.createApiRouter());

    // 404 handler
    this.app.use('*', (req: Request, res: Response) => {
      throw new NotFoundError('Route');
    });
  }

  private createApiRouter(): express.Router {
    const router = express.Router();

    // User routes
    router.get('/users', asyncHandler(this.getUsers));
    router.get('/users/:id', asyncHandler(this.getUser));
    router.post('/users', asyncHandler(this.createUser));
    router.put('/users/:id', asyncHandler(this.updateUser));
    router.delete('/users/:id', asyncHandler(this.deleteUser));

    return router;
  }

  private setupErrorHandling(): void {
    this.app.use(errorHandlerMiddleware);
  }

  // Route handlers
  private async getUsers(req: Request, res: Response): Promise<void> {
    const { page = 1, limit = 10, search } = req.query;

    const users = await this.userService.getUsers({
      page: Number(page),
      limit: Number(limit),
      search: search as string
    });

    const response: ApiResponse = {
      success: true,
      data: users.data,
      meta: {
        timestamp: new Date().toISOString(),
        requestId: req.id,
        pagination: users.pagination
      }
    };

    res.json(response);
  }

  private async getUser(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const user = await this.userService.getUserById(id);

    if (!user) {
      throw new NotFoundError('User');
    }

    const response: ApiResponse = {
      success: true,
      data: user,
      meta: {
        timestamp: new Date().toISOString(),
        requestId: req.id
      }
    };

    res.json(response);
  }

  private async createUser(req: Request, res: Response): Promise<void> {
    const userData = req.body;

    // Validate input
    this.validateUserData(userData);

    const user = await this.userService.createUser(userData);

    const response: ApiResponse = {
      success: true,
      data: user,
      meta: {
        timestamp: new Date().toISOString(),
        requestId: req.id
      }
    };

    res.status(201).json(response);
  }

  private async updateUser(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const userData = req.body;

    // Check if user exists
    const existingUser = await this.userService.getUserById(id);
    if (!existingUser) {
      throw new NotFoundError('User');
    }

    // Validate input
    this.validateUserData(userData, true);

    const user = await this.userService.updateUser(id, userData);

    const response: ApiResponse = {
      success: true,
      data: user,
      meta: {
        timestamp: new Date().toISOString(),
        requestId: req.id
      }
    };

    res.json(response);
  }

  private async deleteUser(req: Request, res: Response): Promise<void> {
    const { id } = req.params;

    // Check if user exists
    const existingUser = await this.userService.getUserById(id);
    if (!existingUser) {
      throw new NotFoundError('User');
    }

    await this.userService.deleteUser(id);

    const response: ApiResponse = {
      success: true,
      data: { message: 'User deleted successfully' },
      meta: {
        timestamp: new Date().toISOString(),
        requestId: req.id
      }
    };

    res.json(response);
  }

  private validateUserData(data: any, isUpdate: boolean = false): void {
    const errors: string[] = [];

    if (!isUpdate || data.name !== undefined) {
      if (!data.name || typeof data.name !== 'string' || data.name.trim().length < 2) {
        errors.push('Name must be a string with at least 2 characters');
      }
    }

    if (!isUpdate || data.email !== undefined) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!data.email || !emailRegex.test(data.email)) {
        errors.push('Valid email is required');
      }
    }

    if (errors.length > 0) {
      throw new ValidationError('Validation failed', { errors });
    }
  }

  // Placeholder for user service - would be injected in real implementation
  private userService = {
    getUsers: async (params: any) => ({ data: [], pagination: {} }),
    getUserById: async (id: string) => null,
    createUser: async (data: any) => data,
    updateUser: async (id: string, data: any) => data,
    deleteUser: async (id: string) => {}
  };

  public start(): void {
    this.server = this.app.listen(this.port, () => {
      console.log(`API Server listening on port ${this.port}`);
    });
  }

  public stop(): void {
    if (this.server) {
      this.server.close();
      console.log('API Server stopped');
    }
  }

  public getApp(): Application {
    return this.app;
  }
}

// Factory function
export const createServer = (port?: number): ApiServer => {
  return new ApiServer(port);
};

// Utility functions
const generateRequestId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});
```

## Middleware Patterns

### Authentication Middleware

```typescript
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

interface AuthenticatedUser {
  id: string;
  email: string;
  role: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: AuthenticatedUser;
    }
  }
}

export const authenticateToken = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    throw new AuthenticationError('Access token required');
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as AuthenticatedUser;
    req.user = decoded;
    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new AuthenticationError('Token expired');
    } else if (error instanceof jwt.JsonWebTokenError) {
      throw new AuthenticationError('Invalid token');
    } else {
      throw new AuthenticationError('Token verification failed');
    }
  }
};

export const requireRole = (allowedRoles: string[]) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user) {
      throw new AuthenticationError('Authentication required');
    }

    if (!allowedRoles.includes(req.user.role)) {
      throw new AuthorizationError('Insufficient permissions');
    }

    next();
  };
};

export const optionalAuth = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1];

  if (token) {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as AuthenticatedUser;
      req.user = decoded;
    } catch (error) {
      // Ignore auth errors for optional auth
      console.warn('Optional auth failed:', error.message);
    }
  }

  next();
};
```

### Rate Limiting Middleware

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { createClient } from 'redis';

// Memory store for development
const createMemoryStore = () => {
  const store = new Map<string, { count: number; resetTime: number }>();

  return {
    increment: (key: string) => {
      const now = Date.now();
      const record = store.get(key);

      if (!record || now > record.resetTime) {
        store.set(key, { count: 1, resetTime: now + 15 * 60 * 1000 }); // 15 minutes
        return { count: 1, resetTime: now + 15 * 60 * 1000 };
      }

      record.count++;
      return { count: record.count, resetTime: record.resetTime };
    },
    decrement: (key: string) => {
      const record = store.get(key);
      if (record) {
        record.count = Math.max(0, record.count - 1);
      }
    }
  };
};

// Rate limiting configurations
export const createRateLimiter = (options: {
  windowMs: number;
  max: number;
  message?: string;
  skipSuccessfulRequests?: boolean;
  skipFailedRequests?: boolean;
}) => {
  const config = {
    windowMs: options.windowMs,
    max: options.max,
    message: options.message || {
      success: false,
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Too many requests, please try again later'
      }
    },
    standardHeaders: true,
    legacyHeaders: false,
    skipSuccessfulRequests: options.skipSuccessfulRequests || false,
    skipFailedRequests: options.skipFailedRequests || false,
    // Use Redis in production, memory store in development
    store: process.env.NODE_ENV === 'production'
      ? new RedisStore({
          sendCommand: (...args: string[]) => redisClient.call(...args),
        })
      : createMemoryStore()
  };

  return rateLimit(config);
};

// Pre-configured rate limiters
export const strictRateLimit = createRateLimiter({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: {
    success: false,
    error: {
      code: 'STRICT_RATE_LIMIT_EXCEEDED',
      message: 'Too many requests. Please wait 15 minutes before trying again.'
    }
  }
});

export const apiRateLimit = createRateLimiter({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000,
  skipSuccessfulRequests: false,
  skipFailedRequests: false
});

export const authRateLimit = createRateLimiter({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Very strict for auth endpoints
  message: {
    success: false,
    error: {
      code: 'AUTH_RATE_LIMIT_EXCEEDED',
      message: 'Too many authentication attempts. Please wait 15 minutes.'
    }
  },
  skipFailedRequests: false // Count failed attempts
});

// Redis client for production
let redisClient: any;
if (process.env.NODE_ENV === 'production') {
  redisClient = createClient({ url: process.env.REDIS_URL });
  redisClient.connect().catch(console.error);
}
```

### Validation Middleware

```typescript
import Joi from 'joi';
import { Request, Response, NextFunction } from 'express';

// Validation schemas
const userCreateSchema = Joi.object({
  name: Joi.string().min(2).max(100).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  role: Joi.string().valid('user', 'admin').default('user')
});

const userUpdateSchema = Joi.object({
  name: Joi.string().min(2).max(100),
  email: Joi.string().email(),
  role: Joi.string().valid('user', 'admin')
}).min(1); // At least one field required

const paginationSchema = Joi.object({
  page: Joi.number().integer().min(1).default(1),
  limit: Joi.number().integer().min(1).max(100).default(10),
  sort: Joi.string().pattern(/^[a-zA-Z_]+:(asc|desc)$/)
});

// Validation middleware factory
export const validateRequest = (schema: Joi.ObjectSchema, property: 'body' | 'query' | 'params' = 'body') => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const { error, value } = schema.validate(req[property], {
      abortEarly: false,
      stripUnknown: true
    });

    if (error) {
      const errors = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message
      }));

      throw new ValidationError('Request validation failed', { errors });
    }

    // Replace request data with validated/sanitized data
    req[property] = value;
    next();
  };
};

// Pre-built validation middleware
export const validateUserCreate = validateRequest(userCreateSchema);
export const validateUserUpdate = validateRequest(userUpdateSchema);
export const validatePagination = validateRequest(paginationSchema, 'query');

// Custom validation for complex business rules
export const validateBusinessRules = (rules: Array<(data: any) => string | null>) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const errors: string[] = [];

    for (const rule of rules) {
      const error = rule(req.body);
      if (error) {
        errors.push(error);
      }
    }

    if (errors.length > 0) {
      throw new ValidationError('Business rule validation failed', { errors });
    }

    next();
  };
};

// Example business rules
const userBusinessRules = [
  (data: any) => {
    // Check if email domain is allowed
    const allowedDomains = ['company.com', 'gmail.com'];
    const emailDomain = data.email.split('@')[1];
    return allowedDomains.includes(emailDomain) ? null : 'Email domain not allowed';
  },
  (data: any) => {
    // Check password strength
    const hasUpperCase = /[A-Z]/.test(data.password);
    const hasLowerCase = /[a-z]/.test(data.password);
    const hasNumbers = /\d/.test(data.password);
    const hasSpecialChar = /[!@#$%^&*]/.test(data.password);

    return (hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar)
      ? null
      : 'Password must contain uppercase, lowercase, number, and special character';
  }
];

export const validateUserBusinessRules = validateBusinessRules(userBusinessRules);
```

## Service Layer Patterns

### Base Service Class

```typescript
import { EventEmitter } from 'events';

export abstract class BaseService extends EventEmitter {
  protected logger: Console;

  constructor() {
    super();
    this.logger = console;
  }

  protected logInfo(message: string, meta?: any): void {
    this.logger.log(`[INFO] ${this.constructor.name}: ${message}`, meta || '');
  }

  protected logError(message: string, error?: Error): void {
    this.logger.error(`[ERROR] ${this.constructor.name}: ${message}`, error?.stack || '');
  }

  protected logWarn(message: string, meta?: any): void {
    this.logger.warn(`[WARN] ${this.constructor.name}: ${message}`, meta || '');
  }

  protected emitEvent(event: string, data: any): void {
    this.emit(event, data);
    this.logInfo(`Event emitted: ${event}`, data);
  }
}
```

### User Service Implementation

```typescript
import { BaseService } from './BaseService';
import { ValidationError, NotFoundError } from '../errors';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  createdAt: Date;
  updatedAt: Date;
}

interface CreateUserData {
  name: string;
  email: string;
  password: string;
  role?: string;
}

interface UpdateUserData {
  name?: string;
  email?: string;
  role?: string;
}

interface UserQuery {
  page: number;
  limit: number;
  search?: string;
  role?: string;
}

interface PaginatedResult<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export class UserService extends BaseService {
  constructor(private userRepository: any, private passwordHasher: any) {
    super();
  }

  async createUser(userData: CreateUserData): Promise<User> {
    try {
      this.logInfo('Creating new user', { email: userData.email });

      // Check if user already exists
      const existingUser = await this.userRepository.findByEmail(userData.email);
      if (existingUser) {
        throw new ValidationError('User with this email already exists');
      }

      // Hash password
      const hashedPassword = await this.passwordHasher.hash(userData.password);

      // Create user
      const user = await this.userRepository.create({
        ...userData,
        password: hashedPassword,
        role: userData.role || 'user'
      });

      this.emitEvent('user.created', { userId: user.id, email: user.email });

      this.logInfo('User created successfully', { userId: user.id });
      return user;

    } catch (error) {
      this.logError('Failed to create user', error);
      throw error;
    }
  }

  async getUserById(userId: string): Promise<User | null> {
    try {
      const user = await this.userRepository.findById(userId);

      if (!user) {
        return null;
      }

      // Remove sensitive data
      const { password, ...safeUser } = user;
      return safeUser;

    } catch (error) {
      this.logError('Failed to get user by ID', error);
      throw error;
    }
  }

  async getUsers(query: UserQuery): Promise<PaginatedResult<User>> {
    try {
      const result = await this.userRepository.findPaginated(query);

      // Remove sensitive data from all users
      const safeUsers = result.data.map(({ password, ...user }) => user);

      return {
        ...result,
        data: safeUsers
      };

    } catch (error) {
      this.logError('Failed to get users', error);
      throw error;
    }
  }

  async updateUser(userId: string, updateData: UpdateUserData): Promise<User> {
    try {
      this.logInfo('Updating user', { userId, updates: Object.keys(updateData) });

      // Check if user exists
      const existingUser = await this.userRepository.findById(userId);
      if (!existingUser) {
        throw new NotFoundError('User');
      }

      // Check email uniqueness if email is being updated
      if (updateData.email && updateData.email !== existingUser.email) {
        const userWithEmail = await this.userRepository.findByEmail(updateData.email);
        if (userWithEmail) {
          throw new ValidationError('Email already in use');
        }
      }

      const updatedUser = await this.userRepository.update(userId, {
        ...updateData,
        updatedAt: new Date()
      });

      this.emitEvent('user.updated', { userId, changes: Object.keys(updateData) });

      this.logInfo('User updated successfully', { userId });
      return updatedUser;

    } catch (error) {
      this.logError('Failed to update user', error);
      throw error;
    }
  }

  async deleteUser(userId: string): Promise<void> {
    try {
      this.logInfo('Deleting user', { userId });

      // Check if user exists
      const existingUser = await this.userRepository.findById(userId);
      if (!existingUser) {
        throw new NotFoundError('User');
      }

      await this.userRepository.delete(userId);

      this.emitEvent('user.deleted', { userId, email: existingUser.email });

      this.logInfo('User deleted successfully', { userId });

    } catch (error) {
      this.logError('Failed to delete user', error);
      throw error;
    }
  }

  async authenticateUser(email: string, password: string): Promise<User | null> {
    try {
      const user = await this.userRepository.findByEmail(email);
      if (!user) {
        return null;
      }

      const isValidPassword = await this.passwordHasher.verify(password, user.password);
      if (!isValidPassword) {
        return null;
      }

      this.emitEvent('user.authenticated', { userId: user.id, email: user.email });

      // Return user without password
      const { password: _, ...safeUser } = user;
      return safeUser;

    } catch (error) {
      this.logError('Authentication failed', error);
      throw error;
    }
  }
}
```

## Repository Layer Patterns

### Base Repository

```typescript
import { BaseService } from './BaseService';

export abstract class BaseRepository<T extends { id: string }> extends BaseService {
  protected tableName: string;

  constructor(tableName: string) {
    super();
    this.tableName = tableName;
  }

  abstract create(data: Partial<T>): Promise<T>;
  abstract findById(id: string): Promise<T | null>;
  abstract findAll(): Promise<T[]>;
  abstract update(id: string, data: Partial<T>): Promise<T>;
  abstract delete(id: string): Promise<void>;

  async exists(id: string): Promise<boolean> {
    const entity = await this.findById(id);
    return entity !== null;
  }

  async count(): Promise<number> {
    const entities = await this.findAll();
    return entities.length;
  }
}
```

This comprehensive guide provides patterns for building robust, scalable Node.js APIs with proper error handling, middleware patterns, service layers, and repository abstractions.