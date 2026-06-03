---
name: create-sdo-work-item
description: "Create work item markdown documents for SDO command execution. Use when: user asks to create a GitHub issue, Azure DevOps PBI/Task/Bug/Epic, work item, or related terms. Generates properly formatted `.temp/wi.md` files that can be submitted to `sdo wi create`."
---

# Create SDO Work Item Document

## Overview

This skill automates the creation of work item markdown documents for the SDO (Simple DevOps Operations) tool. It generates properly formatted documents that can be directly submitted to GitHub Issues or Azure DevOps as work items.

## When to Use

Automatically invoke when the user asks to:
- ✅ "Create a GitHub issue for..."
- ✅ "Generate an issue about..."
- ✅ "Create an Azure DevOps task/PBI/bug for..."
- ✅ "Create a work item for..."
- ✅ "Generate a work item markdown for..."
- ✅ "Create an SDO work item for..."

## Workflow Steps

### Step 1: Clarify Requirements (if needed)

Ask about:
- **Work Item Type**: Issue, PBI, Task, Bug, or Epic
- **Target Platform**: GitHub or Azure DevOps
- **Key Details**: Title, description, acceptance criteria, assignee, labels
- **Repository/Project**: Where should this be created?
- **Critical**: Verify `.temp/sdo-config.yaml` exists in the repository (required for `sdo wi create`)

### Step 2: Generate Document

Create the document based on selected type and platform:
- Use GitHub template for GitHub issues
- Use appropriate Azure DevOps template (PBI/Task/Bug/Epic) for Azure DevOps
- Include proper metadata headers
- Add clear description and acceptance criteria
- File location: `.temp/wi.md` at repository root

### Step 3: Present & Review

- Display the generated `.temp/wi.md` content in a code block
- Ask: "Does this look correct? Any changes needed?"
- Allow user to request modifications before finalizing

### Step 4: Finalize & Execute

- Once approved, verify `.temp/sdo-config.yaml` exists
- Provide the execution command:
  ```bash
  sdo wi create -f .temp/wi.md
  ```
- **Important**: If `.temp/sdo-config.yaml` is missing, inform user that the repository needs SDO initialization

## Document Location & Configuration

```
repository-root/
  .temp/
    wi.md ← Generated here
    sdo-config.yaml ← MUST EXIST (project-specific configuration)
```

### Critical: `.temp/sdo-config.yaml`

**This file is REQUIRED and PROJECT-SPECIFIC:**
- Defines work item type and target platform
- Contains project credentials and configuration
- Automatically created during SDO initialization
- If missing: Repository needs `sdo init` or equivalent setup

## Template Reference

Use these templates for consistency:
- **GitHub**: `.github/skills/templates/issue-gh-example.md`
- **Azure DevOps PBI**: `.github/skills/templates/issue-azdo-pbi-example.md`
- **Azure DevOps Task**: `.github/skills/templates/issue-azdo-task-example.md`
- **Azure DevOps Bug**: `.github/skills/templates/issue-azdo-bug-example.md`
- **Azure DevOps Epic**: `.github/skills/templates/issue-azdo-epic-example.md`

## Key Requirements

- ✅ Always generate `.temp/wi.md` at repository root
- ✅ CRITICAL: Verify `.temp/sdo-config.yaml` exists (required for execution)
- ✅ Match templates exactly for consistency
- ✅ Include checkboxes in acceptance criteria
- ✅ Validate all required fields before presenting
- ✅ Show full content so user can review
- ✅ Allow modifications before final approval
- ✅ Provide execution command for convenience
- ✅ If config missing: Inform user repository needs SDO initialization

## Integration with SDO

The complete workflow:
```
Copilot Skill → .temp/wi.md → User Reviews → sdo wi create -f .temp/wi.md → Work Item Created
```

## Example Interaction

```
User: "Create a GitHub issue for the new validation feature"

You: 
1. Ask clarifying questions if needed
2. Generate .temp/wi.md with:
   - Target: github
   - Title: "Add Validation Feature for SDO Commands"
   - Description of the feature
   - Acceptance Criteria (checkboxes)
   - Labels: enhancement, high-priority
3. Display the content for review
4. Once approved: "Ready! Execute: sdo wi create -f .temp/wi.md"
```
