# React Component Patterns

This guide covers comprehensive patterns for building robust React components, focusing on modern React patterns, TypeScript integration, and best practices for maintainable component architecture.

## Component Architecture Patterns

### Base Component with TypeScript

```tsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

// Types
interface User {
  id: number;
  name: string;
  email: string;
  avatar?: string;
  role: 'admin' | 'user' | 'moderator';
}

interface UserProfileProps {
  userId: number;
  onUpdate?: (user: User) => void;
  onError?: (error: Error) => void;
  className?: string;
}

interface UserProfileState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

// Custom hooks
const useUserProfile = (userId: number) => {
  const [state, setState] = useState<UserProfileState>({
    user: null,
    loading: true,
    error: null
  });

  const fetchUser = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));

      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch user: ${response.status}`);
      }

      const user: User = await response.json();
      setState({ user, loading: false, error: null });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setState({ user: null, loading: false, error: errorMessage });
    }
  }, [userId]);

  const updateUser = useCallback(async (updates: Partial<User>) => {
    if (!state.user) return;

    try {
      const response = await fetch(`/api/users/${userId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      });

      if (!response.ok) {
        throw new Error(`Failed to update user: ${response.status}`);
      }

      const updatedUser: User = await response.json();
      setState(prev => ({ ...prev, user: updatedUser }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Update failed';
      setState(prev => ({ ...prev, error: errorMessage }));
    }
  }, [userId, state.user]);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return {
    ...state,
    refetch: fetchUser,
    updateUser
  };
};

// Error boundary component
const UserProfileErrorFallback: React.FC<{ error: Error; resetError: () => void }> = ({
  error,
  resetError
}) => (
  <div className="error-boundary" role="alert">
    <h3>Something went wrong loading the user profile</h3>
    <p>{error.message}</p>
    <button onClick={resetError}>Try again</button>
  </div>
);

// Main component
const UserProfile: React.FC<UserProfileProps> = ({
  userId,
  onUpdate,
  onError,
  className = ''
}) => {
  const { user, loading, error, refetch, updateUser } = useUserProfile(userId);

  // Notify parent of errors
  useEffect(() => {
    if (error && onError) {
      onError(new Error(error));
    }
  }, [error, onError]);

  // Notify parent of updates
  useEffect(() => {
    if (user && onUpdate) {
      onUpdate(user);
    }
  }, [user, onUpdate]);

  const handleUpdate = useCallback(async (updates: Partial<User>) => {
    await updateUser(updates);
  }, [updateUser]);

  if (loading) {
    return (
      <div className={`user-profile loading ${className}`}>
        <div className="skeleton-loader" aria-label="Loading user profile">
          <div className="skeleton-avatar"></div>
          <div className="skeleton-text"></div>
          <div className="skeleton-text short"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`user-profile error ${className}`}>
        <div className="error-message" role="alert">
          <p>Failed to load user profile: {error}</p>
          <button onClick={refetch} type="button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className={`user-profile not-found ${className}`}>
        <p>User not found</p>
      </div>
    );
  }

  return (
    <div className={`user-profile ${className}`}>
      <div className="user-header">
        <img
          src={user.avatar || '/default-avatar.png'}
          alt={`${user.name}'s avatar`}
          className="user-avatar"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = '/default-avatar.png';
          }}
        />
        <div className="user-info">
          <h2>{user.name}</h2>
          <p className="user-email">{user.email}</p>
          <span className={`user-role role-${user.role}`}>
            {user.role}
          </span>
        </div>
      </div>

      <div className="user-actions">
        <button
          onClick={() => handleUpdate({ name: `${user.name} (Updated)` })}
          type="button"
          disabled={loading}
        >
          Update Name
        </button>
      </div>
    </div>
  );
};

// Exported component with error boundary
export const UserProfileWithErrorBoundary: React.FC<UserProfileProps> = (props) => (
  <ErrorBoundary FallbackComponent={UserProfileErrorFallback}>
    <UserProfile {...props} />
  </ErrorBoundary>
);

