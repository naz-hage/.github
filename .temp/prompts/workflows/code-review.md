# Code Review Workflow

This workflow guides the preparation and creation of pull requests for code changes, ensuring proper review processes and integration with Azure DevOps work items.

## Overview

The code review workflow ensures that code changes are properly prepared, documented, and linked to relevant work items before submission for review.

## Prerequisites
- Git repository with changes committed
- Current branch with implemented changes
- Related work item(s) identified
- `saz` CLI tool available

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

### Step 3: Prepare Pull Request
Use the `saz pr create` command to prepare and create the PR:

```bash
# Copy PR template to temp location
cp .github/PULL_REQUEST_TEMPLATE/pull_request_template.md .temp/pr.md

# Edit .temp/pr.md with your PR details

# Create the pull request
saz pr create --file .temp/pr.md --work-item 166

# Temp file is cleaned up automatically
```

**Command Options:**
- `--file`: Path to markdown file with PR details (use `.temp/pr.md`)
- `--work-item`: Related Azure DevOps work item number
- `--draft`: Create as draft PR (optional)
- `--update-pr`: Update existing PR by ID (optional)

### Step 4: PR Content Validation
Ensure the PR includes:

- [ ] Clear, descriptive title
- [ ] Detailed description of changes
- [ ] Links to related work items
- [ ] Testing instructions
- [ ] Screenshots/screenshots for UI changes
- [ ] Breaking changes documentation

### Step 5: Link Work Items
Ensure PR is properly linked to Azure DevOps work items:

```bash
# Check work item links
az repos pr work-items list --id [pr_number]
```

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

**Reference**: `workflows/pr-squash-merge.md`

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

Use the standard PR template at `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`:

```markdown
## Description
<!-- What changed and why -->

## Changes Made
<!-- Bullet list of key changes -->
- 
- 

## Why These Changes
<!-- Business value or problem solved -->

## Testing
<!-- How you validated the changes -->
- [ ] Tests pass (`make test` or `pytest`)
- [ ] Code quality checks pass (`make lint`)

## Screenshots/Demos
<!-- If applicable, add screenshots or demos -->

## Breaking Changes
<!-- Only if applicable -->

## Notes
<!-- Anything else reviewers should know -->
```

**Note:** When creating a PR on GitHub/Azure DevOps, this template will be automatically loaded.

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
- **Work item not linked:** Use `az repos pr work-item add` to link work items
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
- **Task Implementation**: `workflows/task-implementation.md` (for implementing individual tasks)
- **PBI Implementation**: `workflows/pbi-implementation.md` (for coordinating multiple tasks)
- **Testing**: `workflows/testing.md` (for comprehensive testing strategies)