# Code Review Workflow

This workflow guides the preparation and creation of pull requests for code changes, ensuring proper review processes and integration with Azure DevOps work items.

## Overview

The code review workflow ensures that code changes are properly prepared, documented, and linked to relevant work items before submission for review.

## Prerequisites
- Git repository with changes committed
- Current branch with implemented changes
- Related work item(s) identified
- `sdo` CLI tool available

## Workflow Steps

### Step 1: Prepare Changes for Review
Ensure all changes are committed and tested:

```bash
# Check current status
git status
git log --oneline -5

# Ensure tests pass
# [Run appropriate test commands for your project]
```

### Step 2: Identify Related Work Items
Determine which Azure DevOps work items are addressed by these changes:

```bash
# Check recent commits for work item references
git log --grep="#" --oneline

# Or manually identify work items
# Example: Task #166, PBI #157
```

### Step 3: Create Issue (if needed)
If no related work items were identified in Step 2, create a new issue to track the changes:

**Reference:** `actions/create-issue.md`

**Quick Steps:**
1. Create an issue message file in `.temp/issue-message.md` following the Issue format in `actions/create-workitem.md`
2. Use the `sdo` tool to create the issue:
   ```powershell
   sdo workitem create --file-path .temp/issue-message.md
   ```
3. Note the issue number for use in PR creation

### Step 4: Create Pull Request
Use the dedicated PR creation action to prepare and submit your changes for review:

**Reference:** `actions/create-pr.md`

**Quick Steps:**
1. Follow the PR creation workflow in `actions/create-pr.md`
2. Use issue/task number as filename prefix (e.g., `123-pr-message.md`)
3. Link to related work items when available

**Command:**
```powershell
# Follow the detailed steps in actions/create-pr.md
sdo pr create --file .temp/<issue-number>-pr-message.md --work-item <id>
```

### Step 5: PR Content Validation
Ensure the PR includes:

- [ ] Clear, descriptive title
- [ ] Detailed description of changes
- [ ] Links to related work items
- [ ] Testing instructions
- [ ] Screenshots/screenshots for UI changes
- [ ] Breaking changes documentation

### Step 6: Request Review
- Assign appropriate reviewers
- Add relevant labels
- Set milestone if applicable
- Notify team members

### Step 7: Conduct Code Review
Once reviewers are assigned, the review process begins:

**For Reviewers:**
- Review code changes for correctness, style, and adherence to standards
- Test the changes locally if needed
- Provide constructive feedback with specific suggestions
- Approve or request changes through Azure DevOps PR interface

**For Authors:**
- Address review feedback promptly
- Make requested changes and push updates
- Re-request review after addressing feedback
- Ensure all CI/CD checks pass

### Step 8: Merge and Close
After approval:

```bash
# Merge the PR (if auto-merge not enabled)
az repos pr update --id [PR_ID] --status completed

# Verify task closure
az boards work-item show --id [TASK_ID] --output table

# Clean up branch (optional)
git branch -d azdo-[TASK_ID]
git push azure --delete azdo-[TASK_ID]
```

### Step 9: Squash Merge Process
For approved PRs, follow the squash merge workflow to consolidate commits:

**Reference**: `actions/pr-squash-merge.md`

**Key Steps:**
1. **Generate Squash Commit Message**: Create a concise, meaningful commit message from all PR commits
2. **Execute Squash Merge**: Use GitHub CLI or web interface to squash and merge
3. **Verify Merge Success**: Confirm the merge completed correctly with proper commit message

**Example Squash Merge Command:**
```bash
# Using GitHub CLI for squash merge
gh pr merge [PR_ID] --squash --delete-branch -t "Your consolidated commit message"
```

**Post-Squash Checklist:**
- [ ] Commit message accurately summarizes all changes
- [ ] Single commit created on main branch
- [ ] Feature branch automatically deleted
- [ ] No merge commit created (clean history)
- [ ] CI/CD pipelines trigger on main branch

## PR Title Guidelines

**Format:** `[TASK/PBI-XXX] Brief description`

**Examples:**
- `[TASK-166] Add work item management commands`
- `[PBI-157] Implement Azure DevOps work items API`

## PR Description Format

PR descriptions follow the repository's standard template. See `actions/create-pr.md` for detailed formatting guidelines and the complete PR creation process.

**Standard Template Location:** `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`

**Key Elements:**
- Clear, descriptive title following repo conventions (e.g., `[TASK-123] Brief description`)
- Detailed description of changes and business value
- List of key changes made
- Testing information and validation steps
- Links to related work items/issues

## Review Checklist

### For Reviewers
- [ ] Code follows established patterns and standards
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact assessed
- [ ] Breaking changes properly documented

### For Authors
- [ ] Self-review completed
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Related work items linked
- [ ] No sensitive data committed
- [ ] Branch up to date with main

## Error Handling

**Common Issues:**
- **Work item not linked:** Ensure `--work-item` flag is used with `sdo pr create`
- **Branch conflicts:** Rebase on latest main before creating PR
- **Tests failing:** Ensure all tests pass before requesting review
- **Missing documentation:** Update README and other docs as needed

## Validation Steps

- [ ] PR created successfully
- [ ] Work items properly linked
- [ ] All required checks pass
- [ ] Reviewers assigned
- [ ] Branch protection rules satisfied
- [ ] No merge conflicts
- [ ] **Squash merge executed with proper commit message**
- [ ] Single consolidated commit on main branch
- [ ] Feature branch cleaned up

## Review Completion and Next Steps

### After PR Merge
- [ ] Verify task status shows as "Done"
- [ ] Confirm work item relationships are maintained
- [ ] Check that CI/CD pipelines completed successfully
- [ ] Update any dependent tasks or PBIs as needed

### Transition to Next Task
Once the current task's PR is merged:

1. **Update PBI Progress**: Mark the completed task in the parent PBI
2. **Start Next Task**: Begin the next task in the PBI breakdown
3. **Branch Cleanup**: Delete merged feature branches
4. **Documentation**: Update any release notes or changelogs

**Important**: Always complete one task fully (including PR merge) before starting the next task in a PBI.

### Related Workflows
- **Work Item Start**: `workflows/workitem-start.md` (for implementing individual tasks and coordinating multiple tasks)
- **Testing**: `workflows/testing.md` (for comprehensive testing strategies)
- **PR Creation**: `actions/create-pr.md` (for detailed PR creation steps)