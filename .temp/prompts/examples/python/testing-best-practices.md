# Python Testing Best Practices

This guide covers comprehensive testing strategies and best practices for Python applications, focusing on unit testing, integration testing, and test-driven development patterns.

## Testing Fundamentals

### Test Structure and Organization

```python
# tests/
# ├── __init__.py
# ├── conftest.py          # Shared fixtures and configuration
# ├── unit/               # Unit tests
# │   ├── test_models.py
# │   ├── test_services.py
# │   └── test_utils.py
# ├── integration/        # Integration tests
# │   ├── test_api.py
# │   └── test_database.py
# └── e2e/               # End-to-end tests
#     └── test_user_flow.py
```

### Basic Test File Structure

```python
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

# Test subject imports
from myapp.services.user_service import UserService
from myapp.models.user import User
from myapp.repositories.user_repository import UserRepository

class TestUserService:
    """Test cases for UserService class."""

    @pytest.fixture
    def user_repository_mock(self):
        """Mock user repository."""
        return Mock(spec=UserRepository)

    @pytest.fixture
    def user_service(self, user_repository_mock):
        """User service with mocked dependencies."""
        return UserService(user_repository_mock)

    def test_create_user_success(self, user_service, user_repository_mock):
        """Test successful user creation."""
        # Arrange
        user_data = {'name': 'John Doe', 'email': 'john@example.com'}
        expected_user = User(id=1, **user_data)

        user_repository_mock.create.return_value = expected_user

        # Act
        result = user_service.create_user(user_data)

        # Assert
        assert result.id == 1
        assert result.name == 'John Doe'
        assert result.email == 'john@example.com'
        user_repository_mock.create.assert_called_once_with(user_data)

    def test_create_user_validation_error(self, user_service, user_repository_mock):
        """Test user creation with invalid data."""
        # Arrange
        invalid_data = {'name': '', 'email': 'invalid-email'}

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(invalid_data)

        assert 'name' in str(exc_info.value)
        assert 'email' in str(exc_info.value)
        user_repository_mock.create.assert_not_called()
```

## Unit Testing Patterns

### Testing Classes with Dependencies

```python
class TestUserServiceWithDatabase:
    """Test UserService with actual database (for integration tests)."""

    @pytest.fixture
    def db_session(self):
        """Database session fixture."""
        # Setup test database
        session = create_test_session()
        yield session
        # Cleanup
        session.rollback()
        session.close()

    @pytest.fixture
    def user_repo(self, db_session):
        """User repository with test database."""
        return UserRepository(db_session)

    @pytest.fixture
    def user_service(self, user_repo):
        """User service with real repository."""
        return UserService(user_repo)

    def test_create_and_retrieve_user(self, user_service):
        """Test creating and retrieving a user."""
        # Arrange
        user_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'age': 30
        }

        # Act
        created_user = user_service.create_user(user_data)
        retrieved_user = user_service.get_user(created_user.id)

        # Assert
        assert retrieved_user.name == user_data['name']
        assert retrieved_user.email == user_data['email']
        assert retrieved_user.age == user_data['age']
```

### Testing Async Functions

```python
import pytest_asyncio
import asyncio
from unittest.mock import AsyncMock

class TestAsyncUserService:
    """Test async user service methods."""

    @pytest.fixture
    async def async_user_repo_mock(self):
        """Mock async user repository."""
        mock = AsyncMock()
        mock.create.return_value = User(id=1, name='Async User', email='async@example.com')
        return mock

    @pytest.fixture
    async def async_user_service(self, async_user_repo_mock):
        """Async user service with mocked dependencies."""
        return AsyncUserService(async_user_repo_mock)

    @pytest.mark.asyncio
    async def test_create_user_async(self, async_user_service, async_user_repo_mock):
        """Test async user creation."""
        # Arrange
        user_data = {'name': 'Async User', 'email': 'async@example.com'}

        # Act
        result = await async_user_service.create_user(user_data)

        # Assert
        assert result.id == 1
        assert result.name == 'Async User'
        async_user_repo_mock.create.assert_called_once_with(user_data)
```

