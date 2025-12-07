# Close Work Item Action

You are tasked with closing a work item (Issue, PBI, or Task) after successful completion using an automated workflow.

## Overview

This action provides a unified guide for closing work items across platforms (GitHub Issues, Azure DevOps PBIs/Tasks) using the SDO CLI tool. The work item type and platform are determined by the file content and metadata.

## Work Item Types

### Issues (GitHub or Azure DevOps)
Used for closing resolved bugs, completed features, or addressed general tracking items.

**File Format:** Create `.temp/close-issue-message.md` with:
```markdown
# <[issue-number]: Issue Title> - CLOSED

## Target: <github|azure>
## Repository: <owner/repo>
## Work Item ID: <issue-number>
## Work Item Type: Issue

## Closure Summary

<Brief summary of resolution and validation completed>

## Acceptance Criteria Verification
- [x] <Acceptance criterion 1 - completed>
- [x] <Acceptance criterion 2 - completed>
- [x] <Include all criteria marked as completed>

## Testing Completed
- [x] <Testing type and results>
- [x] <Additional validation performed>

## Documentation Updated
- [x] <Documentation changes made>
- [x] <User guides, API docs, etc.>
```

**Guidelines:**
- Title: Use [issue-number] format with " - CLOSED" suffix
- Target: Specify 'github' or 'azure' platform
- Work Item ID: The issue number
- Closure Summary: Brief description of what was accomplished
- Acceptance Criteria: Mark all criteria as completed with [x]
- Testing: Document testing completed
- Documentation: Note any documentation updates

### PBIs (Azure DevOps)
Used for closing completed high-level features, user stories, or epics.

**File Format:** Create `.temp/close-pbi.md` with:
```markdown
# PBI-XXX: [Descriptive Title] - CLOSED

## Target: azdo
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
## Iteration: [FROM project-config.yaml: azure_devops.default_iteration]
## Work Item ID: [PBI_ID]
## Work Item Type: PBI

## Closure Summary
[Comprehensive summary of feature delivery and validation]

## Business Value Delivered
[How this PBI delivered business value]

## Acceptance Criteria Verification
- [x] [All functional requirements implemented]
- [x] [Quality requirements met]
- [x] [Non-functional requirements satisfied]

## Child Tasks Completed
- [x] Task #[ID1] - [Title] - COMPLETED
- [x] Task #[ID2] - [Title] - COMPLETED
- [x] [List all child tasks with completion status]

## Testing Completed
- [x] End-to-end functionality tested
- [x] User acceptance testing completed
- [x] Performance requirements validated
- [x] Security requirements verified

## Documentation Updated
- [x] Code documentation complete
- [x] User guides updated
- [x] API documentation current
- [x] Architecture diagrams updated

## Stakeholder Approvals
- [x] Product Owner: [Name] - APPROVED
- [x] Key Stakeholders: [Names] - APPROVED

## Quality Metrics
- Test Coverage: [XX]%
- Performance: [MET/NOT MET]
- Security: [PASSED/FAILED]
- Documentation: [COMPLETE/PARTIAL]
```

**Note:** This updates the Azure DevOps work item. Azure DevOps remains the source of truth.

### Tasks (Azure DevOps)
Used for closing completed specific work units that implement PBI requirements.

**File Format:** Create `.temp/close-task.md` with:
```markdown
# Task-XXX: [Descriptive Title] - CLOSED

**Parent PBI:** #[PBI_ID] - [PBI Title]

## Target: azdo
## Project: Proto
## Area: Proto\Warriors
## Iteration: Proto\Sprint [XX]
## Work Item ID: [TASK_ID]
## Work Item Type: Task
## Parent ID: [PBI_ID]
## PR ID: [Pull request number]

## Closure Summary
[What was implemented and validated]

## Implementation Details
[Technical approach used and key decisions]

## Acceptance Criteria Verification
- [x] [Specific completion condition met]
- [x] [Code, tests, documentation complete]

## Testing Completed
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Code review completed

## Definition of Done
- [x] Code follows project standards
- [x] Tests pass with adequate coverage
- [x] Code reviewed and approved
- [x] Documentation updated

## Branch Cleanup
- [x] Feature branch merged
- [x] Local branch deleted
- [x] Remote branch deleted

## Effort Actual: [X hours/days]
```

**Note:** This updates the Azure DevOps work item. Azure DevOps remains the source of truth.

## Command
Use the `sdo` tool to close the work item:
```powershell
sdo workitem close --file-path .temp/<filename>.md
```

**Note:** The target platform (GitHub or Azure) and work item type are determined by the `## Target:` and `## Work Item Type:` fields in the file.

## Examples

### Close Resolved Issue
```powershell
# Create issue closure message file (.temp/close-issue-message.md)
# Content follows the Issue format above

# Close issue
sdo workitem close --file-path .temp/close-issue-message.md
# Output: ✓ Issue closed successfully - URL: https://github.com/owner/repo/issues/123
```

### Close Completed PBI
```powershell
# Create PBI closure file (.temp/close-pbi.md)
# Content follows the PBI format above

# Close PBI
sdo workitem close --file-path .temp/close-pbi.md
# Output: ✓ PBI closed successfully - URL: https://dev.azure.com/org/project/_workitems/edit/789
```

### Close Completed Task
```powershell
# Create task closure file (.temp/close-task.md)
# Content follows the Task format above

# Close task
sdo workitem close --file-path .temp/close-task.md
# Output: ✓ Task closed successfully - URL: https://dev.azure.com/org/project/_workitems/edit/101
```

## Post-Closure Workflow
After closure, follow platform-specific next steps:
- **Issues**: Verify closure and update any dependent work items
- **PBIs/Tasks**: Check parent/child relationships and update sprint progress

## Error Handling

### Common Issues:
1. **SDO command fails**: Verify sdo is installed and configured
2. **Authentication issues**: Check Azure DevOps/GitHub credentials
3. **File format issues**: Ensure the file follows the specified format for the work item type
4. **Work item not found**: Verify work item ID and permissions
5. **Validation failures**: Ensure all required fields are properly formatted

### Recovery Steps:
- If SDO fails: Verify tool installation and permissions
- If authentication fails: Reconfigure credentials
- If closure fails: Check file format and work item status
- If validation fails: Review file content against format requirements

## Notes
- Work items require appropriate closure documentation for tracking and auditing
- Always include verification of acceptance criteria completion
- Follow repository's work item closure conventions
- Ensure stakeholder approvals are documented for PBIs
- Maintain traceability between related work items