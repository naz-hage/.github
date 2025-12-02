# Create Issue Workflow

You are tasked with creating an issue for the current repository changes using an automated workflow.

## Workflow Steps

### Step 1: Analyze Current Git State
1. Check current branch: `git branch --show-current`
2. Check for uncommitted changes: `git status --porcelain`
3. Get list of changed files: `git diff --name-only`

### Step 2: Generate Issue Message
Create a file named `issue-message.md` in the `.temp` directory (`.temp/issue-message.md` from repo root) with:

**Format:**
```markdown
# <[issue-number]: Issue Title>

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
- Title: Use [issue-number] format with clear, descriptive title
- Target: Specify 'github' or 'azure' platform
- Repository: Use 'owner/repo' format
- Labels: Use relevant labels like 'backlog', 'bug', 'enhancement'
- Description: Explain the problem or feature clearly and concisely
- Acceptance Criteria: List specific, testable requirements with checkboxes

### Step 3: Create Issue with SDO
Use the `sdo` tool to create the issue:
```powershell
sdo issue create --file .temp/issue-message.md
```

**Options:**
```powershell
sdo issue create --file .temp/issue-message.md --type <bug|feature|task>
sdo issue create --file .temp/issue-message.md --assign <username>
```

### Step 4: Verify Issue Creation
1. Display the issue URL from sdo output
2. Confirm issue was created successfully
3. Note the issue number for potential branch naming

### Step 5: Branch Management
Create a feature branch for the issue using the issue number:
1. Create a feature branch with descriptive name including issue number
   - Use pattern: `issue/<issue-number>-<descriptive-name>` or `bug/<issue-number>-<descriptive-name>`
   - Example: `issue/123-add-validation` or `bug/456-fix-path-handling`
2. Switch to the new branch: `git checkout -b <branch-name>`

### Step 6: Commit Changes (if any)
**If there are uncommitted changes:**
1. Stage all changes: `git add .`
2. Create a descriptive commit message based on the changes
3. Commit: `git commit -m "<message>"`

**If already committed:**
- Verify commits exist: `git log origin/main..HEAD --oneline`

### Step 7: Push Branch (if created)
**If you created a branch:**
Push the branch to remote:
```powershell
git push -u origin <branch-name>
```

## Example Execution

**Bug Report Scenario:**
```powershell
# Check current state
git status

# Create issue message file (.temp/issue-message.md)
# Content follows the format above with [issue-number] title, metadata headers, description, and acceptance criteria

# Create issue and get issue number
sdo issue create --file .temp/issue-message.md --type bug
# Output: ✓ Issue created successfully - URL: https://github.com/owner/repo/issues/123

# Create branch using issue number
git checkout -b issue/123-fix-path-validation

# Make changes and commit
git add .
git commit -m "Fix path validation issue #123"

# Push branch
git push -u origin issue/123-fix-path-validation
```

**Feature Request Scenario:**
```powershell
# Check current state
git status

# Create issue message file (.temp/issue-message.md)
# Content follows the format above with [issue-number] title, metadata headers, description, and acceptance criteria

# Create issue
sdo issue create --file .temp/issue-message.md --type feature
# Output: ✓ Issue created successfully - URL: https://github.com/owner/repo/issues/456

# Create branch using issue number
git checkout -b feature/456-add-yaml-support

# Make changes and commit
git add .
git commit -m "Add YAML configuration support #456"

# Push branch
git push -u origin feature/456-add-yaml-support
```

## Error Handling

### Common Issues:
1. **SDO command fails**: Verify sdo is installed and configured
2. **Authentication issues**: Check Azure DevOps/GitHub credentials
3. **File format issues**: Ensure issue-message.md follows the specified format

### Recovery Steps:
- If SDO fails: Verify tool installation and permissions
- If authentication fails: Reconfigure credentials
- If creation fails: Check file format and content

## Notes
- Issues require a dedicated branch for development work
- Always create a branch after issue creation using the issue number
- Include issue number in branch names for traceability
- Always include enough context for someone else to understand the issue
- Follow repository's issue tracking conventions
- Check for existing issues to avoid duplicates