# Work Item Start Workflow

This comprehensive workflow guides the complete process of starting work on work items (Issues, PBIs, and Tasks) across GitHub and Azure DevOps platforms. It combines preparation, planning, implementation setup, and development processes using the unified SDO tool.

## Overview

The Work Item Start workflow provides end-to-end guidance for beginning development work on any type of work item. **This workflow covers the complete start-to-implementation process** - from initial verification through development environment setup to active coding following established patterns.

**Key Principles:**
- **Unified Tooling**: Use SDO for all work item and repository operations
- **Proper Planning**: Verify requirements and dependencies before starting
- **Environment Setup**: Ensure development environment is properly configured
- **Quality Standards**: Follow established coding patterns and testing practices

## Prerequisites

### For All Work Items
- [ ] Work item exists and is assigned to you
- [ ] Acceptance criteria are clear and understood
- [ ] No blocking dependencies exist
- [ ] Required tools and environment are set up
- [ ] Repository access and permissions confirmed

### For Issues (GitHub)
- [ ] Issue is properly labeled and prioritized
- [ ] Related requirements are documented
- [ ] No duplicate issues exist
- [ ] Repository and branch access available

### For PBIs (Azure DevOps)
- [ ] PBI in "Committed" state with task breakdown
- [ ] All child Tasks created and properly linked
- [ ] Task breakdown follows ranked implementation order
- [ ] Sprint capacity allocated for PBI work
- [ ] Development team assigned and available

### For Tasks (Azure DevOps)
- [ ] Task work item created and assigned
- [ ] Parent PBI approved and in "Committed" state
- [ ] Task requirements clearly defined
- [ ] Acceptance criteria established

## Input Parameters

```
Work Item ID: [Issue/PBI/Task number, e.g., 123]
Work Item Type: [Issue/PBI/Task]
Platform: [GitHub/Azure DevOps]
Repository: [owner/repo for GitHub, org/project for Azure DevOps]
Branch Name: [feature branch name following convention]
```

## Complete Start Workflow

### Phase 1: Verification and Preparation

#### 1.1 Verify Work Item Details
```bash
# Check work item status and details
sdo workitem show --id [WORK_ITEM_ID]

# Verify work item state and assignment
# Ensure it's assigned to you and in correct state
```

#### 1.2 Check Repository Status
```bash
# Verify repository state
git status
git branch -a

# Ensure you're on main/master branch
git branch
```

#### 1.3 Validate Prerequisites
**For PBIs (Additional Validation):**
```bash
# Check PBI readiness
sdo workitem show --id [PBI_ID]

# Verify task breakdown exists
# Confirm all child tasks are linked
```

**For Tasks (Additional Validation):**
```bash
# Check parent PBI status
sdo workitem show --id [PARENT_PBI_ID]

# Verify task is properly linked
# Confirm acceptance criteria are defined
```

### Phase 2: Branch Creation and Setup

#### 2.1 Create Feature Branch
```bash
# Create appropriately named feature branch
git checkout -b [branch-name]

# Push to remote and set upstream
git push -u origin [branch-name]
```

**Branch Naming Conventions:**
- **Issues**: `issue-[number]-[description]` (e.g., `issue-123-networth-command`)
- **PBIs**: `pbi-[number]-[description]` (e.g., `pbi-456-reports-enhancement`)
- **Tasks**: `task-[number]-[description]` (e.g., `task-167-implement-cli-handler`)

#### 2.2 Update Work Item Status
```bash
# Mark work item as In Progress
sdo workitem update --id [WORK_ITEM_ID] --state "In Progress"
```

#### 2.3 Set Up Development Environment
```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Verify environment setup
python -c "import [package_name]; print('Environment ready')"
```

### Phase 3: Analysis and Planning

#### 3.1 Review Requirements
**For All Work Items:**
- Analyze acceptance criteria and requirements
- Identify integration points and dependencies
- Consider edge cases and error conditions
- Plan testing approach (TDD recommended)

**For PBIs (Additional):**
- [ ] Validate task breakdown and dependencies
- [ ] Review sprint capacity and timeline
- [ ] Coordinate with assigned team members
- [ ] Plan task execution order (Task 1, Task 2, etc.)

**For Tasks (Additional):**
- [ ] Review parent PBI context and goals
- [ ] Analyze task-specific requirements
- [ ] Identify required code changes
- [ ] Plan implementation approach

#### 3.2 Review Existing Codebase
```bash
# Explore codebase structure
find . -name "*.py" -path "*/[package]/*" | head -10

# Review established patterns
grep -r "class.*Client" [package]/
grep -r "def.*handle" [package]/cli.py
```

#### 3.3 Plan Implementation Approach
**Code Patterns to Follow:**
- CLI handlers: Reference `[package]/cli.py`
- API methods: Reference `[package]/client.py`
- Error handling: Use type hints, docstrings, proper exceptions
- Logging: Follow established logging patterns

### Phase 4: Development Environment Setup

#### 4.1 Code Quality Tools
```bash
# Set up pre-commit hooks and quality checks
make lint        # Run all quality checks
make format      # Format code with Black and isort

# Verify tools are working
python -m pytest --version
python -m black --version
```

#### 4.2 Testing Framework Setup
```bash
# Verify testing environment
python -m pytest tests/ --collect-only | head -10

# Check test coverage setup
python -m pytest --cov=[package] --cov-report=term-missing --collect-only | head -5
```

### Phase 5: Implementation Guidelines

#### 5.1 Development Standards
**Code Implementation:**
- Use type hints and comprehensive docstrings
- Follow established error handling patterns
- Implement proper logging throughout
- Write self-documenting code

