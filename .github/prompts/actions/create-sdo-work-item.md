# Create SDO Work Item Document Skill

## Purpose
Create properly formatted work item markdown documents in `.temp/wi.md` that can be submitted to `sdo wi create` for processing across GitHub and Azure DevOps platforms.

## When to Use
- User asks: "Create a work item document for...", "Generate an issue/PBI/task for...", "Create a work item markdown..."
- Generating issues/tasks from code changes, bugs, features, or improvements
- Creating work items for GitHub Issues or Azure DevOps (PBIs, Tasks, Bugs, Epics)

## Workflow

### Step 1: Determine Work Item Details
Gather from the user request:
1. **Work Item Type**: Issue, PBI, Task, Bug, or Epic
2. **Target Platform**: GitHub or Azure DevOps
3. **Content**: Title, description, acceptance criteria, labels/fields
4. **Metadata**: Assignee, labels, area/iteration (if AZDO), repository

### Step 2: Select Appropriate Template
Based on the target platform and work item type:

**GitHub:**
- Use [issue-gh-example.md](../templates/issue-gh-example.md)
- Set `Target: github` in the document header

**Azure DevOps:**
- **PBI**: Use [issue-azdo-pbi-example.md](../templates/issue-azdo-pbi-example.md)
- **Task**: Use [issue-azdo-task-example.md](../templates/issue-azdo-task-example.md)
- **Bug**: Use [issue-azdo-bug-example.md](../templates/issue-azdo-bug-example.md)
- **Epic**: Use [issue-azdo-epic-example.md](../templates/issue-azdo-epic-example.md)
- Set `Target: azure` in the document header

### Step 3: Generate Work Item Document
Create `.temp/wi.md` following the selected template with:
1. **Target Header Section**: Platform (github/azure), repository, assignee, labels, work item type
2. **Description**: Clear, concise problem statement or goal
3. **Acceptance Criteria**: Checkboxes with testable requirements
4. **Additional Fields**: Any platform-specific metadata (Area, Iteration for AZDO)

### Step 4: Present and Review
- Display the generated `.temp/wi.md` content to the user
- Allow user to review and request modifications
- Once approved, user can execute: `sdo wi create -f .temp/wi.md`

## Example Execution

**User Request:**
> "Create a GitHub issue for adding a new command validation feature"

**Your Response:**
1. Ask clarifying questions (if needed):
   - Specific requirements/acceptance criteria?
   - Who should be assigned?
   - Any labels?
2. Generate `.temp/wi.md` with:
   - Target: github
   - Proper title and description
   - Clear acceptance criteria
   - Relevant labels (e.g., "enhancement", "high-priority")
3. Show the generated content
4. Offer to modify before submission

## Document Structure

```markdown
# [Work Item Title]

## Target: [github|azure]
## Repository: [repo-path]
## Assignee: [user or empty]
## Labels: [comma-separated or empty]
## Work Item Type: [Issue|PBI|Task|Bug|Epic]
## Area: [AZDO only - optional]
## Iteration: [AZDO only - optional]

## Description
[Clear description of the work item]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

[Optional: Additional sections like Design, Testing, etc.]
```

## Key Rules

1. **Always include** the Target header section
2. **Match the template** exactly for the selected platform/type
3. **Use checkboxes** for acceptance criteria
4. **Keep descriptions** clear and actionable
5. **Validate** that all required fields are populated
6. **Location**: Always generate in `.temp/wi.md`
7. **Repository format**: 
   - GitHub: `owner/repo` (e.g., `naz-hage/naz`)
   - Azure DevOps: Project path or auto-detect from config
8. **CRITICAL**: Verify `.temp/sdo-config.yaml` exists before running `sdo wi create`

## Critical: `.temp/sdo-config.yaml` Configuration File

**This file is REQUIRED and PROJECT-SPECIFIC. It must exist before executing `sdo wi create`.**

### Why This File Matters

The `sdo-config.yaml` file is essential because it:
- ✅ Defines the work item type (Issue, PBI, Task, Bug, Epic)
- ✅ Specifies the target platform (GitHub or Azure DevOps)
- ✅ Contains project-specific credentials and platform configuration
- ✅ Is automatically created by SDO during repository initialization
- ✅ Must be present in `.temp/` directory for `sdo wi create` to function

### Before Creating a Work Item

**Always verify:**
1. `.temp/sdo-config.yaml` exists in the repository root
2. The file is configured correctly for the target platform
3. The project-specific settings match your repository setup

**If missing:**
- Initialize SDO for this repository: `sdo init` or similar
- This file is project-specific and automatically generated - do NOT create it manually
- Contact your project administrator if initialization is unclear

## Integration with SDO

Once the document is created and approved, and `.temp/sdo-config.yaml` exists:
```bash
cd [repository-root]
sdo wi create -f .temp/wi.md
```

This will parse the markdown and create the work item on the target platform using the configuration from `.temp/sdo-config.yaml`.

**Troubleshooting:**
- If `sdo wi create` fails: First verify `.temp/sdo-config.yaml` exists
- If configuration error: Ensure SDO has been initialized for this repository
- If platform mismatch: Verify Target field in wi.md matches platform in sdo-config.yaml

## Tips

- For GitHub: Use simple descriptive titles, labels help with filtering
- For AZDO: Include Area and Iteration for better organization
- For acceptance criteria: Make them specific and testable
- Use the templates as reference for consistent formatting
- Ask clarifying questions when the request is ambiguous
