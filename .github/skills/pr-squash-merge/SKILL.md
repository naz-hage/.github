---
name: pr-squash-merge
description: "Execute squash and merge workflow for pull requests. Use when: user asks to 'squash and merge PR', 'merge PR', 'finalize PR', 'complete PR'. Generates concise squash commit messages from multiple commits, reviews with user, and executes merge via GitHub CLI."
---

# PR Squash and Merge Workflow

## Overview

This skill guides the complete squash and merge process for pull requests, including generating concise commit messages, user confirmation, and executing the merge operation via GitHub CLI.

## When to Use

Automatically invoke when the user asks to:
- ✅ "Squash and merge this PR"
- ✅ "Merge the pull request"
- ✅ "Finalize the PR"
- ✅ "Complete this PR"
- ✅ "Squash merge PR #123"

## Workflow Steps

### Step 1: Verify PR Readiness

Before squash merging, ensure:
- ✅ All CI checks have passed
- ✅ Required reviews are approved
- ✅ The PR description clearly explains the changes
- ✅ No merge conflicts exist
- ✅ PR is in mergeable state

If any checks fail, inform user and stop.

### Step 2: Collect Commit Messages

Retrieve all commits in the PR:
```bash
gh pr view <number> --json commits --jq '.commits[].messageHeadline'
```

Output will be a list of commit messages like:
```
* Commit message 1
* Commit message 2
* Commit message 3
```

### Step 3: Generate Squash Commit Message

Create a single, cohesive commit message that:

**Rules**:
1. **Summarize overall change** - Don't just concatenate messages
2. **Remove duplicates** - Consolidate similar commits
3. **Omit non-relevant comments** - Remove TODOs, temporary notes
4. **Use imperative mood** - Start with verb: "Add", "Fix", "Update", "Refactor"
5. **Keep concise** - Aim for 50-72 characters for first line
6. **Explain what and why** - Purpose, not just mechanics

**Consolidation Patterns**:
- Multiple "Refactor X" → Single "Refactor X and related components"
- Repeated test updates → "Update tests" or omit if they follow implementation
- Documentation updates → Include unless significant enough for separate mention
- Method renames → Include in refactor summary unless primary change

**Example Transformation**:

Input:
```
* Refactor PATH management: centralize operations in PathManager
* Rename DeduplicateAndRewrite to RemoveDuplicatePathSegments
* Update path command to use effective PATH from environment
* Update tests for PATH operations
* Enhance path command documentation with usage examples
```

Output:
```
Refactor PATH management and improve command documentation

- Centralize PATH operations in PathManager
- Rename methods for clarity and add null input validation
- Update path command to display effective PATH from environment
- Enhance documentation with usage examples
```

### Step 4: Present for User Confirmation

Display the prepared squash commit message for review:

```
📋 SQUASH MERGE PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PR: #<number> - <title>

Prepared Squash Commit Message:

<prepared message>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Proceed with squash merge? (y/N):
```

If user says no or requests changes, allow them to modify the message before proceeding.

### Step 5: Execute Squash Merge

Once confirmed, execute merge via GitHub CLI:

```bash
# Squash merge and delete branch
gh pr merge <number> --squash --delete-branch -b "<commit message>"
```

Or if custom message needed:
```bash
gh pr merge <number> --squash --delete-branch -t "Title" -b "Body text"
```

### Step 6: Post-Merge Verification

After successful merge:

```bash
# Update local main branch
git checkout main
git fetch origin
git pull --rebase origin main

# Verify merge
git log --oneline -n 5

# Clean up local branch if still exists
git branch -a | grep <branch-name>
```

**Verify**:
- ✅ PR merged successfully
- ✅ Branch deleted (or offer to delete)
- ✅ Commit message matches prepared message
- ✅ Local main updated with latest changes
- ✅ CI/CD pipelines trigger on main branch
- ✅ Related issues closed if applicable

## Key Requirements

- ✅ Verify PR readiness before proceeding
- ✅ Retrieve all commit messages from PR
- ✅ Consolidate commits into single meaningful message
- ✅ Display prepared message to user for confirmation
- ✅ Allow modifications before execution
- ✅ Execute merge via GitHub CLI with confirmed message
- ✅ Update local main after merge
- ✅ Clean up local branch
- ✅ Verify successful merge completion

## Best Practices

**DO:**
- ✅ Always show prepared squash message before execution
- ✅ Use imperative mood (Add, Fix, Update, Refactor)
- ✅ Consolidate similar commits (don't repeat)
- ✅ Keep first line concise (50-72 chars)
- ✅ Include context about why changes matter
- ✅ Update local main after merge
- ✅ Verify CI/CD runs successfully after merge

**DON'T:**
- ❌ Merge without user confirmation of squash message
- ❌ Use passive voice ("was fixed", "were updated")
- ❌ Include unrelated changes in single squash
- ❌ Forget to update local main after merge
- ❌ Leave dangling local branches
- ❌ Proceed if CI checks failing or PR not ready

## Squash Commit Message Examples

**Good Examples**:
- `Fix PATH command to show effective PATH instead of test values`
- `Refactor PATH management and update documentation`
- `Add null handling to PATH operations and improve error messages`
- `Update development tools to latest stable versions`

**Bad Examples** (avoid):
- `Fix issue #123` (too vague)
- `Update method X and fix bug Y and add test Z` (too many things)
- `WIP: working on PATH stuff` (incomplete)
- `Fixed some bugs and updated tests` (no context)

## Integration with SDO Workflow

```
Feature Development Complete
         ↓
    [This Skill: Squash & Merge]
         ↓
Commit Merged to Main Branch
         ↓
    [CI/CD Pipelines Run]
         ↓
    Production Ready
```

## Troubleshooting

**Common Issues**:
- **Merge conflicts**: Resolve locally, push to branch, retry merge
- **Failing CI**: Address test failures or linting issues before merge
- **Permission denied**: Ensure push and merge permissions
- **Local branch not deleted**: Use `git branch -D <name>` to force delete
- **Local main out of sync**: Run `git checkout main && git fetch origin && git pull --rebase origin main`

**Recovery Steps**:
1. Check PR status: `gh pr view <number>`
2. Verify permissions: `gh auth status`
3. Resolve conflicts if any
4. Update local main after merge
5. Retry if temporary network issues