export default UserProfile;
```

### Compound Component Pattern

```tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

// Types
interface TabContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

interface TabProps {
  id: string;
  children: ReactNode;
}

interface TabListProps {
  children: ReactNode;
}

interface TabPanelProps {
  tabId: string;
  children: ReactNode;
}

// Context
const TabContext = createContext<TabContextValue | null>(null);

const useTabContext = () => {
  const context = useContext(TabContext);
  if (!context) {
    throw new Error('Tab components must be used within a TabContainer');
  }
  return context;
};

// Main container component
interface TabContainerProps {
  defaultTab?: string;
  children: ReactNode;
  onTabChange?: (tabId: string) => void;
}

export const TabContainer: React.FC<TabContainerProps> = ({
  defaultTab = '',
  children,
  onTabChange
}) => {
  const [activeTab, setActiveTab] = useState(defaultTab);

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    onTabChange?.(tabId);
  };

  const contextValue: TabContextValue = {
    activeTab,
    setActiveTab: handleTabChange
  };

  return (
    <TabContext.Provider value={contextValue}>
      <div className="tab-container">
        {children}
      </div>
    </TabContext.Provider>
  );
};

// Tab component
export const Tab: React.FC<TabProps> = ({ id, children }) => {
  const { activeTab, setActiveTab } = useTabContext();
  const isActive = activeTab === id;

  return (
    <button
      className={`tab ${isActive ? 'active' : ''}`}
      onClick={() => setActiveTab(id)}
      aria-selected={isActive}
      role="tab"
    >
      {children}
    </button>
  );
};

// TabList component
export const TabList: React.FC<TabListProps> = ({ children }) => (
  <div className="tab-list" role="tablist">
    {children}
  </div>
);

// TabPanel component
export const TabPanel: React.FC<TabPanelProps> = ({ tabId, children }) => {
  const { activeTab } = useTabContext();
  const isActive = activeTab === tabId;

  return (
    <div
      className={`tab-panel ${isActive ? 'active' : ''}`}
      role="tabpanel"
      aria-labelledby={`tab-${tabId}`}
      hidden={!isActive}
    >
      {isActive && children}
    </div>
  );
};

// Usage example
const UserDashboard: React.FC = () => (
  <TabContainer defaultTab="profile" onTabChange={(tab) => console.log('Switched to:', tab)}>
    <TabList>
      <Tab id="profile">Profile</Tab>
      <Tab id="settings">Settings</Tab>
      <Tab id="activity">Activity</Tab>
    </TabList>

    <TabPanel tabId="profile">
      <UserProfile userId={123} />
    </TabPanel>

    <TabPanel tabId="settings">
      <UserSettings />
    </TabPanel>

    <TabPanel tabId="activity">
      <UserActivity />
    </TabPanel>
  </TabContainer>
);
```

### Render Props Pattern

```tsx
import React, { ReactNode, ComponentType } from 'react';

// Types
interface DataState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

interface DataProviderProps<T> {
  endpoint: string;
  children: (state: DataState<T> & { refetch: () => void }) => ReactNode;
  fallback?: ComponentType<{ refetch: () => void }>;
}

// Generic data provider
function DataProvider<T = any>({
  endpoint,
  children,
  fallback: Fallback
}: DataProviderProps<T>) {
  const [state, setState] = useState<DataState<T>>({
    data: null,
    loading: true,
    error: null
  });

  const fetchData = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));

      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: T = await response.json();
      setState({ data, loading: false, error: null });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setState({ data: null, loading: false, error: errorMessage });
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Show fallback if provided and there's an error
  if (state.error && Fallback) {
    return <Fallback refetch={fetchData} />;
  }

  return <>{children({ ...state, refetch: fetchData })}</>;
}

// Specialized providers
export const UserProvider: React.FC<{
  userId: number;
  children: (state: DataState<User> & { refetch: () => void }) => ReactNode;
}> = ({ userId, children }) => (
  <DataProvider<User> endpoint={`/api/users/${userId}`}>
    {children}
  </DataProvider>
);