### Testing Exceptions and Error Conditions

```python
class TestUserServiceErrorHandling:
    """Test error handling in UserService."""

    def test_create_user_repository_error(self, user_service, user_repository_mock):
        """Test handling repository errors during user creation."""
        # Arrange
        user_data = {'name': 'John Doe', 'email': 'john@example.com'}
        user_repository_mock.create.side_effect = DatabaseError("Connection failed")

        # Act & Assert
        with pytest.raises(ServiceError) as exc_info:
            user_service.create_user(user_data)

        assert "Failed to create user" in str(exc_info.value)
        assert exc_info.value.__cause__ is not None

    def test_get_user_not_found(self, user_service, user_repository_mock):
        """Test retrieving non-existent user."""
        # Arrange
        user_repository_mock.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundError) as exc_info:
            user_service.get_user(999)

        assert "User 999 not found" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_email", [
        "",
        "invalid-email",
        "user@",
        "@domain.com",
        "user@domain",
    ])
    def test_create_user_invalid_email(self, user_service, user_repository_mock, invalid_email):
        """Test user creation with various invalid email formats."""
        # Arrange
        user_data = {'name': 'John Doe', 'email': invalid_email}

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(user_data)

        assert "email" in str(exc_info.value).lower()
```

### Testing with Fixtures and Parametrization

```python
@pytest.fixture(scope="class")
def test_users():
    """Fixture providing test user data."""
    return [
        {'name': 'Alice', 'email': 'alice@example.com', 'role': 'admin'},
        {'name': 'Bob', 'email': 'bob@example.com', 'role': 'user'},
        {'name': 'Charlie', 'email': 'charlie@example.com', 'role': 'user'},
    ]

class TestUserBulkOperations:
    """Test bulk user operations."""

    @pytest.mark.parametrize("user_count", [1, 5, 10, 100])
    def test_bulk_create_users(self, user_service, user_repository_mock, user_count):
        """Test creating multiple users at once."""
        # Arrange
        users_data = [
            {'name': f'User {i}', 'email': f'user{i}@example.com'}
            for i in range(user_count)
        ]

        # Act
        results = user_service.bulk_create_users(users_data)

        # Assert
        assert len(results) == user_count
        assert all(user.id is not None for user in results)
        user_repository_mock.bulk_create.assert_called_once_with(users_data)

    def test_bulk_create_with_failures(self, user_service, user_repository_mock):
        """Test bulk creation where some users fail validation."""
        # Arrange
        users_data = [
            {'name': 'Valid User', 'email': 'valid@example.com'},
            {'name': '', 'email': 'invalid@example.com'},  # Invalid: empty name
            {'name': 'Another Valid', 'email': 'another@example.com'},
            {'name': 'Third Valid', 'email': 'invalid-email'},  # Invalid: bad email
        ]

        # Act
        results = user_service.bulk_create_users(users_data)

        # Assert
        assert len(results) == 4
        assert results[0].success is True  # Valid user
        assert results[1].success is False  # Invalid name
        assert results[1].error == "Name is required"
        assert results[2].success is True  # Valid user
        assert results[3].success is False  # Invalid email
        assert "email" in results[3].error.lower()
```

## Integration Testing Patterns

### Testing with Test Databases

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from myapp.database import Base, get_db_session

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def test_session(test_engine):
    """Create test database session."""
    SessionLocal = sessionmaker(bind=test_engine)
    session = SessionLocal()

    # Start transaction
    session.begin()

    try:
        yield session
    finally:
        # Rollback transaction to keep tests isolated
        session.rollback()
        session.close()

