# Create Work Item Document Action

You are tasked with creating a work item document (Issue, PBI, or Task) for the current repository changes.

## Overview

This action provides a unified guide for creating work item markdown documents across platforms (GitHub Issues, Azure DevOps PBIs/Tasks). The work item type and platform are determined by the document content and metadata. Once created, these markdown files can be submitted for processing via `sdo wi create`.

**Important:** All work item files should be created in the `.temp/` directory at the root of the repository where the work item will be created.

## Naming Convention for `sdo wi create`

Files must be named by work item type in `.temp/`:
- `.temp/issue.md` - GitHub Issue
- `.temp/task.md` - Azure DevOps Task
- `.temp/pbi.md` - Azure DevOps PBI
- `.temp/bug.md` - Azure DevOps Bug
- `.temp/epic.md` - Azure DevOps Epic

## Work Item Types

For complete formatting examples and standards, see the [templates](../templates/) directory:

- **GitHub Issues**: [issue-gh-example.md](../templates/issue-gh-example.md)
- **Azure DevOps PBIs**: [issue-azdo-pbi-example.md](../templates/issue-azdo-pbi-example.md)
- **Azure DevOps Tasks**: [issue-azdo-task-example.md](../templates/issue-azdo-task-example.md)
- **Azure DevOps Bugs**: [issue-azdo-bug-example.md](../templates/issue-azdo-bug-example.md)
- **Azure DevOps Epics**: [issue-azdo-epic-example.md](../templates/issue-azdo-epic-example.md)

All work item files should be created in the `.temp/` directory following the format shown in the corresponding template example.

## File Creation Workflow

### Step 1: Create the Markdown Document
Create the appropriate markdown file in the `.temp/` directory using the naming convention above, following the template example for your work item type:
- Refer to the corresponding example in [templates/](../templates/) for your specific work item type

### Step 2: Review and Prepare for Submission
- Ensure all required fields are populated correctly
- Verify the `## Target:` field matches your intended platform (github or azure)
- For Azure DevOps work items, confirm project-specific fields are accurate (Area, Iteration, etc.)
- Include sufficient context and acceptance criteria for team review

### Step 3: Submit for Processing
- Once the markdown file is created and reviewed, submit it via `sdo wi create`
- The target platform and work item type are determined by the filename and metadata fields in the document