export const PostsProvider: React.FC<{
  userId?: number;
  children: (state: DataState<Post[]> & { refetch: () => void }) => ReactNode;
}> = ({ userId, children }) => {
  const endpoint = userId ? `/api/users/${userId}/posts` : '/api/posts';
  return (
    <DataProvider<Post[]> endpoint={endpoint}>
      {children}
    </DataProvider>
  );
};

// Usage
const UserProfileWithPosts: React.FC<{ userId: number }> = ({ userId }) => (
  <UserProvider userId={userId}>
    {({ data: user, loading: userLoading, error: userError, refetch: refetchUser }) => (
      <div className="user-profile-with-posts">
        {userLoading && <div>Loading user...</div>}
        {userError && <div>Error: {userError}</div>}
        {user && (
          <>
            <h1>{user.name}</h1>
            <PostsProvider userId={userId}>
              {({ data: posts, loading: postsLoading, error: postsError, refetch: refetchPosts }) => (
                <>
                  {postsLoading && <div>Loading posts...</div>}
                  {postsError && <div>Error loading posts: {postsError}</div>}
                  {posts && (
                    <div className="posts">
                      <h2>Posts by {user.name}</h2>
                      {posts.map(post => (
                        <article key={post.id}>
                          <h3>{post.title}</h3>
                          <p>{post.content}</p>
                        </article>
                      ))}
                    </div>
                  )}
                </>
              )}
            </PostsProvider>
          </>
        )}
      </div>
    )}
  </UserProvider>
);
```

## Performance Optimization Patterns

### Memoization and Optimization

```tsx
import React, { memo, useMemo, useCallback } from 'react';

// Expensive calculation hook
const useExpensiveCalculation = (baseValue: number, multiplier: number) => {
  return useMemo(() => {
    console.log('Performing expensive calculation...');
    // Simulate expensive operation
    let result = baseValue;
    for (let i = 0; i < 1000000; i++) {
      result += Math.sin(i) * multiplier;
    }
    return result;
  }, [baseValue, multiplier]); // Only recalculate when these change
};

// Memoized component
interface ExpensiveComponentProps {
  value: number;
  multiplier: number;
  onChange: (value: number) => void;
}

const ExpensiveComponent = memo<ExpensiveComponentProps>(({
  value,
  multiplier,
  onChange
}) => {
  const result = useExpensiveCalculation(value, multiplier);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(Number(e.target.value));
  }, [onChange]);

  return (
    <div>
      <input
        type="number"
        value={value}
        onChange={handleChange}
        aria-label="Value input"
      />
      <p>Result: {result.toFixed(2)}</p>
    </div>
  );
});

ExpensiveComponent.displayName = 'ExpensiveComponent';

// Optimized list component
interface Item {
  id: number;
  name: string;
  value: number;
}

interface ItemListProps {
  items: Item[];
  selectedId?: number;
  onItemSelect: (item: Item) => void;
  renderItem?: (item: Item) => ReactNode;
}

const ItemList = memo<ItemListProps>(({
  items,
  selectedId,
  onItemSelect,
  renderItem
}) => {
  const defaultRenderItem = useCallback((item: Item) => (
    <div key={item.id} className="item">
      {item.name}: {item.value}
    </div>
  ), []);

  const renderFunction = renderItem || defaultRenderItem;

  const handleItemClick = useCallback((item: Item) => {
    onItemSelect(item);
  }, [onItemSelect]);

  return (
    <ul className="item-list">
      {items.map(item => (
        <li
          key={item.id}
          className={selectedId === item.id ? 'selected' : ''}
          onClick={() => handleItemClick(item)}
        >
          {renderFunction(item)}
        </li>
      ))}
    </ul>
  );
});

ItemList.displayName = 'ItemList';
```

### Code Splitting and Lazy Loading

```tsx
import React, { Suspense, lazy, ComponentType } from 'react';

