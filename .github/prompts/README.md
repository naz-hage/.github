# Copilot Prompts and Instructions

This directory contains structured prompts and instructions to guide Copilot (GitHub Copilot) in providing high-quality assistance for development work in this repository.

## 🎯 Copilot Skills & Workflows

All workflows in this directory leverage **Copilot skills** registered in `.copilot-instructions.md`. Skills are:
- **Auto-invocable**: Triggered automatically when you mention related keywords
- **Project-agnostic**: Reference `sdo-config.yaml` for project-specific settings
- **Structured**: Each provides clear step-by-step workflows
- **Integrated**: Output files ready for `sdo` CLI commands

**Quick Start:**
- Create work items: Say "create a GitHub issue"
- Prepare PRs: Say "prepare PR document"
- Update tasks: Say "update issue 35"
- Build/test/publish: Say "build project", "run tests", or "publish nuget"

**Key Files:**
- **`../copilot-instructions.md`** - Master skills registry with all trigger patterns
- **`../skills/`** - Reusable Copilot skills (7 available)
- **`../sdo-config.yaml`** - SDO configuration (organization, project, tools, authentication, paths)

## Directory Structure

```
.github/
├── .copilot-instructions.md     # Workspace skills registry and auto-invoke patterns
├── prompts/
│   ├── README.md                # This file - overview and usage guide
│   ├── platform-mapping.md      # Standardized term mappings (SDO/AzDO/GitHub)
│   ├── actions/                 # Action-specific prompts (tool commands)
│   │   ├── README.md           # Action prompts overview
│   │   ├── create-wi.md        # Create work items
│   │   ├── update-pr.md        # Update PR message template
│   │   └── pr-squash-merge.md  # Squash merge pull requests
│   └── templates/              # Reusable prompt templates
│       └── pull_request_template.md # GitHub PR template for SDO development
└── skills/                      # Reusable Copilot skills for common workflows
    ├── create-sdo-work-item/   # Create work item markdown documents
    ├── prepare-pr-document/    # Prepare PR templates for submission
    ├── update-issue/           # Update issue/task status
    ├── nb-build/               # Build C# projects with nbuild
    ├── nb-test/                # Run tests with nbuild
    ├── nb-nuget/               # Publish NuGet packages
    └── run-ps1/                # Run PowerShell scripts
```

## Directory Purposes

### Skills Directory
Reusable, auto-invocable Copilot skills for common development workflows. Each skill:
- **Has auto-invoke triggers**: Automatically recognized when user mentions related keywords
- **Preserves template structure**: Maintains consistency across workflows (Create SDO Work Item, Prepare PR Document, Update Issue)
- **Provides step-by-step workflows**: Guides developers through multi-phase processes
- **Integrates with SDO commands**: Skills output `.temp/*.md` files ready for `sdo` CLI execution

**Available Skills:**
- `create-sdo-work-item/` - Generate work items for GitHub Issues or Azure DevOps
- `prepare-pr-document/` - Prepare PR templates for `sdo pr create`
- `update-issue/` - Update issue status with acceptance criteria validation
- `nb-build/` - Build C# projects with custom nbuild system
- `nb-test/` - Run tests with custom nbuild system
- `nb-nuget/` - Publish NuGet packages locally
- `run-ps1/` - Execute PowerShell scripts

Comprehensive skill registry: See `.copilot-instructions.md` for all available skills and triggers.

### Actions Directory
Specific, actionable prompts for executing individual development actions using `sdo` CLI commands. See [actions/README.md](actions/README.md) for comprehensive documentation of all available action commands, file formats, and tool integration details.

### Templates Directory
Reusable prompt templates with detailed step-by-step instructions for particular tools and workflows. These contain:
- **Tool-specific guides**: Instructions for `sdo` CLI commands, PowerShell scripts, etc.
- **Detailed workflows**: Step-by-step processes for specific scenarios
- **Project-specific context**: References to Proto Azure DevOps project and local tooling

## How to Use These Prompts & Skills

### For Developers
1. **Creating work items**: Say "create a GitHub issue" or "create a work item" → auto-invokes create-sdo-work-item skill
2. **Preparing PRs**: Say "prepare PR document" or "fill in PR template" → auto-invokes prepare-pr-document skill
3. **Updating tasks**: Say "update issue 35" → auto-invokes update-issue skill
4. **Building/Testing**: Say "build project", "run tests", or "publish nuget" → auto-invokes respective nbuild skills
5. **Running scripts**: Say "run script" → auto-invokes run-ps1 skill

### For Copilot
These skills are designed to auto-invoke based on user intent. For reference:
- All skills are registered in `.copilot-instructions.md` with trigger patterns
- Each skill has a SKILL.md file with complete workflow documentation
- Skills output `.temp/*.md` files ready for `sdo` CLI commands

### Manual References
If auto-invoke doesn't trigger, explicitly reference:
- Skills directory: `.github/skills/<skill-name>/SKILL.md`
- Action prompts: `.github/prompts/actions/<action-name>.md`
- Instructions: `.copilot-instructions.md`

## Contributing

When adding new prompts:
1. Place them in the appropriate subdirectory
2. Follow the naming convention: `kebab-case.md`
3. Include clear descriptions and examples
4. Update this README if adding new subdirectories

## Best Practices

- **Be specific**: Prompts work best when they provide clear, specific guidance
- **Include context**: Reference repository standards, technologies, and conventions
- **Show examples**: Include before/after examples whenever possible
- **Keep updated**: Review and update prompts as the repository evolves

## Related Files

- `.github/copilot-instructions.md` - Skills registry with auto-invoke trigger patterns
- `.github/skills/` - Reusable Copilot skills for common workflows
- `.github/prompts/actions/` - Action-specific development prompts
- `.temp/sdo-config.yaml` - SDO configuration file (master template)
- `README.md` - Main repository documentation