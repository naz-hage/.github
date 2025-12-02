# PR Squash Merge Workflow

You are tasked with guiding the squash and merge process for pull requests, including generating concise commit messages and executing the merge operation.

## Squash Merge Process

### Step 1: Review the PR
Before squash merging, ensure:
- All CI checks have passed
- Required reviews are approved
- The PR description clearly explains the changes
- No merge conflicts exist

### Step 2: Generate Squash Commit Message
Create a concise, meaningful squash commit message from multiple individual commit messages in a pull request.

## Input Format
You will receive a list of commit messages from commits that are being squashed together, typically in this format:
```
* Commit message 1
* Commit message 2
* Commit message 3
...
```

## Output Requirements
Create a single, cohesive commit message that:

1. **Summarizes the overall change** - Don't just concatenate messages
2. **Removes duplicates** - If multiple commits say similar things, consolidate them
3. **Omits non-relevant comments** - Remove TODOs, temporary notes, or irrelevant details
4. **Uses imperative mood** - Start with a verb like "Add", "Fix", "Update", "Refactor", etc.
5. **Is concise but descriptive** - Aim for 50-72 characters for the first line
6. **Focuses on what changed and why** - Explain the purpose, not just the mechanics

## Guidelines

### Good Examples
- `Fix PATH command to show effective PATH instead of test values`
- `Refactor PATH management and update documentation`
- `Add null handling to PATH operations and improve error messages`

### Bad Examples (avoid these)
- `Update method X and fix bug Y and add test Z` (too many things)
- `Fix issue #123` (too vague, no context)
- `WIP: working on PATH stuff` (incomplete, not ready for commit)

### Common Patterns to Consolidate
- Multiple "Refactor X" messages → Single "Refactor X and related components"
- Repeated test updates → "Update tests" or omit if tests are just following implementation changes
- Documentation updates → Include in main change or separate if significant
- Method renames → Include in refactor summary unless it's the main change

## Process
1. **Analyze all messages** - Understand the overall scope and purpose
2. **Identify duplicates** - Group similar changes together
3. **Find the main theme** - What is the primary goal of these changes?
4. **Remove noise** - Filter out temporary or irrelevant messages
5. **Craft summary** - Write a clear, concise description

## Step 3: Execute Squash Merge

### Step 3a: Review Prepared Commit Message
Before executing the merge, always show the user the prepared squash commit message for confirmation:

**Example Output:**
```
📝 Prepared Squash Commit Message for PR #192:

Update development tools to latest versions and deprecate Update-DocVersions command

- Updated 15+ development tools to latest stable versions (kubectl 1.34.1, MongoDB 8.2.1, Node.js 22.21.0, Python 3.14.0, etc.)
- Removed deprecated Update-DocVersions PowerShell function
- Replaced with MSBuild target `nb update_doc_versions` for automated documentation updates
- Updated ntools.md and version automation guides

✅ Proceed with squash merge? (y/N): 
```

### Step 3b: Execute the Merge

Once confirmed, execute the merge using one of these methods:

### Using GitHub CLI
```bash
# List open PRs
gh pr list

# Squash merge a specific PR (replace #123 with actual PR number)
gh pr merge 123 --squash --delete-branch

# Or merge with custom commit message
gh pr merge 123 --squash --delete-branch -t "Your custom commit message"

# After merge: Update local main branch
git checkout main
git fetch origin
git pull --rebase origin main

# If local branch still exists after merge, clean it up
git branch -d branch-name  # Use -D if branch not fully merged
```

### Alternative: Using GitHub Web Interface
1. Navigate to the PR on GitHub
2. Click the **"Squash and merge"** button
3. Edit the commit message if needed
4. Click **"Confirm squash and merge"**
5. Delete the branch if prompted

### Post-Merge Checklist
- [ ] PR is merged successfully
- [ ] Branch is deleted (if using --delete-branch)
- [ ] Local branch is cleaned up (run `git branch -d <branch-name>` if needed)
- [ ] Switch to main branch and update local repository
- [ ] Commit message matches the prepared squash message
- [ ] CI/CD pipelines trigger on main branch
- [ ] Related issues are closed if applicable
- [ ] Team is notified of the merge if needed

## Example Transformation

## Example Transformation

**Input:**
```
* Refactor PATH management: centralize operations in PathManager and update related tests
* Refactor PATH management: consolidate methods in PathManager and update related tests
* Rename DeduplicateAndRewrite method to RemoveDuplicatePathSegments and update related tests for clarity
* Update RemovePath and AddAppInstallPathToEnvironmentPath methods to handle null or empty inputs gracefully and adjust related tests
* Update DisplayPathSegments method to retrieve PATH directly from the environment variable, ensuring it defaults to an empty string if not set
* Add summary documentation for UpdateEnvironmentVariables method and clean up unused usings in PathManager
* Enhance 'path' command documentation to clarify output and include usage examples
```

**Output:**
```
Refactor PATH management and improve command documentation

- Centralize PATH operations in PathManager with better error handling
- Rename methods for clarity and add null input validation
- Update path command to use effective PATH and enhance documentation
```

## Step 4: Verify Merge Success

After squash merging, verify:
- The commit appears on the main branch with your crafted message
- All files are correctly merged
- No unintended changes occurred
- CI/CD pipelines are running successfully
- Commit message matches exactly what was prepared and confirmed
- Local branch is cleaned up (run `git branch -a` to verify)
- Local main branch is up to date with origin (run `git status` to check)

## Troubleshooting

### Common Issues:
- **Merge conflicts**: Resolve conflicts locally before merging
- **Failing CI**: Address any test failures or linting issues
- **Permission denied**: Ensure you have merge permissions for the repository
- **Branch protection**: Some repositories require specific conditions before merging
- **Local branch not deleted**: Use `git branch -D branch-name` to force delete unmerged branches

### Recovery:
- If merge fails, you can abort and try again
- Use `gh pr merge --abort` to cancel an in-progress merge
- Check PR status with `gh pr view <number>`
- After merge: Always update local main with `git checkout main && git fetch origin && git pull --rebase origin main`

## Additional Notes
- If the changes span multiple major areas, consider a multi-line format
- Keep the tone professional and technical
- Focus on user-facing changes when possible
- If changes are purely internal/refactoring, make that clear in the message
- Always test the merge on a separate branch first if you're unsure
- **Always review the prepared squash commit message before executing the merge** - this ensures the consolidated message accurately represents the changes
- **Always update your local main branch after merging** - run `git checkout main && git fetch origin && git pull --rebase origin main` to stay in sync