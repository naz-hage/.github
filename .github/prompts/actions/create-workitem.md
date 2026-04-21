# Create Work Item Document Action

You are tasked with creating a work item document (Issue, PBI, or Task) for the current repository changes.

## Overview

This action provides a unified guide for creating work item markdown documents across platforms (GitHub Issues, Azure DevOps PBIs/Tasks). The work item type and platform are determined by the document content and metadata. Once created, these markdown files can be submitted for processing via your team's work item management workflow.

**Important:** All work item files should be created in the `.temp/` directory at the root of the repository where the work item will be created.

**Prerequisites:** Replace `[REPO_NAME]` with your actual repository name (e.g., `my-repo`) throughout this guide.

## Work Item Types

### Issues (GitHub or Azure DevOps)
Used for bugs, features, or general tracking items.

**File Format:** Create `[REPO_NAME]/.temp/issue-message.md` with:
```markdown
# <Issue Title>

## Target: <github|azure>
## Repository: <owner/repo>
## Assignee:
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
## Assignee:
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

## File Creation Workflow

### Step 1: Create the Markdown Document
Create the appropriate markdown file in the `.temp/` directory:
- **For Issues**: Create `[REPO_NAME]/.temp/issue-message.md` following the Issue format above
- **For PBIs**: Create `[REPO_NAME]/.temp/pbi.md` following the PBI format above
- **For Tasks**: Create `[REPO_NAME]/.temp/task.md` following the Task format above

### Step 2: Review and Prepare for Submission
- Ensure all required fields are populated correctly
- Verify the `## Target:` field matches your intended platform (github or azure)
- For Azure DevOps work items, confirm project-specific fields (Area, Iteration, etc.) are accurate
- Include sufficient context and acceptance criteria for team review

### Step 3: Submit for Processing
- Once the markdown file is created and reviewed, submit it via your team's work item management workflow
- The target platform (GitHub or Azure) and work item type are determined by the `## Target:` and `## Work Item Type:` fields in the document

