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
sdo wi show --id [ISSUE_NUMBER]

# For Azure DevOps work items
sdo wi show --id [WORK_ITEM_ID]
```

## Work Item Types

Closing work items follows the same formatting structure as creation. For reference formatting examples, see:

- **GitHub Issues**: [issue-gh-example.md](../templates/issue-gh-example.md)
- **Azure DevOps PBIs**: [issue-azdo-pbi-example.md](../templates/issue-azdo-pbi-example.md)
- **Azure DevOps Tasks**: [issue-azdo-task-example.md](../templates/issue-azdo-task-example.md)

When closing work items, update the corresponding fields with:
- **Closure Summary**: Brief summary of completion and validation
- **Acceptance Criteria**: Mark all items as completed [x]
- **Testing Completed**: Document testing performed
- **Documentation Updated**: Note documentation changes
- **Effort Actual** (Tasks only): Record actual time spent

For detailed examples of how to structure work item documents, refer to the templates folder.

## Command
Use the `sdo` tool to close the work item:
```powershell
sdo wi update --id [WORK_ITEM_ID] --state Done
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
sdo wi update --id 123 --state Done
# Output: ✓ Work item updated successfully - URL: https://github.com/owner/repo/issues/123
```

### Close Completed PBI
```powershell
# Close the PBI
sdo wi update --id 789 --state Done
# Output: ✓ Work item updated successfully - URL: https://dev.azure.com/org/project/_workitems/edit/789
```

### Close Completed Task
```powershell
# Close the task
sdo wi update --id 101 --state Done
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
- If work item not found: Use `sdo wi show --id [ID]` to verify the work item exists
- If PR not merged: Use `sdo pr show [PR_ID]` to check PR status
- If state transition fails: Check work item type and current state with `sdo wi show --id [ID]`

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
4. Execute SDO wi update command
5. Perform branch cleanup and repository synchronization

Use this action consistently across all work item closures to maintain quality standards and proper tracking.