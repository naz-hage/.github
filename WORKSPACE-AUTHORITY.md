# Workspace Configuration Authority

This `.github` folder is the **single source of truth** for all Copilot instructions, skills, and configurations in this multi-root workspace.

## Authority Structure

When `.github` is cloned locally and added as a workspace folder:

- **`.github/.copilot-instructions.md`** → Master instruction registry (all skills, triggers, workflows)
- **`.github/.github/skills/`** → All reusable Copilot skills (7 available)
- **`.github/sdo-config.yaml`** → Workspace-wide configuration
- **`.github/.github/prompts/`** → Reusable prompt templates

## How It Works

1. **Copilot loads instructions** from `.github/.copilot-instructions.md` first
2. **All skills in `.github/.github/skills/`** are available to ALL workspace folders
3. **Other folders** (ntools, ntools-launcher) inherit this configuration automatically
4. **No duplication** - Instructions live in ONE place, accessible everywhere

## For Users & Developers

### Opening the Workspace
```bash
code .code-workspace
```

### Skills Available Everywhere
Whether you're working in `ntools/`, `ntools-launcher/`, or `.github/`, Copilot has access to:
- Create work items
- Prepare PR documents
- Update issues
- Build/test/publish projects
- Run PowerShell scripts

### Adding New Instructions
All new Copilot skills and instructions go in:
```
.github/.github/skills/<skill-name>/SKILL.md
```

Register them in:
```
.github/.copilot-instructions.md
```

They're automatically available to the entire workspace.

## Why This Design

✅ **Single Source of Truth** - No duplicate instructions across folders  
✅ **Automatic Discovery** - Skills load for all workspace folders  
✅ **Easy Onboarding** - New developers just open `.code-workspace`  
✅ **Portable** - `.code-workspace` travels with the repo  
✅ **Scalable** - Add new skills once, available everywhere  
✅ **Maintainable** - Updates in one place apply globally  

## Folder Breakdown

```
source/
├── .code-workspace                # Workspace file (source of truth)
├── .github/                       # Configuration & Authority
│   ├── .copilot-instructions.md  # Master skills registry
│   ├── WORKSPACE-AUTHORITY.md    # This file
│   ├── SETUP.md                  # Setup & onboarding guide
│   ├── .github/
│   │   ├── skills/               # All reusable Copilot skills
│   │   ├── prompts/              # Prompt templates
│   │   └── README.md             # Prompts & skills overview
│   └── sdo-config.yaml           # Shared configuration
├── ntools-launcher/              # Project folder (inherits config)
└── ntools/                        # Project folder (inherits config)
```

## Technical Details

### Workspace File (`.code-workspace`)
- Defines all workspace folders
- Sets `copilot.instructionsLocation` to `.github`
- Enables auto-loading of Copilot configurations
- Portable across machines and environments

### Instruction Resolution Order
1. Copilot checks `.code-workspace` for `instructionsLocation`
2. Loads `.github/.copilot-instructions.md`
3. Discovers all skills in `.github/.github/skills/`
4. Makes all skills available globally (for all folders)

### Skills Availability
- Skills in `.github/.github/skills/` are **automatically accessible** from any workspace folder
- Each skill has auto-invoke triggers (e.g., "create work item", "prepare PR")
- Users don't need to know where skills are located—just speak naturally

## Migration & Cloning

When cloning this workspace to a new machine:

1. Clone the repository
2. Open the workspace:
   ```bash
   code .code-workspace
   ```
3. All instructions and skills load automatically
4. Copilot has full context across all folders

No additional setup needed—the `.code-workspace` file handles everything.
