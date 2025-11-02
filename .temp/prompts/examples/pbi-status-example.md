# PBI Status Checker - Implementation Example

This demonstrates how to use the generic PBI status checker prompt with specific parameters for any development project.

## Example Usage

### Input Parameters
```
Repository: [PROJECT_ROOT]
Current Branch: [CURRENT_BRANCH]
PBI File: [PBI_FILE_PATH]
```

### Execution Steps

1. **Parse PBI File**: Extract acceptance criteria from the markdown
2. **Check File Existence**: Verify all mentioned files exist in the repository
3. **Validate Content**: Check if files contain expected configurations
4. **Update Status**: Mark items as completed [x] or pending [ ]
5. **Generate Report**: Show what's done vs what's remaining

### File Patterns to Check
Based on generic PBI example:
- `src/main/[LANGUAGE]/core/[FEATURE].py` - Core business logic implementation
- `src/main/[LANGUAGE]/[FEATURE]/service.py` - Service layer implementation
- `src/test/[LANGUAGE]/[FEATURE]Test.py` - Unit test implementations
- `docs/api/[FEATURE]-api.md` - API documentation
- `config/[FEATURE]-config.yaml` - Configuration files

### Status Report Output
```markdown
# PBI-123 Status Report
✅ Completed: 5/10 items
🔄 Pending: 5/10 items

## Next Steps
1. Implement core business logic in service classes
2. Add comprehensive unit and integration tests
3. Create API documentation and examples
4. Update configuration templates
5. Create pull request for code review
```

## Multi-Language Examples

### Python Project
```markdown
# PBI-456 Status Report
✅ Completed: 4/8 items
🔄 Pending: 4/8 items

## Completed Items
- [x] Implement user authentication service in `src/auth/service.py`
- [x] Add database models in `src/models/user.py`
- [x] Create unit tests in `tests/test_auth.py`
- [x] Update API documentation in `docs/auth-api.md`

## Pending Items
- [ ] Add integration tests for authentication flow
- [ ] Implement password reset functionality
- [ ] Add rate limiting middleware
- [ ] Create deployment configuration
```

### JavaScript/TypeScript Project
```markdown
# PBI-789 Status Report
✅ Completed: 6/9 items
🔄 Pending: 3/9 items

## Completed Items
- [x] Implement React component in `src/components/UserProfile.tsx`
- [x] Add API service in `src/services/userService.ts`
- [x] Create unit tests in `src/components/__tests__/UserProfile.test.tsx`
- [x] Update TypeScript interfaces in `src/types/user.ts`
- [x] Add Storybook stories in `src/components/UserProfile.stories.tsx`
- [x] Update component documentation in `docs/components.md`

## Pending Items
- [ ] Add end-to-end tests with Cypress
- [ ] Implement error boundary component
- [ ] Add accessibility testing
```

### Java Project
```markdown
# PBI-101 Status Report
✅ Completed: 5/7 items
🔄 Pending: 2/7 items

## Completed Items
- [x] Implement service class in `src/main/java/com/example/UserService.java`
- [x] Add repository interface in `src/main/java/com/example/UserRepository.java`
- [x] Create entity class in `src/main/java/com/example/User.java`
- [x] Add unit tests in `src/test/java/com/example/UserServiceTest.java`
- [x] Update REST controller in `src/main/java/com/example/UserController.java`

## Pending Items
- [ ] Add integration tests with TestContainers
- [ ] Implement caching layer
```

### C# Project
```markdown
# PBI-202 Status Report
✅ Completed: 4/6 items
🔄 Pending: 2/6 items

## Completed Items
- [x] Implement service class in `src/Services/UserService.cs`
- [x] Add data model in `src/Models/User.cs`
- [x] Create unit tests in `tests/UserServiceTests.cs`
- [x] Update API controller in `src/Controllers/UserController.cs`

## Pending Items
- [ ] Add integration tests with xUnit
- [ ] Implement logging and monitoring
```

## Automation Potential

This pattern can be extended to:
- **GitHub Actions**: Run as workflow on pull request creation
- **Azure DevOps Pipelines**: Integrate with build and release pipelines
- **GitLab CI/CD**: Use as part of merge request pipelines
- **Jenkins**: Execute as post-build step
- **Slack/Teams Integration**: Send notifications on status changes
- **Jira/Azure DevOps**: Auto-update work item status
- **Documentation Sites**: Generate living documentation from PBI status

## Configuration Templates

### GitHub Actions Workflow
```yaml
name: PBI Status Check
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  pbi-status-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check PBI Status
        run: |
          # Run PBI status checker script
          python scripts/check_pbi_status.py ${{ github.event.pull_request.body }}
```

### Azure DevOps Pipeline
```yaml
trigger:
  - main
  - develop

jobs:
- job: PBICheck
  displayName: 'PBI Status Validation'
  steps:
  - script: |
      # Run PBI validation script
      python tools/pbi_checker.py $(System.PullRequest.PullRequestId)
    displayName: 'Validate PBI Completion'
```

## Best Practices

### Status Update Guidelines
- **Mark as Complete**: Only when all acceptance criteria are met and tested
- **Partial Completion**: Use progress indicators for multi-step items
- **Dependencies**: Note any blocking issues or external dependencies
- **Testing**: Include test coverage metrics in status updates
- **Documentation**: Update API docs and README files as features are completed

### Integration Patterns
- **Pull Request Templates**: Include PBI status section in PR descriptions
- **Branch Naming**: Use PBI IDs in branch names for traceability
- **Commit Messages**: Reference PBI IDs in commit messages
- **Code Reviews**: Use PBI checklists during review process

### Reporting and Analytics
- **Progress Tracking**: Generate burndown charts from PBI status
- **Team Metrics**: Track completion rates and cycle times
- **Quality Metrics**: Monitor test coverage and bug rates
- **Process Improvement**: Identify bottlenecks and improvement opportunities