**Testing Approach (TDD):**
```python
# Example test structure
import unittest
from unittest.mock import patch
from [package].client import [ClientClass]

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.client = [ClientClass]()

    def test_success_case(self):
        # Arrange
        expected_result = "expected"

        # Act
        result = self.client.new_method()

        # Assert
        self.assertEqual(result, expected_result)

    def test_error_case(self):
        # Test error conditions
        with self.assertRaises(ValueError):
            self.client.new_method(invalid_param="value")
```

#### 5.2 Progress Tracking
**Daily Development Updates:**
- Update work item status regularly
- Document progress and any blockers
- Communicate with stakeholders
- Ensure alignment with acceptance criteria

**For PBIs - Task Coordination:**
- Complete tasks in ranked order (Task 1, then Task 2, etc.)
- Ensure task dependencies are met before starting dependent tasks
- Perform integration testing at task boundaries
- Update PBI status as tasks complete

**For Tasks - Implementation Focus:**
- Maintain complete focus on one task
- Ensure code is review-ready throughout development
- Verify all acceptance criteria are met
- Update documentation and comments

### Phase 6: Quality Assurance Setup

#### 6.1 Unit Testing
```bash
# Run specific tests during development
python -m pytest tests/test_new_feature.py -v

# Run with coverage
python -m pytest --cov=[package] --cov-report=html tests/test_new_feature.py
```

#### 6.2 Integration Testing
```bash
# Test CLI integration
python -m [package].cli [new-command] --help
python -m [package].cli [new-command] [test-parameters]

# Test API integration
python -c "from [package].client import [ClientClass]; c = [ClientClass](); print('Integration test passed')"
```

#### 6.3 Code Quality Validation
```bash
# Run quality checks regularly
make lint
make format

# Check for security issues
# (Add security scanning commands as needed)
```

## Work Item Type Specific Guidance

### Issues (GitHub/Azure DevOps)
**Implementation Focus:**
- Single feature or bug fix implementation
- May span multiple files but focused scope
- Complete end-to-end functionality
- Comprehensive testing required

**Completion Criteria:**
- [ ] Feature implemented and working
- [ ] All acceptance criteria verified
- [ ] Unit and integration tests passing
- [ ] Documentation updated
- [ ] Code reviewed and approved

### PBIs (Azure DevOps) - Coordination Level
**Management Focus:**
- Coordinate multiple tasks to deliver complete feature
- Ensure task dependencies are properly managed
- Validate end-to-end integration across tasks
- Manage sprint capacity and team coordination

**Key Activities:**
- [ ] Validate task breakdown and sequencing
- [ ] Assign tasks to appropriate team members
- [ ] Monitor task progress and dependencies
- [ ] Coordinate integration testing
- [ ] Validate PBI-level acceptance criteria

**Success Metrics:**
- [ ] All child tasks completed successfully
- [ ] Tasks completed in optimal sequence
- [ ] Integration testing passes
- [ ] PBI acceptance criteria met
- [ ] Sprint goals achieved

### Tasks (Azure DevOps) - Implementation Level
**Development Focus:**
- Individual coding and testing work
- Follow established patterns and standards
- Complete one task before starting another
- Ensure code quality and test coverage

**Implementation Steps:**
- [ ] Analyze task requirements thoroughly
- [ ] Implement following established patterns
- [ ] Write comprehensive tests (TDD approach)
- [ ] Update documentation and comments
- [ ] Verify acceptance criteria met
- [ ] Code review ready

## Error Handling and Recovery

### Common Start Issues

**Work Item Access Issues:**
- Verify work item exists and you have access
- Check platform credentials (GitHub token, Azure DevOps PAT)
- Confirm work item is in correct state for starting work

**Branch Creation Issues:**
- Ensure unique branch name (check existing branches)
- Verify repository permissions for branch creation
- Check naming convention compliance

**Environment Setup Issues:**
- Verify all required tools are installed
- Check Python version compatibility
- Validate dependency installation

**PBI/Task Coordination Issues:**
- Confirm task breakdown is complete for PBIs
- Verify parent-child relationships are correct
- Check sprint capacity and team assignments

### Recovery Steps
- **Access Denied**: Request appropriate permissions from repository admin
- **Branch Conflicts**: Use unique identifiers or coordinate with team
- **Environment Failures**: Check system requirements and reinstall dependencies
- **Coordination Issues**: Review work item relationships and update as needed

## Success Metrics

### Process Quality
- [ ] Work item properly verified before starting
- [ ] Branch created following naming conventions
- [ ] Environment properly configured
- [ ] Development standards followed from start

### Development Readiness
- [ ] Requirements clearly understood
- [ ] Implementation approach planned
- [ ] Testing strategy established
- [ ] Code quality tools configured

### Progress Tracking
- [ ] Work item status updated appropriately
- [ ] Progress communicated regularly
- [ ] Blockers identified and resolved quickly
- [ ] Acceptance criteria tracked throughout

## Next Steps

After completing this start workflow:

1. **Active Development** - Begin implementation following established patterns
2. **Regular Testing** - Run tests frequently and maintain quality standards
3. **Progress Updates** - Keep work item status and stakeholders informed
4. **Code Review Preparation** - Ensure code is review-ready throughout development

## Related Workflows and Actions

- **Start Work Item Action**: `actions/start-workitem.md` (quick start guide)
- **Close Work Item Action**: `actions/close-workitem.md` (completion workflow)
- **Create PR Action**: `actions/create-pr.md` (PR preparation)
- **Code Review Workflow**: `workflows/code-review.md` (PR review process)
- **Testing Workflow**: `workflows/testing.md` (comprehensive testing)

This workflow ensures all work items start with proper preparation, planning, and setup, establishing a solid foundation for successful implementation and delivery.</content>
<parameter name="filePath">c:\source\.github\.github\prompts\workflows\workitem-start.md