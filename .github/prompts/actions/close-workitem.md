# Close Work Item Action

You are tasked with closing a work item (Issue, PBI, or Task) after successful completion using an automated workflow.

## Prerequisites

Before closing a work item, ensure:

### For All Work Items
- [ ] Implementation completed and tested
- [ ] Code reviewed and approved
- [ ] All acceptance criteria verified
- [ ] Documentation updated
- [ ] No outstanding issues or blockers

### For Issues (GitHub)
- [ ] **PR merged/closed**: Verify the associated pull request has been successfully merged
- [ ] **Linked PR exists**: Ensure PR is properly linked to the issue
- [ ] **CI/CD passed**: All required checks have passed
- [ ] **No merge conflicts**: PR was merged cleanly

### For PBIs/Tasks (Azure DevOps)
- [ ] All child tasks/PBIs completed (for PBIs)
- [ ] Parent PBI updated (for Tasks)
- [ ] Sprint/iteration status updated
- [ ] Stakeholder approval obtained

### Verification Commands

**Check PR status (GitHub):**
```bash
# Check PR merge status
sdo pr show [PR_NUMBER]

# Check PR status details
sdo pr status [PR_NUMBER]
```

**Check issue status:**
```bash
# For GitHub issues
sdo workitem show --id [ISSUE_NUMBER]

# For Azure DevOps work items
sdo workitem show --id [WORK_ITEM_ID]
```

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
sdo workitem update --id [WORK_ITEM_ID] --state Done
```

**Note:** SDO automatically determines the platform (GitHub or Azure DevOps) based on the work item ID and your authentication setup.

**Important:** Use the correct `.temp` directory path for your repository:
- For home repo: `c:\source\home\.temp\<filename>.md`
- For other repos: `<repo-root>\.temp\<filename>.md`

## Examples

### Close Resolved Issue
```powershell
# Check PR status first
sdo pr show 123

# Close the issue
sdo workitem update --id 123 --state Done
# Output: ✓ Work item updated successfully - URL: https://github.com/owner/repo/issues/123
```

### Close Completed PBI
```powershell
# Close the PBI
sdo workitem update --id 789 --state Done
# Output: ✓ Work item updated successfully - URL: https://dev.azure.com/org/project/_workitems/edit/789
```

### Close Completed Task
```powershell
# Close the task
sdo workitem update --id 101 --state Done
# Output: ✓ Work item updated successfully - URL: https://dev.azure.com/org/project/_workitems/edit/101
```

## Post-Closure Workflow
After closure, follow platform-specific next steps:
- **Issues**: Verify closure and update any dependent work items
- **PBIs/Tasks**: Check parent/child relationships and update sprint progress

### Branch Cleanup (Git)
After closing work items, perform branch cleanup:
```bash
# Switch to main branch
git checkout main

# Delete the feature branch locally
git branch -d [branch-name]

# Fetch latest changes from origin
git fetch origin

# Pull latest changes
git pull origin main
```

**Note:** Replace `[branch-name]` with the actual feature branch name used for the work item.

## Error Handling

### Common Issues:
1. **SDO command fails**: Verify sdo is installed and configured
2. **Authentication issues**: Check Azure DevOps/GitHub credentials and PAT tokens
3. **Work item not found**: Verify work item ID exists and you have access
4. **PR not merged**: Ensure associated PR is merged before closing issue
5. **Invalid state transition**: Some work item types may have workflow restrictions

### Recovery Steps:
- If SDO fails: Run `sdo --help` to verify installation
- If authentication fails: Check `AZURE_DEVOPS_PAT` environment variable and GitHub CLI login
- If work item not found: Use `sdo workitem show --id [ID]` to verify the work item exists
- If PR not merged: Use `sdo pr show [PR_ID]` to check PR status
- If state transition fails: Check work item type and current state with `sdo workitem show --id [ID]`

## Notes
- Work items require appropriate closure documentation for tracking and auditing
- Always include verification of acceptance criteria completion
- Follow repository's work item closure conventions
- Ensure stakeholder approvals are documented for PBIs
- Maintain traceability between related work items

---

## Summary
This action provides a comprehensive workflow for closing work items across GitHub Issues and Azure DevOps work items using the unified SDO tool. The process ensures proper verification, documentation, and cleanup after successful completion of development work.

**Key Benefits:**
- **Unified Interface**: Single tool (SDO) for all platforms
- **Complete Verification**: PR status, testing, and acceptance criteria validation
- **Proper Documentation**: Structured closure files for audit trails
- **Branch Management**: Automated cleanup of feature branches
- **Error Handling**: Recovery steps for common issues

**Workflow Steps:**
1. Verify prerequisites and completion status
2. Check PR status (for issues) or work item relationships (for PBIs/Tasks)
3. Create appropriate closure documentation file
4. Execute SDO workitem update command
5. Perform branch cleanup and repository synchronization

Use this action consistently across all work item closures to maintain quality standards and proper tracking.