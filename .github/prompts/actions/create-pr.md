# Create Pull Request Workflow

You are tasked with creating a pull request for the current repository changes using an automated workflow.

## Input
- **Repository name**: The name of the repository (e.g., `home`, `sdo`, `ntools`)
- **Issue created**: Whether an issue has already been created for these changes

## Workflow Steps

### Step 1: Analyze Current Git State
1. Check current branch: `git branch --show-current`
2. Check for uncommitted changes: `git status --porcelain`
3. Get list of changed files: `git diff --name-only`
4. Get detailed changes: `git diff`

### Step 2: Branch Management
**If an issue was already created:**
- Verify you're on the correct feature branch created for the issue
- If not on a feature branch, create one following the issue branch naming pattern

**If on main/master branch (no issue created yet):**
1. Create a feature branch with descriptive name based on changes
   - Use pattern: `feature/<descriptive-name>` or `fix/<descriptive-name>`
   - Example: `feature/add-pr-workflow` or `fix/path-validation`
2. Switch to the new branch: `git checkout -b <branch-name>`

**If already on a feature branch:**
- Continue with existing branch

### Step 3: Commit Changes (if needed)
**If there are uncommitted changes:**
1. Stage all changes: `git add .`
2. Create a descriptive commit message based on the changes
3. Commit: `git commit -m "<message>"`

**If already committed:**
- Verify commits exist: `git log origin/main..HEAD --oneline`

### Step 4: Generate PR Message
Copy the repository's standard PR template and create a file named `<issue-number>-pr-message.md` in the `.temp` directory (`.temp/<issue-number>-pr-message.md` from repo root):

**Standard Template Location:**
- **GitHub**: `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`
- **Azure DevOps**: `.azuredevops/PULL_REQUEST_TEMPLATE.md`

**Command:**
```powershell
# Detect platform and set template path
$remote = git remote -v | Select-Object -First 1
if ($remote -match "github\.com") {
    $templatePath = ".github/PULL_REQUEST_TEMPLATE/pull_request_template.md"
} elseif ($remote -match "dev\.azure\.com") {
    $templatePath = ".azuredevops/PULL_REQUEST_TEMPLATE.md"
} else {
    Write-Host "Unable to detect platform from git remote"
    exit 1
}
# Copy the standard PR template to temp location
cp $templatePath .temp/<issue-number>-pr-message.md

# Edit .temp/<issue-number>-pr-message.md with your PR details
```

**Fill out the template with:**
- Clear, descriptive title following repo conventions (e.g., `[TASK-123] Brief description`)
- Detailed description of changes and business value
- List of key changes made
- Testing information and validation steps
- Links to related work items/issues
- Any breaking changes or special notes

**Note:** The filename must be prefixed with the issue/task number (e.g., `123-pr-message.md` for issue #123).

### Step 5: Push Branch
Push the branch to remote:
```powershell
git push -u origin <branch-name>
```

### Step 6: Create Pull Request with SDO
Use the `sdo` tool to create the PR:
```powershell
sdo pr create --file .temp/<issue-number>-pr-message.md
```

**If work item ID is available:**
```powershell
sdo pr create --file .temp/<issue-number>-pr-message.md --work-item <id>
```

### Step 7: Verify PR Creation
1. Display the PR URL from sdo output
2. Confirm PR was created successfully
3. Show next steps for the user

## Example Execution

**Scenario 1: Direct PR creation (no issue created yet)**

```powershell
# 1. Check current state
git status
# Output: On branch main, Changes not staged for commit: ...

# 2. Create feature branch
git checkout -b feature/enhance-test-batch

# 3. Commit changes
git add .
git commit -m "Enhance TEST_BATCH target with validation phases"

# 4. Copy and edit PR template (.temp/123-pr-message.md)
# Detect platform and copy appropriate template
$remote = git remote -v | Select-Object -First 1
if ($remote -match "github\.com") {
    cp .github/PULL_REQUEST_TEMPLATE/pull_request_template.md .temp/123-pr-message.md
} elseif ($remote -match "dev\.azure\.com") {
    cp .azuredevops/PULL_REQUEST_TEMPLATE.md .temp/123-pr-message.md
}
# Edit .temp/123-pr-message.md with your PR details following the standard template format

# 5. Push branch
git push -u origin feature/enhance-test-batch

# 6. Create PR
sdo pr create --file .temp/123-pr-message.md

# Output:
# ✓ Pull request created successfully
# URL: https://dev.azure.com/org/home/_git/home/pullrequest/123
```

**Scenario 2: PR creation after issue was created**

```powershell
# Assuming issue #456 was already created and branch exists

# 1. Check current state and verify on correct branch
git status
git branch --show-current
# Output: issue/456-enhance-test-batch

# 2. Skip branch creation (already on issue branch)

# 3. Commit any remaining changes
git add .
git commit -m "Complete TEST_BATCH enhancement for issue #456"

# 4. Copy and edit PR template (.temp/456-pr-message.md)
# Detect platform and copy appropriate template
$remote = git remote -v | Select-Object -First 1
if ($remote -match "github\.com") {
    cp .github/PULL_REQUEST_TEMPLATE/pull_request_template.md .temp/456-pr-message.md
} elseif ($remote -match "dev\.azure\.com") {
    cp .azuredevops/PULL_REQUEST_TEMPLATE.md .temp/456-pr-message.md
}
# Edit .temp/456-pr-message.md with your PR details following the standard template format

# 5. Push branch
git push -u origin issue/456-enhance-test-batch

# 6. Create PR linked to the issue
sdo pr create --file .temp/456-pr-message.md --work-item 456

# Output:
# ✓ Pull request created successfully
# URL: https://dev.azure.com/org/home/_git/home/pullrequest/123
```

## Error Handling

### Common Issues:
1. **No changes detected**: Inform user and exit gracefully
2. **Wrong branch when issue exists**: Verify you're on the correct issue branch
3. **Already on feature branch with no new commits**: Check if PR already exists
4. **Branch name conflicts**: Suggest alternative branch name
5. **Push fails**: Check remote access and authentication
6. **SDO command fails**: Verify sdo is installed and configured

### Recovery Steps:
- If commit fails: Review commit message or check for empty commits
- If push fails: Verify remote repository access
- If PR creation fails: Check Azure DevOps/GitHub authentication

## Post-Creation Actions
1. Display PR URL to user
2. Suggest next steps:
   - Review the PR on the platform
   - Request reviewers
   - Link to related work items if not already done
   - Monitor CI/CD pipeline status

## Notes
- Always verify git repository before starting
- If an issue was created first, ensure you're on the correct issue branch
- Preserve existing commit history if on feature branch
- Use meaningful branch and commit messages
- Follow repository's branching strategy
- Link PRs to existing issues when possible using `--work-item` flag
- Check for existing PRs to avoid duplicates
