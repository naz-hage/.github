---
name: run-ps1
description: Run PowerShell scripts (.ps1 files) directly
triggers:
  - run
  - execute script
  - launch script
  - run script
---

# Run PowerShell Script Skill

## Purpose
Executes PowerShell (.ps1) scripts directly in the terminal without requiring explicit `powershell.exe` or `-ExecutionPolicy` flags. Assumes the terminal is already in PowerShell (user's default).

## When to Use
- User says "run script", "execute test.ps1", "launch build script"
- Need to run any .ps1 file in the workspace
- Building, testing, or deployment scripts

## How to Use

### Simple Syntax
```powershell
.\path\to\script.ps1
```

### With Arguments
```powershell
.\path\to\script.ps1 -Param1 value1 -Param2 value2
```

## Example Commands

**Run test script:**
```powershell
.\.temp\test.ps1
```

**Run build script with parameters:**
```powershell
.\scripts\build.ps1 -Configuration Release -Platform x64
```

**Run from parent directory:**
```powershell
..\other\deploy.ps1
```

## Notes

- The terminal must already be PowerShell (user defaults to PowerShell)
- No need for `powershell.exe -ExecutionPolicy Bypass -File`
- Scripts run in the current PowerShell session, preserving environment variables
- Use relative paths (`.\.temp\test.ps1` not `C:\source\...`)
- If script needs elevated permissions, the current terminal session must have admin privileges

## Common Scripts

| Purpose | Script Location |
|---------|-----------------|
| Build project | `nb build` or custom nbuild.ps1 |
| Run tests | `.\.temp\test.ps1` or custom test runner |
| Deploy | `scripts\deploy.ps1` |
| Setup | `dev-setup\dev-setup.ps1` |
