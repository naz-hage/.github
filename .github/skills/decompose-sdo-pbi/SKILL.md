---
name: decompose-sdo-pbi
description: "Decompose a Product Backlog Item (PBI) into tasks and generate individual SDO work item markdown files. Use when: user asks to 'decompose PBI', 'break down PBI into tasks', 'create tasks from PBI', 'split PBI'. Reads `.temp/<num>-pbi.md`, analyzes requirements, generates `.temp\wi<task#>.md` files using create-sdo-work-item format."
---

# Decompose SDO PBI into Work Items

## Overview

This skill decomposes a Product Backlog Item (PBI) into logically grouped tasks and generates individual work item markdown documents that follow the SDO work item format. Each task becomes a separate `.temp\wi<task#>.md` file ready for `sdo wi create`.

## When to Use

Automatically invoke when the user asks to:
- ✅ "Decompose the PBI into tasks"
- ✅ "Break down the PBI into work items"
- ✅ "Create tasks from this PBI"
- ✅ "Split the PBI into tasks"
- ✅ "Generate work items from the PBI"
- ✅ "Create decomposed tasks for the PBI"

## Workflow Steps

### Step 1: Locate & Validate PBI File

Identify the PBI markdown file:
- Look in `.temp/` for files matching pattern `<num>-pbi.md` (e.g., `1-pbi.md`, `42-pbi.md`)
- Read the complete file to extract:
  - **Title**: From H1 or metadata header
  - **Description**: Main content/goals
  - **Acceptance Criteria**: User-facing requirements
  - **Technical Details**: Implementation constraints, dependencies
  - **Scope**: Effort estimate, priority level

If multiple PBI files exist, ask user which one to decompose.

### Step 2: Analyze & Decompose

Break down the PBI into 1-3 logical tasks following these principles:

**Grouping Strategy**:
- **Feature/Component Grouping**: Related functionality → single task
- **Layer Grouping**: UI → Business Logic → Data → single task per layer
- **Workflow Grouping**: Sequential operations → single task
- **Risk/Complexity Grouping**: High-risk items → dedicated task
- **Testing/Validation**: Separate testing/validation as final task

**For Each task, Identify**:
- Title (concise, action-oriented)
- Description (what needs to be done)
- Acceptance Criteria (checkboxes from PBI criteria, refined for this task)
- Dependencies (which tasks must complete first)
- Effort estimate (S/M/L, or story points)

### Step 3: Generate Work Item Files

Create individual `.temp\wi<task#>.md` files for each decomposed task.

**File Naming Convention**:
```
.temp\wi1.md    ← Task 1
.temp\wi2.md    ← Task 2
.temp\wi3.md    ← Task 3
... etc
```

**Template Format**: Use the appropriate template from `create-sdo-work-item` skill:
- **GitHub**: `.github/skills/templates/issue-gh-example.md`
- **Azure DevOps Task**: `.github/skills/templates/issue-azdo-task-example.md`

Each generated `.temp\wi<task#>.md` file must include:
- `parent-pbi-<num>` label (for traceability)
- `decompose-task` label (to identify as decomposed work)
- Task type (not Epic/PBI)
- Dependency links to related subtasks

### Step 4: Present & Review

Display all generated work items in order:

```
📋 PBI DECOMPOSITION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parent PBI: <num>-pbi.md
Total Tasks Generated: <count>

✓ Task 1: <title>
✓ Task 2: <title>
✓ Task 3: <title>
... etc
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Show content of each `.temp\wi<task#>.md`:

````
## wi1.md
```markdown
<full content>
```

## wi2.md
```markdown
<full content>
```
````

Ask: "Does this decomposition look correct? Any changes needed?"

### Step 5: Finalize & Execute

Once user approves:
- Verify all `.temp\wi<task#>.md` files are created
- Verify `.temp/sdo-config.yaml` exists (required for execution)
- Provide batch creation command:
  ```bash
  # Create all decomposed tasks
  sdo wi create -f .temp\wi1.md
  sdo wi create -f .temp\wi2.md
  sdo wi create -f .temp\wi3.md
  # ... repeat for each task
  ```

Or if SDO supports batch:
  ```bash
  sdo wi create -f .temp\wi*.md
  ```

## File Structure

```
repository-root/
  .temp/
    <num>-pbi.md           ← Input (read by this skill)
    wi1.md                 ← Generated (Task 1)
    wi2.md                 ← Generated (Task 2)
    wi3.md                 ← Generated (Task 3)
    sdo-config.yaml        ← MUST EXIST (for execution)
```

## Key Requirements

- ✅ Read complete PBI file from `.temp/<num>-pbi.md`
- ✅ Extract title, description, acceptance criteria, dependencies
- ✅ Decompose into 3-8 focused tasks
- ✅ Generate all `.temp\wi<task#>.md` files using standard format
- ✅ Each task references parent PBI in labels and description
- ✅ Include dependency relationships between tasks
- ✅ Validate all required fields before presenting
- ✅ Show full decomposition summary with all task titles
- ✅ Display complete content of each wi<task#>.md file
- ✅ Allow modifications before final approval
- ✅ Verify `.temp/sdo-config.yaml` exists before providing execution command
- ✅ Provide batch execution command for all generated tasks

## Decomposition Best Practices

**⚠️ CRITICAL CONSTRAINT:**
- **Maximum 3 tasks per PBI**. If decomposition requires more than 3 tasks, ask user to split PBI into multiple PBIs first.

**DO:**
- ✅ Group logically related work into single tasks
- ✅ Create clear dependencies between tasks
- ✅ Make each task independently understandable
- ✅ Include both feature work and testing/validation
- ✅ Estimate effort for each task
- ✅ Reference parent PBI number in all tasks

**DON'T:**
- ❌ Create too many tiny tasks (fragments work unnecessarily)
- ❌ Create dependencies that can't be parallelized
- ❌ Forget to include testing/validation as a task
- ❌ Generate ambiguous task titles
- ❌ Omit acceptance criteria from tasks
- ❌ Lose traceability to parent PBI

## Integration with SDO Workflow

```
User PBI (.temp/<num>-pbi.md)
         ↓
    [This Skill]
         ↓
Decomposed Tasks (.temp\wi1.md, wi2.md, wi3.md, ...)
         ↓
    [create-sdo-work-item via sdo wi create]
         ↓
    Work Items Created in Azure DevOps/GitHub
         ↓
    Development Team Executes Tasks
```

## Example

**Input**: `.temp/1-pbi.md` (Feature: Azure DevOps Integration)

**Output**:
- `wi1.md` - Task: Design API integration interface
- `wi2.md` - Task: Implement authentication/token handling
- `wi3.md` - Task: Create Azure DevOps REST client
- `wi4.md` - Task: Add configuration management
- `wi5.md` - Task: Write unit tests
- `wi6.md` - Task: Integration testing & validation
