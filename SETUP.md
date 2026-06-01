# Multi-Root Workspace Setup Guide

Welcome! This guide explains how to set up and use the workspace with centralized Copilot instructions.

## Quick Start

### 1. Open the Workspace
```bash
code .code-workspace
```

That's it! All Copilot skills and instructions load automatically.

### 2. Verify Setup
- You should see 3 folders in the Explorer:
  - 📋 Configuration (Source of Truth) ← `.github` folder
  - ntools-launcher
  - ntools
- Copilot should be ready to use

### 3. Try a Skill
Try one of these commands in Copilot chat:
- "Create a GitHub issue for..." → Invokes `create-sdo-work-item` skill
- "Prepare PR document" → Invokes `prepare-pr-document` skill
- "Build project" → Invokes `nb-build` skill
- "Run tests" → Invokes `nb-test` skill

## Workspace Structure

```
source/
├── .code-workspace                # ← Open this file to start
├── .github/                       # ← Source of truth for all instructions
│   ├── .copilot-instructions.md  # Master skills registry
│   ├── WORKSPACE-AUTHORITY.md    # Authority & configuration structure
│   ├── SETUP.md                  # This file
│   ├── .github/
│   │   ├── skills/
│   │   │   ├── create-sdo-work-item/   # Create GitHub/Azure DevOps items
│   │   │   ├── prepare-pr-document/    # Prepare PR templates
│   │   │   ├── update-issue/           # Update issue status
│   │   │   ├── nb-build/               # Build C# projects
│   │   │   ├── nb-test/                # Run tests
│   │   │   ├── nb-nuget/               # Publish NuGet packages
│   │   │   └── run-ps1/                # Run PowerShell scripts
│   │   ├── prompts/
│   │   │   ├── README.md               # Prompts overview
│   │   │   ├── actions/                # Action-specific prompts
│   │   │   └── templates/              # Reusable templates
│   │   └── README.md                   # Skills & prompts documentation
│   ├── sdo-config.yaml                 # Workspace configuration
│   └── README.md                       # Configuration overview
├── ntools-launcher/                    # C# launcher project
└── ntools/                             # Main C# project
```

## Available Copilot Skills

All these skills are auto-invocable from any workspace folder:

### Work Item Management
- **Create SDO Work Item** - "create a GitHub issue" / "create a work item"
- **Prepare PR Document** - "prepare PR document" / "fill in PR template"
- **Update Issue** - "update issue 35" / "mark issue done"

### Build & Test
- **NB Build** - "build project" / "build" / "compile"
- **NB Test** - "run tests" / "test" / "execute tests"
- **NB NuGet** - "publish nuget" / "build package"
- **Run PowerShell** - "run script" / "run ps1"

See `.github/.copilot-instructions.md` for complete skill registry.

## How Instructions Work

### Single Source of Truth
All Copilot instructions live in **one place**: `.github/.copilot-instructions.md`

When you're working in any folder (`ntools/`, `ntools-launcher/`, etc.), Copilot loads instructions from `.github` automatically.

### Auto-Invoke Triggers
Each skill has trigger patterns. For example:
- "create issue" → auto-invokes `create-sdo-work-item` skill
- "prepare PR" → auto-invokes `prepare-pr-document` skill
- "build project" → auto-invokes `nb-build` skill

Just speak naturally, and Copilot recognizes the intent.

### Manual References
If auto-invoke doesn't trigger, explicitly reference:
```
See .github/.github/skills/prepare-pr-document/SKILL.md
```

## Adding New Skills

### Step 1: Create the Skill
```
.github/.github/skills/<skill-name>/SKILL.md
```

Example: `.github/.github/skills/my-new-skill/SKILL.md`

### Step 2: Register It
Add to `.github/.copilot-instructions.md`:
```markdown
### My New Skill

**Triggers:** "my skill", "do something"

Description of what the skill does.

**Skill:** [My New Skill](./.github/skills/my-new-skill/SKILL.md)
```

### Step 3: Done!
The skill is automatically available to all workspace folders.

## Folder-Specific Notes

### `.github/` Folder
**Purpose:** Master configuration and skill definitions
- All Copilot instructions live here
- All skill files live here
- Central point of maintenance

**Do NOT create** duplicate `.copilot-instructions.md` files in other folders.

### `ntools/` & `ntools-launcher/` Folders
**Purpose:** Project code
- Contains C# projects
- Can have project-specific `.instructions.md` (optional, for local overrides only)
- Inherits all skills from `.github/` automatically

**Can have** local `.instructions.md` for project-specific guidance (optional):
```
ntools/.instructions.md                # Optional: Project-specific notes only
ntools-launcher/.instructions.md       # Optional: Project-specific notes only
```

But **master instructions** always come from `.github/`.

## Troubleshooting

### "Copilot isn't finding my skill"
1. Check `.github/.copilot-instructions.md` - is the skill registered?
2. Verify the path is correct in the registration
3. Reload VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"

### "Instructions aren't loading"
1. Check that you opened `.code-workspace` (not individual folders)
2. Verify `.github/.copilot-instructions.md` exists
3. Check VS Code settings for `copilot.instructionsLocation`

### "Which folder are these instructions from?"
All master instructions are in `.github/.copilot-instructions.md`. That's the source of truth. Project-specific notes may exist in individual folders (optional).

## Best Practices

✅ **DO:**
- Keep master instructions in `.github/.copilot-instructions.md`
- Register all skills in the master instructions file
- Use `.code-workspace` to open the workspace
- Reference `.github/` folder for all configuration questions

❌ **DON'T:**
- Create duplicate instruction files in `ntools/` or `ntools-launcher/`
- Edit instructions in multiple places (maintenance nightmare)
- Close individual folders and open them separately
- Modify Copilot settings in VS Code settings (use `.code-workspace`)

## For Team Members

### New Developer Checklist
- [ ] Clone the repository
- [ ] Open `.code-workspace`
- [ ] Verify all 3 folders appear in Explorer
- [ ] Try a Copilot skill (e.g., "build project")
- [ ] Read this SETUP.md file
- [ ] Review `.github/.copilot-instructions.md` for available skills

### Questions?
See:
- **`.github/WORKSPACE-AUTHORITY.md`** - How the workspace authority structure works
- **`.github/.copilot-instructions.md`** - Complete skill registry
- **`.github/.github/prompts/README.md`** - Detailed skill documentation

## Summary

| Question | Answer |
|----------|--------|
| How do I open the workspace? | `code .code-workspace` |
| Where are instructions? | `.github/.copilot-instructions.md` |
| How do I use skills? | Say natural language commands (e.g., "create issue") |
| Where are skill files? | `.github/.github/skills/` |
| How do I add a new skill? | Create folder in `.github/.github/skills/`, register in master instructions |
| What if I'm in `ntools/` folder? | You inherit all `.github/` instructions automatically |
| Do I need to copy instructions elsewhere? | No—`.github/` is the single source of truth |

---

**Ready to go!** Open `.code-workspace` and start using Copilot skills across your entire workspace.
