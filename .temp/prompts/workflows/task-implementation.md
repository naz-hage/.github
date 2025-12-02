# Task Implementation Workflow

This workflow guides the implementation phase of an individual Azure DevOps Task from planning to completion. It covers the coding, testing, and validation phases of development work for a single, implementable unit of work.

## Overview

The Task implementation workflow transforms individual task requirements into working code following the SDO project's standards and practices. **This workflow focuses on implementing one Task at a time** - each Task represents a specific, implementable unit that can be completed independently and contributes to meeting the parent PBI's acceptance criteria.

**Key Principle**: One task, one focus. Complete each task fully (coded, tested, documented) before moving to the next task in the PBI breakdown.

**Note**: This workflow is for individual Task implementation. For PBI-level coordination across multiple tasks, see `workflows/pbi-implementation.md`.

## Prerequisites

- Task work item created and assigned in Azure DevOps
- Development environment configured (see Copilot instructions)
- Parent PBI approved and in "Committed" state

**Note:** Task details are retrieved from Azure DevOps (source of truth), not local files.

## Implementation Workflow

### Phase 1: Preparation

#### 1.1 Read Task Requirements
```bash
# View task details in Azure DevOps (source of truth)
az boards work-item show --id [TASK_ID]

# Or open in browser
# https://dev.azure.com/[AZURE_DEVOPS_ORG]/[AZURE_DEVOPS_PROJECT]/_workitems/edit/[TASK_ID]
```

#### 1.2 Update Task Status
```bash
az boards work-item update --id [TASK_ID] --fields "System.State=In Progress"
```

#### 1.3 Create Feature Branch
```bash
git checkout -b azdo-[TASK_ID]
```

#### 1.4 Set Up Environment
```bash
pip install -r requirements.txt
pip install -e .
python -c "import sdo_package; print('Package ready')"
```

### Phase 2: Analysis and Design

#### 2.1 Review Requirements
Analyze task requirements, identify integration points, and consider edge cases.

#### 2.2 Review Existing Code
```bash
find . -name "*.py" -path "*/sdo_package/*"
grep -r "class.*Client" sdo_package/
```

#### 2.3 Plan Implementation
Design the approach following established patterns in `sdo_package/`.

### Phase 3: Implementation

#### 3.1 Follow Code Patterns
Reference established patterns:
- CLI handlers: `sdo_package/cli.py`
- API methods: `sdo_package/client.py`
- Error handling: Use type hints, docstrings, proper exceptions

#### 3.2 Implement Core Functionality
Develop features with type hints, docstrings, error handling, and logging.

#### 3.3 Add Tests
```python
import unittest
from unittest.mock import patch
from sdo_package.client import AzureDevOpsClient

class TestNewFeature(unittest.TestCase):
    def test_success_case(self):
        # Test implementation
        pass
```

#### 3.4 Update Documentation
Update docstrings, README, and architecture docs as needed.

### Phase 4: Testing and Validation

#### 4.1 Unit Testing
```bash
python -m pytest                                    # Run all tests
python -m pytest tests/test_new_feature.py -v      # Specific test
python -m pytest --cov=sdo_package --cov-report=html  # With coverage
```

#### 4.2 Integration Testing
```bash
python -m sdo_package.cli [new-command] --help
python -m sdo_package.cli [new-command] [test-parameters]
```

#### 4.3 Code Quality
```bash
make lint        # Run all quality checks
make format      # Format code with Black and isort
```

### Phase 5: Completion

#### 5.1 Verify Acceptance Criteria
Ensure all task acceptance criteria are met.

#### 5.2 Document Task Notes (Optional)
If you need to add comments to the task (e.g., documenting anti-patterns, decisions, or additional work):

```bash
# Create notes file for review and formatting
$taskId = 167  # Your task ID
$notesFile = ".temp/task-notes-$taskId.md"

# Create the notes file with proper markdown formatting
@"
## Task $taskId Implementation Notes

### Summary
[Brief summary of what was completed]

### Additional Work
- [Any work beyond task scope]
- [Rationale for additional changes]

### Decisions Made
- [Important technical decisions]
- [Trade-offs considered]

### Anti-Patterns Documented
- [Any deviations from standard workflow]
- [Justification for the deviation]
"@ | Out-File -FilePath $notesFile -Encoding UTF8

# Edit the notes file to add your content
code $notesFile

# After reviewing and formatting, post the comment to Azure DevOps
$notes = Get-Content -Path $notesFile -Raw
az boards work-item update --id $taskId --discussion $notes

# Optional: Keep the notes file for reference or delete it
# Remove-Item $notesFile
```

**Benefits:**
- Review and format notes before posting
- Ensure proper markdown formatting
- Avoid unformatted text walls in Azure DevOps
- Keep local copy for reference

#### 5.3 Commit Changes

**Create commit message file for review:**
```bash
# Create commit message file
$taskId = 167  # Your task ID
$commitFile = ".temp/commit-message-$taskId.txt"

# Create the commit message with conventional commit format
@"
feat: implement [feature description]

- Add [functionality details]
- Update [components modified]
- Add tests
- Update docs

Closes #$taskId
"@ | Out-File -FilePath $commitFile -Encoding UTF8

# Review and edit the commit message
code $commitFile

# After review, use it for the commit
git add .
git commit -F $commitFile
git push azure feature/task-$taskId-description
```

**Commit Message Guidelines:**
- Use conventional commit format: `feat:`, `fix:`, `docs:`, `test:`, etc.
- First line: Brief summary (50 chars or less)
- Blank line, then bullet points for details
- Reference task with `Closes #[TASK_ID]`


#### 5.4 Create Pull Request

**Reference:** `actions/create-pr.md`

Follow the PR creation workflow in `actions/create-pr.md` to prepare and submit your changes for review. Use the task ID for linking the PR to the work item.

## Next Steps

After completing this workflow:

1. **Code Review** - Follow `workflows/code-review.md` to get PR reviewed and merged
2. **Task Closure** - Follow `workflows/task-closure.md` after PR merge to close task and update parent PBI

**Important:** Complete the current task's review/merge before starting new tasks.

## Related Workflows

- [PBI Implementation](pbi-implementation.md) - Coordinating multiple tasks
- [Code Review](code-review.md) - PR review process
- [Testing](testing.md) - Quality assurance
- [Task Closure](task-closure.md) - Final task completion