class TestUserIntegration:
    """Integration tests for user operations."""

    def test_full_user_lifecycle(self, test_session):
        """Test complete user lifecycle: create, read, update, delete."""
        # Arrange
        user_repo = UserRepository(test_session)
        user_service = UserService(user_repo)

        user_data = {
            'name': 'Integration Test User',
            'email': 'integration@example.com',
            'department': 'Engineering'
        }

        # Act: Create user
        created_user = user_service.create_user(user_data)

        # Assert: User was created
        assert created_user.id is not None
        assert created_user.name == user_data['name']

        # Act: Retrieve user
        retrieved_user = user_service.get_user(created_user.id)

        # Assert: User data matches
        assert retrieved_user.email == user_data['email']
        assert retrieved_user.department == user_data['department']

        # Act: Update user
        update_data = {'department': 'Product'}
        updated_user = user_service.update_user(created_user.id, update_data)

        # Assert: User was updated
        assert updated_user.department == 'Product'

        # Act: Delete user
        user_service.delete_user(created_user.id)

        # Assert: User was deleted
        with pytest.raises(NotFoundError):
            user_service.get_user(created_user.id)
```

### Testing API Endpoints

```python
import pytest
from fastapi.testclient import TestClient
from myapp.main import app
from myapp.database import get_db_session

@pytest.fixture
def client(test_session):
    """Test client with test database."""
    def override_get_db():
        return test_session

    app.dependency_overrides[get_db_session] = override_get_db
    return TestClient(app)

