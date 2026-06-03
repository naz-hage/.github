---
name: split-pbi-into-smaller-pbis
description: "Split a large PBI into smaller PBIs that each can be decomposed into max 3 tasks. Use when: user asks to 'split PBI', 'break down large PBI', 'make PBI smaller', 'size down PBI'. Reads `.temp/<num>-pbi.md`, analyzes scope, generates multiple `.temp/<num>-pbi.md` files using create-sdo-work-item format."
---

# Split Large PBI into Smaller PBIs

## Overview

This skill splits oversized Product Backlog Items into multiple smaller, manageable PBIs. Each resulting PBI is sized so it can be decomposed into a maximum of 3 tasks using the `decompose-sdo-pbi` skill.

## When to Use

Automatically invoke when the user asks to:
- ✅ "Split this PBI into smaller PBIs"
- ✅ "This PBI is too big"
- ✅ "Break down this large PBI"
- ✅ "Make this PBI smaller"
- ✅ "Size down this PBI"
- ✅ "Split into multiple PBIs"

## Workflow Steps

### Step 1: Locate & Validate Large PBI File

Identify the PBI markdown file:
- Look in `.temp/` for files matching pattern `<num>-pbi.md` (e.g., `1-pbi.md`, `42-pbi.md`)
- Read the complete file to extract:
  - **Title**: Main feature/capability
  - **Description**: Full scope and goals
  - **Acceptance Criteria**: All user-facing requirements
  - **Technical Details**: Implementation constraints, dependencies
  - **Scope Indicators**: Why is it too large?

If multiple PBI files exist, ask user which one to split.

### Step 2: Analyze Scope & Identify Split Points

Evaluate the PBI to find natural split points:

**Look for**:
- Sequential phases (Phase 1, Phase 2, Phase 3)
- Component/module boundaries (Auth module, Data layer, API layer)
- Feature variants (Basic version, Advanced features, Admin features)
- User roles/personas (User workflows, Admin workflows)
- Functional areas (Read operations, Write operations, Validation)

**Apply Splitting Strategy**:
1. **Vertical Slicing**: Split by user-facing features/workflows
2. **Horizontal Slicing**: Split by technical layers (if necessary)
3. **Phased Delivery**: Split by delivery phases/milestones
4. **Scope Reduction**: Remove optional/nice-to-have items for later PBIs

**Validate Each Split**:
- Each resulting PBI must decompose into ≤3 tasks
- Each resulting PBI must be independently valuable
- Each resulting PBI must have clear acceptance criteria
- Identify dependencies between resulting PBIs

### Step 3: Generate Smaller PBI Files

Create individual `.temp\<num>-pbi.md` files for each split PBI.

**File Naming Convention**:
```
.temp\wi-1.md   ← Split from original PBI 1 (Part A)
.temp\wi-2.md   ← Split from original PBI 1 (Part B)
.temp\wi-3.md   ← Split from original PBI 1 (Part C)
```

OR (if starting fresh):
```
.temp\wi-2.md    ← New PBI 2
.temp\wi-3.md    ← New PBI 3
.temp\wi-4.md    ← New PBI 4
```

**Template Format**: Use the appropriate template from `create-sdo-work-item` skill:
- **GitHub**: `.github/skills/templates/issue-gh-example.md`
- **Azure DevOps PBI**: `.github/skills/templates/issue-azdo-pbi-example.md`

Each generated `.temp\<num>-pbi.md` file must include:
- Clear, independent title (not just "Part A")
- Description focusing on this slice's scope
- Acceptance criteria specific to this PBI (subset of original)
- `split-from-pbi-<original>` label (for traceability)
- Dependencies on other split PBIs (if any)
- Effort estimate (relative to original)

### Step 4: Present & Review

Display the split strategy and resulting PBIs:

```
📋 PBI SPLITTING ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original PBI: <num>-pbi.md
Reason: <Too many tasks required / Too complex / Too large>
Total PBIs Generated: <count>

Split Strategy: <Vertical slicing / Phased delivery / Component grouping>

✓ PBI 1a: <title> (Task 1, Task 2, Task 3)
✓ PBI 1b: <title> (Task 1, Task 2)
✓ PBI 1c: <title> (Task 1, Task 2, Task 3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dependencies:
  1a → 1b (1b depends on 1a)
  1b → 1c (1c depends on 1b)
```

