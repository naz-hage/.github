# Copilot Prompts and Instructions

This directory contains structured prompts and instructions to guide Copilot (GitHub Copilot) in providing high-quality assistance for development work in this repository.

## 🎯 Project-Agnostic Workflows

All workflows in this directory are **project-agnostic** and reference **`sdo-config.yaml`** for project-specific settings. This design enables easy transfer to other projects.

**Key Files:**
- **`../sdo-config.yaml`** - SDO configuration (organization, project, tools, authentication, paths)
- **`platform-mapping.md`** - Standardized term mappings between SDO, Azure DevOps, and GitHub
- **`../copilot-instructions.md`** - Project-specific development guidelines

## Directory Structure

```
.github/prompts/
├── README.md                    # This file - overview and usage guide
├── platform-mapping.md          # Standardized term mappings (SDO/AzDO/GitHub)
├── actions/                     # Action-specific prompts (tool commands)
│   ├── README.md               # Action prompts overview
│   ├── create-wi.md            # Create work items
│   ├── update-pr.md            # Update PR message template
│   └── pr-squash-merge.md      # Squash merge pull requests
└── templates/                   # Reusable prompt templates
    └── pull_request_template.md # GitHub PR template for SDO development
```

## Directory Purposes

### Actions Directory
Specific, actionable prompts for executing individual development actions using `sdo` CLI commands. See [actions/README.md](actions/README.md) for comprehensive documentation of all available action commands, file formats, and tool integration details.

### Templates Directory
Reusable prompt templates with detailed step-by-step instructions for particular tools and workflows. These contain:
- **Tool-specific guides**: Instructions for `sdo` CLI commands, PowerShell scripts, etc.
- **Detailed workflows**: Step-by-step processes for specific scenarios
- **Project-specific context**: References to Proto Azure DevOps project and local tooling

## How to Use These Prompts

### For Developers
1. **When starting work**: Use `sdo wi create` to create work items
2. **When updating PRs**: Follow guidelines in `actions/update-pr.md`
3. **When stuck**: Reference action prompts in the `actions/` directory

### For Copilot
These prompts are designed to be referenced in your Copilot chat or used as context. For example:
- "Follow the guidelines in `.github/prompts/actions/update-pr.md`"

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

- `.github/copilot-instructions.md` - General Copilot instructions for this repository
- `.temp/sdo-config.yaml` - SDO configuration file (master template)
- `README.md` - Main repository documentation