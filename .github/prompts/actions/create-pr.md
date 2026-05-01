# Create Pull Request Document Workflow

You are tasked with creating a pull request markdown document for the current repository changes.

## Input
- **Repository name**: The name of the repository (e.g., `home`, `sdo`, `ntools`)
- **Issue created**: Whether an issue has already been created for these changes

## Workflow Steps

### Step 1: Analyze Current Git State (Optional)
Use git commands to understand your changes before documenting them:

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

### Step 4: Create PR Document

Create a PR document following the standard template format:

**Template Location:**
- **GitHub**: `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`
- **Azure DevOps**: `.azuredevops/PULL_REQUEST_TEMPLATE.md`

**File Naming:** Create `<issue-number>-pr-message.md` in the `.temp/` directory (e.g., `.temp/123-pr-message.md`)

**Instructions:**
1. Review the repository's standard PR template
2. Create PR document following the template structure exactly
3. Replace placeholder values with actual content:
   - Put the PR title on line 1, starting with `[WORKITEM-XXX]` followed by a clear description of the changes
   - Do not keep a placeholder heading like "# Pull Request Template" - replace it with the actual title and content
   - Description: Explain what changed and why
   - Testing: How changes were validated
   - Related work items: Link to issues/tasks
4. Ensure all required fields are populated

### Step 5: Push Branch (Optional)
If ready to push changes to remote:
```powershell
git push -u origin <branch-name>
```

### Step 6: Prepare for Submission
Once the PR markdown document is created and reviewed:
- Ensure all required fields are populated
- Verify the branch is pushed if not already done
- Confirm the document is ready for submission via your team's PR workflow

## Example Execution

**Scenario 1: Create PR document for feature branch**

```powershell
# 1. Review current changes
git status
git diff --name-only

# 2. Create PR markdown document (.temp/123-pr-message.md)
# Following the standard template format:
# ## Title: [ISSUE-123] Brief description of changes
# - Description: What changed and why
# - List of key changes
# - Business value or problem solved
# - Testing and validation details

# 3. Document is ready for review and submission
Write-Host "PR document created: .temp/123-pr-message.md"
Write-Host "Ready for submission via team workflow"
```

**Scenario 2: Create PR document after issue was created**

```powershell
# 1. Verify on correct branch for the issue
git status
git branch --show-current
# Output: 244-issue

# 2. Review changes on this branch
git diff origin/main --name-only

# 3. Create PR markdown document (.temp/244-pr-message.md)
# Following the standard template format:
# ## Title: [ISSUE-244] Feature/fix description
# - Description: What changed and why (linked to issue #244)
# - List of key changes with file names
# - Business value or problem solved
# - Testing and validation details
# - Link to issue #244

# 4. Document is ready for review and submission
Write-Host "PR document created: .temp/244-pr-message.md"
Write-Host "Ready for submission via team workflow (linked to issue #244)"
```

## Document Review Checklist

### Before Finalizing:
1. **Template existence**: Verified that the repository's PR template file exists
2. **Format compliance**: Document structure EXACTLY matches the repository's standard template (not a generic format)
3. **Content completeness**: All required fields are populated
4. **Accuracy**: Description reflects all changes made
5. **Clarity**: Title and description are clear and professional
6. **Links**: Related issues/work items are correctly referenced

### Common Issues:
1. **Missing change details**: Review git diff to capture all changes
2. **Vague descriptions**: Use specific technical details
3. **Incomplete testing info**: Document all testing performed
4. **Missing issue links**: Reference related work items
5. **Formatting errors**: Ensure markdown syntax is valid

## Next Steps After Document Creation
1. Review the PR markdown document for completeness and accuracy
2. Submit the document via your team's PR management workflow
3. Once submitted:
   - Request reviewers
   - Monitor CI/CD checks
   - Address any feedback or review comments
   - Link to related work items if not already done

## Notes
- Always verify git repository before starting
- If an issue was created first, ensure you're on the correct issue branch
- Preserve existing commit history if on feature branch
- Use meaningful branch and commit messages
- Follow repository's branching strategy
- Link PRs to existing issues when possible
- Check for existing PRs to avoid duplicates

## Agent Execution Instructions

To enable an AI agent (like the Copilot coding agent) to perform this task autonomously:
Validate Template Exists**: FIRST, check if the repository's PR template file exists:
   - Try to read `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md` for GitHub
   - Try to read `.azuredevops/PULL_REQUEST_TEMPLATE.md` for Azure DevOps
   - If NEITHER file exists, STOP and ask user to provide the PR template format. Do NOT proceed.
   - If template exists, read its full contents to understand the exact structure and fields required.

2. **Gather Context**: Use tools like `read_file` to access the repository's actual PR template and `list_dir`/`grep_search` to understand the repository structure and current branch state.

3. **Analyze Git State**: Use `run_in_terminal` to execute git commands (`git status`, `git diff`, `git branch`) to understand current changes and branch.

4. **Handle Inputs Dynamically**: Infer inputs like issue number from branch name or file naming conventions. Only prompt the user if information is ambiguous.

5. **Create PR Document**: Generate the PR markdown document using `create_file` in the `.temp/` directory with appropriate naming (`<issue-number>-pr-message.md`). **The document structure MUST EXACTLY MATCH the repository's standard template** - follow the template fields, sections, and format precisely
4. **Create PR Document**: Generate the PR markdown document using `create_file` in the `.temp/` directory with appropriate naming (`<issue-number>-pr-message.md`). Follow the standard template structure with:
6. **Validation**: Review the created document to ensure:
   - All required fields from the template are included
   - Format exactly matches the repository's standard template
   - Completeness and accuracy before providing to user

7. **Complete End-to-End**: Execute all workflow steps sequentially, providing a final summary with document location, format valid
   - Testing information
   - Related issue/work item links

5. **Validation**: Review the created document to ensure completeness and accuracy before providing to user.

6. **Complete End-to-End**: Execute all workflow steps sequentially, providing a final summary with document location, content review, and suggested next steps for submission.

This augmentation allows the agent to create PR documents independently, using available tools to gather information and generate comprehensive PR documentation.