class TestUserAPI:
    """Test user API endpoints."""

    def test_create_user_api(self, client):
        """Test creating user via API."""
        user_data = {
            'name': 'API Test User',
            'email': 'api@example.com'
        }

        response = client.post('/users/', json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data['name'] == user_data['name']
        assert data['email'] == user_data['email']
        assert 'id' in data

    def test_get_user_api(self, client):
        """Test retrieving user via API."""
        # First create a user
        user_data = {'name': 'Get Test User', 'email': 'get@example.com'}
        create_response = client.post('/users/', json=user_data)
        user_id = create_response.json()['id']

        # Then retrieve it
        response = client.get(f'/users/{user_id}')

        assert response.status_code == 200
        data = response.json()
        assert data['id'] == user_id
        assert data['name'] == user_data['name']

    def test_get_nonexistent_user_api(self, client):
        """Test retrieving non-existent user via API."""
        response = client.get('/users/99999')

        assert response.status_code == 404
        data = response.json()
        assert 'error' in data
        assert 'not found' in data['error'].lower()

    def test_create_user_validation_error(self, client):
        """Test creating user with invalid data."""
        invalid_data = {
            'name': '',  # Empty name
            'email': 'invalid-email'  # Invalid email
        }

        response = client.post('/users/', json=invalid_data)

        assert response.status_code == 422
        data = response.json()
        assert 'detail' in data
        # Check for validation errors
        error_fields = [error['loc'][-1] for error in data['detail']]
        assert 'name' in error_fields
        assert 'email' in error_fields
```

## Mocking and Test Doubles

### Advanced Mocking Patterns

```python
from unittest.mock import Mock, MagicMock, call
import pytest

class TestComplexService:
    """Test service with complex dependencies."""

    @pytest.fixture
    def mock_cache(self):
        """Mock cache with advanced behavior."""
        cache = Mock()
        cache.get.return_value = None  # Cache miss by default
        cache.set.return_value = True
        return cache

    @pytest.fixture
    def mock_metrics(self):
        """Mock metrics collector."""
        metrics = Mock()
        return metrics

    @pytest.fixture
    def complex_service(self, mock_cache, mock_metrics):
        """Complex service with multiple dependencies."""
        return ComplexService(cache=mock_cache, metrics=mock_metrics)

    def test_cached_operation(self, complex_service, mock_cache, mock_metrics):
        """Test operation with caching behavior."""
        # Arrange
        user_id = 123
        expected_data = {'name': 'Cached User'}

        # First call - cache miss
        mock_cache.get.return_value = None
        # Simulate database call
        complex_service.db_get_user = Mock(return_value=expected_data)

        # Act
        result1 = complex_service.get_user_with_cache(user_id)

        # Assert first call
        assert result1 == expected_data
        mock_cache.get.assert_called_with(f'user:{user_id}')
        mock_cache.set.assert_called_with(f'user:{user_id}', expected_data, ttl=300)
        mock_metrics.increment.assert_called_with('cache_miss')

        # Reset mocks
        mock_cache.reset_mock()
        mock_metrics.reset_mock()

        # Second call - cache hit
        mock_cache.get.return_value = expected_data

        # Act
        result2 = complex_service.get_user_with_cache(user_id)

        # Assert second call
        assert result2 == expected_data
        mock_cache.get.assert_called_with(f'user:{user_id}')
        mock_cache.set.assert_not_called()  # Should not set cache on hit
        mock_metrics.increment.assert_called_with('cache_hit')
        complex_service.db_get_user.assert_called_once()  # Only called once

    def test_error_handling_with_metrics(self, complex_service, mock_cache, mock_metrics):
        """Test error handling with metrics collection."""
        # Arrange
        mock_cache.get.side_effect = Exception("Cache connection failed")

        # Act & Assert
        with pytest.raises(ServiceError) as exc_info:
            complex_service.get_user_with_cache(123)

        assert "Cache connection failed" in str(exc_info.value)
        mock_metrics.increment.assert_called_with('cache_error')
```

### Mock Side Effects and Callbacks

```python
def test_async_operation_with_side_effects(self, async_service):
    """Test async operation with complex side effects."""
    # Arrange
    call_count = 0

    def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ConnectionError("Temporary failure")
        return {"data": "success"}

    async_service.external_api_call = Mock(side_effect=side_effect)

    # Act
    result = await async_service.resilient_operation()

    # Assert
    assert result == {"data": "success"}
    assert call_count == 2  # First call failed, second succeeded
    assert async_service.external_api_call.call_count == 2
```

## Test Organization and Best Practices

### Test Configuration (conftest.py)

```python
# conftest.py
import pytest
from myapp.database import create_engine, Base
from myapp.config import TestConfig

@pytest.fixture(scope="session")
def test_engine():
    """Test database engine."""
    engine = create_engine(TestConfig.DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def test_session(test_engine):
    """Test database session with transaction rollback."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="session")
def test_client(test_engine):
    """Test client for API testing."""
    from myapp.main import app
    from myapp.database import get_db_session

    def override_get_db():
        return test_session(test_engine)

    app.dependency_overrides[get_db_session] = override_get_db
    return TestClient(app)

# Custom markers
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
```

### Running Tests with Coverage

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=myapp --cov-report=html

# Run specific test categories
pytest -m "unit"                    # Only unit tests
pytest -m "integration"             # Only integration tests
pytest -m "not slow"                # Skip slow tests

# Run tests in parallel
pytest -n auto

# Run with detailed output
pytest -v --tb=short
```

### Test Quality Metrics

```python
# .coveragerc
[run]
source = myapp
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

[html]
directory = htmlcov
```

## Performance Testing

### Load Testing with pytest

```python
import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class TestPerformance:
    """Performance tests for critical operations."""

    @pytest.mark.slow
    def test_bulk_operation_performance(self, user_service, benchmark):
        """Test performance of bulk user creation."""
        user_data = [
            {'name': f'User {i}', 'email': f'user{i}@example.com'}
            for i in range(100)
        ]

        # Benchmark the operation
        result = benchmark(user_service.bulk_create_users, user_data)

        assert len(result) == 100
        assert benchmark.stats.stats.mean < 5.0  # Should complete in under 5 seconds

    @pytest.mark.slow
    @pytest.mark.parametrize("concurrent_users", [10, 50, 100])
    def test_concurrent_access(self, user_service, concurrent_users):
        """Test concurrent user access."""
        def create_user(i):
            return user_service.create_user({
                'name': f'Concurrent User {i}',
                'email': f'concurrent{i}@example.com'
            })

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(create_user, i) for i in range(concurrent_users)]
            results = [future.result() for future in as_completed(futures)]

        end_time = time.time()

        assert len(results) == concurrent_users
        assert all(user.id is not None for user in results)
        # Should complete within reasonable time
        assert (end_time - start_time) < 30
```

## Continuous Integration

### GitHub Actions Test Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests with coverage
      run: |
        pytest --cov=myapp --cov-report=xml --cov-fail-under=80

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

This comprehensive testing guide provides patterns and best practices for building robust, maintainable test suites in Python applications.