---
name: prepare-pr-document
description: "Prepare pull request template with current branch changes for submission. Use when: user says 'prepare PR document', 'prepare PR message', 'fill in PR template', 'prepare PR'. Preserves template structure while filling in actual implementation details, ready for `sdo pr create`."
---

# Prepare PR Document

## When to Use

- Need to prepare `.temp/<issue-number>-pr-message.md` with implementation details
- Feature branch has changes ready to be documented
- PR template exists and needs sections filled
- Before executing `sdo pr create`

## Workflow

### Step 1: Verify Template Exists
- Check `.temp/<issue-number>-pr-message.md` exists (created by `sdo wi start`)
- Confirm on correct feature branch

### Step 2: Analyze Changes
```powershell
git diff origin/main --name-only
git diff origin/main --stat
```

### Step 3: Prepare Template (Preserve Structure)

**CRITICAL: Keep all template sections intact**

| Section | Action |
|---------|--------|
| **Title** | Keep `###:` prefix, add descriptive text |
| **Description** | Keep section - explain what changed and why |
| **Changes** | Keep section - list changes in bullet style (short) |
| **Why** | Keep section - list reasons in bullet style (short) |

### Step 4: Verify & Ready for PR
- All template sections filled
- Markdown syntax valid
- Ready for: `sdo pr create -f .temp/<issue-number>-pr-message.md`

## What Changed (Bullet Format)

**Format Example:**
```
### Changes
- Modified StepExecutor.cs: Added verbose logging
- Updated Logger.cs: Implemented centralized logging interface
- Fixed CreateNoWindow: Prevented cmd.exe spawning (3 locations)

### Why
- Better diagnostics during test execution
- Consistent output formatting across components
- Eliminated unwanted process spawning
```

## Checklist

- [ ] Template file exists at `.temp/<issue-number>-pr-message.md`
- [ ] On correct feature branch (matches issue number)
- [ ] Title updated (issue prefix `###:` kept)
- [ ] **All template sections present and filled**
- [ ] Changes listed in bullet style (concise)
- [ ] Why changes made listed in bullet style (concise)
- [ ] Markdown syntax valid

## Next Steps

Execute PR creation:
```powershell
sdo pr create -f .temp/123-pr-message.md
```

## Key Points

- ✅ **PRESERVE template structure** - Never remove or rename sections
- ✅ **Keep issue prefix** in title (e.g., `### 123:`)
- ✅ **Use bullet points** for Changes and Why sections
- ✅ **Keep entries short** - One line per bullet
- ✅ **Template must exist** before preparing
- ✅ **Update template only** - Commit separately if needed
