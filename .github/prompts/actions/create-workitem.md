# Create Work Item Action

You are tasked with creating a work item (Issue, PBI, or Task) for the current repository changes using an automated workflow.

## Overview

This action provides a unified guide for creating work items across platforms (GitHub Issues, Azure DevOps PBIs/Tasks) using the SDO CLI tool. The work item type and platform are determined by the file content and metadata.

**Important:** All work item files should be created in the `.temp/` directory at the root of the repository where the work item will be created. All `sdo` commands must be run from the repository root directory.

**Prerequisites:** Replace `[REPO_NAME]` with your actual repository name (e.g., `my-repo`) throughout this guide.

## Work Item Types

### Issues (GitHub or Azure DevOps)
Used for bugs, features, or general tracking items.

**File Format:** Create `[REPO_NAME]/.temp/issue-message.md` with:
```markdown
# <Issue Title>

## Target: <github|azure>
## Repository: <owner/repo>
## Assignee: <username or leave blank>
## Labels: <comma-separated labels>

## Description

<Detailed description of the issue, problem, or feature request>

## Acceptance Criteria
- [ ] <Clear, testable requirement 1>
- [ ] <Clear, testable requirement 2>
- [ ] <Include UI, logic, error handling, and test coverage as needed>
```

**Guidelines:**
- Title: descriptive title
- Target: Specify 'github' or 'azure' platform
- Repository: Use 'owner/repo' format
- Labels: Use relevant labels like 'backlog', 'bug', 'enhancement'
- Description: Explain the problem or feature clearly and concisely
- Acceptance Criteria: List specific, testable requirements with checkboxes

### PBIs (Azure DevOps)
Used for high-level features, user stories, or epics representing business value.

**File Format:** Create `[REPO_NAME]/.temp/pbi.md` with:
```markdown
# PBI-XXX: [Descriptive Title]

## Target: azdo
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
## Iteration: [FROM project-config.yaml: azure_devops.default_iteration]
## Assignee: [Product Owner or value from project-config.yaml]
## Work Item Type: PBI

## Description
[Clear description of business need and expected outcome]

## Business Value
[Why this PBI matters - impact on users/business]

## Acceptance Criteria
- [ ] [Specific, testable requirement]
- [ ] [Cover functional, performance, usability]
- [ ] [Include error handling scenarios]

## Dependencies
- [ ] [External systems/APIs required]
- [ ] [Other PBIs that must complete first]

## Story Points: [Estimate]
```

**Note:** This is a temporary file. Azure DevOps is the source of truth after creation.

### Tasks (Azure DevOps)
Used for specific, implementable work units that break down PBIs.

**File Format:** Create `[REPO_NAME]/.temp/task.md` with:
```markdown
# Task-XXX: [Descriptive Title]

**Parent PBI:** #[PBI_ID] - [PBI Title]

## Target: azdo
## Project: Proto
## Area: Proto\Warriors
## Iteration: Proto\Sprint [XX]
## Parent ID: [PBI_ID]
## Assignee: [Team Member]
## Labels: task
## Work Item Type: Task

## Description
[What needs to be implemented and why]

## Implementation Details
[Technical approach and design decisions]

## Acceptance Criteria
- [ ] [Specific completion condition]
- [ ] [Include code, tests, documentation]

## Dependencies
- [ ] [Prerequisites from other tasks/systems]

## Testing Requirements
- [ ] [Unit/integration tests required]

## Definition of Done
- [ ] Code follows project standards
- [ ] Tests pass with adequate coverage
- [ ] Code reviewed and approved
- [ ] Documentation updated

## Effort Estimate: [X hours/days]
```

**Note:** This is a temporary file. Azure DevOps is the source of truth after creation.

## Command
Use the `sdo` tool to create the work item. **Important:** Run these commands from the root directory of the repository where the work item will be created.
```powershell
sdo workitem create --file-path ./.temp/<filename>.md
```

**Note:** The target platform (GitHub or Azure) and work item type are determined by the `## Target:` and `## Work Item Type:` fields in the file.

## Examples

### Bug Report Issue
```powershell
# Create issue message file ([REPO_NAME]/.temp/issue-message.md)
# Content follows the Issue format above

# Create issue and get issue number (run from repository root)
sdo workitem create --file-path ./.temp/issue-message.md
# Output: ✓ Issue created successfully - URL: https://github.com/owner/repo/issues/123
```

### Feature Request Issue
```powershell
# Create issue message file ([REPO_NAME]/.temp/issue-message.md)
# Content follows the Issue format above

# Create issue (run from repository root)
sdo workitem create --file-path ./.temp/issue-message.md
# Output: ✓ Issue created successfully - URL: https://github.com/owner/repo/issues/456
```

### PBI Creation
```powershell
# Create PBI file ([REPO_NAME]/.temp/pbi.md)
# Content follows the PBI format above

# Create PBI (run from repository root)
sdo workitem create --file-path ./.temp/pbi.md
# Output: ✓ PBI created successfully - URL: https://dev.azure.com/org/project/_workitems/edit/789
```

### Task Creation
```powershell
# Create task file ([REPO_NAME]/.temp/task.md)
# Content follows the Task format above

# Create task (run from repository root)
sdo workitem create --file-path ./.temp/task.md
# Output: ✓ Task created successfully - URL: https://dev.azure.com/org/project/_workitems/edit/101
```

## Post-Creation Workflow
After creation, follow platform-specific workflows:
- **Issues**: Create a branch using the issue number (e.g., `git checkout -b issue/123-fix-validation`)
- **PBIs/Tasks**: Update in Azure DevOps for refinement and assignment

## Error Handling

### Common Issues:
1. **SDO command fails**: Verify sdo is installed and configured
2. **Authentication issues**: Check Azure DevOps/GitHub credentials
3. **File format issues**: Ensure the file follows the specified format for the work item type

### Recovery Steps:
- If SDO fails: Verify tool installation and permissions
- If authentication fails: Reconfigure credentials
- If creation fails: Check file format and content

## Notes
- Work items require appropriate metadata for proper linking and tracking
- Always include enough context for team members to understand the item
- Follow repository's work item tracking conventions
- Check for existing items to avoid duplicates