// Lazy load components
const LazyUserProfile = lazy(() => import('./UserProfile'));
const LazyUserSettings = lazy(() => import('./UserSettings'));
const LazyUserActivity = lazy(() => import('./UserActivity'));

// Loading component
const LoadingSpinner: React.FC = () => (
  <div className="loading-spinner" aria-label="Loading">
    <div className="spinner"></div>
    <p>Loading...</p>
  </div>
);

// Error boundary for lazy components
const LazyErrorBoundary: React.FC<{ children: ReactNode }> = ({ children }) => (
  <ErrorBoundary
    FallbackComponent={({ error, resetErrorBoundary }) => (
      <div className="lazy-error">
        <h3>Failed to load component</h3>
        <p>{error.message}</p>
        <button onClick={resetErrorBoundary}>Try again</button>
      </div>
    )}
  >
    {children}
  </ErrorBoundary>
);

// Lazy wrapper component
interface LazyWrapperProps {
  component: ComponentType<any>;
  fallback?: ReactNode;
  [key: string]: any;
}

const LazyWrapper: React.FC<LazyWrapperProps> = ({
  component: Component,
  fallback = <LoadingSpinner />,
  ...props
}) => (
  <Suspense fallback={fallback}>
    <Component {...props} />
  </Suspense>
);

// Usage in routing
const AppRoutes: React.FC = () => (
  <Router>
    <Switch>
      <Route path="/profile/:userId">
        <LazyErrorBoundary>
          <LazyWrapper
            component={LazyUserProfile}
            userId={useParams().userId}
          />
        </LazyErrorBoundary>
      </Route>

      <Route path="/settings">
        <LazyErrorBoundary>
          <LazyWrapper component={LazyUserSettings} />
        </LazyErrorBoundary>
      </Route>

      <Route path="/activity">
        <LazyErrorBoundary>
          <LazyWrapper component={LazyUserActivity} />
        </LazyErrorBoundary>
      </Route>
    </Switch>
  </Router>
);
```

## Testing Patterns

### Component Testing with React Testing Library

```tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { jest } from '@jest/globals';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';

// Mock fetch
global.fetch = jest.fn();

const mockUser: User = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  role: 'user'
};

describe('UserProfile', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state initially', () => {
    (global.fetch as jest.Mock).mockImplementationOnce(() =>
      new Promise(() => {}) // Never resolves
    );

    render(<UserProfile userId={1} />);

    expect(screen.getByLabelText('Loading user profile')).toBeInTheDocument();
  });

  it('renders user data when fetch succeeds', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockUser)
    });

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('user')).toBeInTheDocument();
  });

  it('renders error state when fetch fails', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(
      new Error('Network error')
    );

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load user profile/)).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });

  it('calls onError callback when error occurs', async () => {
    const mockOnError = jest.fn();
    (global.fetch as jest.Mock).mockRejectedValueOnce(
      new Error('Network error')
    );

    render(<UserProfile userId={1} onError={mockOnError} />);

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith(
        expect.any(Error)
      );
    });
  });

  it('calls onUpdate callback when user data is loaded', async () => {
    const mockOnUpdate = jest.fn();
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockUser)
    });

    render(<UserProfile userId={1} onUpdate={mockOnUpdate} />);

    await waitFor(() => {
      expect(mockOnUpdate).toHaveBeenCalledWith(mockUser);
    });
  });

  it('handles update button click', async () => {
    const user = userEvent.setup();
    const updatedUser = { ...mockUser, name: 'John Doe (Updated)' };

    (global.fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockUser)
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(updatedUser)
      });

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    const updateButton = screen.getByRole('button', { name: /update name/i });
    await user.click(updateButton);

    await waitFor(() => {
      expect(screen.getByText('John Doe (Updated)')).toBeInTheDocument();
    });
  });
});
```

This comprehensive guide provides patterns for building robust, maintainable React components with proper TypeScript integration, error handling, performance optimization, and testing strategies.