Show content of each `.temp\<num>-pbi.md`:

````
## 1a-pbi.md
```markdown
<full content>
```

## 1b-pbi.md
```markdown
<full content>
```
````

Ask: "Does this split strategy look correct? Any changes needed?"

### Step 5: Finalize & Generate Files

Once user approves:
- Create all `.temp\<num>-pbi.md` files
- Preserve original PBI for reference (or archive to `.temp/<num>-pbi.original.md`)
- Provide next steps:
  ```bash
  # Next: Decompose each PBI into tasks
  # For each smaller PBI, use decompose-sdo-pbi skill
  ```

## File Structure

```
repository-root/
  .temp/
    1-pbi.md                ← Input (original large PBI)
    wi-1.md              ← Generated (Split PBI 1)
    wi-2.md              ← Generated (Split PBI 2)
    wi-3.md              ← Generated (Split PBI 3)
    sdo-config.yaml        ← MUST EXIST (for later execution)
```

## Key Requirements

- ✅ Read complete PBI file from `.temp/<num>-pbi.md`
- ✅ Analyze scope and identify natural split points
- ✅ Split into 2-4 smaller PBIs (fewer is better)
- ✅ Each resulting PBI must be decomposable into ≤3 tasks
- ✅ Each resulting PBI must be independently valuable
- ✅ Generate all `.temp\<num>-pbi.md` files using standard format
- ✅ Include `split-from-pbi-<original>` label for traceability
- ✅ Map dependencies between split PBIs
- ✅ Validate all required fields before presenting
- ✅ Show full split summary with decomposition estimates for each
- ✅ Display complete content of each resulting PBI file
- ✅ Allow modifications before final approval
- ✅ Preserve original PBI or archive it

## Splitting Best Practices

**DO:**
- ✅ Use vertical slicing (by user workflows/features) as primary strategy
- ✅ Keep each PBI independently valuable and deployable
- ✅ Minimize dependencies between split PBIs
- ✅ Include clear acceptance criteria for each split
- ✅ Reference original PBI number in all splits
- ✅ Estimate effort for each split relative to original
- ✅ Plan phased delivery if appropriate
- ✅ Ask stakeholder for split validation (optional features, sequencing)

**DON'T:**
- ❌ Create too many splits (aim for 2-4, not 10)
- ❌ Split into tiny, undeployable pieces
- ❌ Lose sight of original PBI's overall goal
- ❌ Generate ambiguous PBI titles
- ❌ Create circular dependencies between splits
- ❌ Forget to include acceptance criteria from original
- ❌ Lose traceability to parent PBI

## Integration with Decompose-PBI Workflow

```
User Large PBI (.temp/<num>-pbi.md)
         ↓
    [This Skill: Split]
         ↓
Smaller PBIs (.temp\1a-pbi.md, 1b-pbi.md, 1c-pbi.md, ...)
         ↓
    [decompose-sdo-pbi Skill]
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

**Input**: `.temp/1-pbi.md` (Feature: Complete Azure DevOps Integration)
- Current: 8+ tasks estimated
- Problem: Too large, can't be managed as single PBI

**Split Strategy**: Vertical slicing by authentication model

**Output**:
- `.temp/wi-1.md` - **PBI: Azure AD OAuth Integration** (3 tasks)
  - YAML config parsing & validation
  - OAuth token handling
  - Integration testing
  - Dependencies: None

- `.temp/wi-2.md` - **PBI: PAT (Personal Access Token) Support** (2 tasks)
  - Token storage & management
  - Integration testing
  - Dependencies: wi-1 (basic auth framework)

- `.temp/wi-3.md` - **PBI: Advanced Azure DevOps Features** (3 tasks)
  - Query API integration
  - Webhook support
  - Admin panel features
  - Dependencies: wi-1, wi-2 (basic auth working)
