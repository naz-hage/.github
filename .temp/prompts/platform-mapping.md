# Platform Term Mapping for SDO Tool

This document provides standardized term mappings between the SDO CLI tool, Azure DevOps, and GitHub platforms. This ensures consistent terminology across all workflows and documentation.

## Work Items

| SDO Term | Azure DevOps | GitHub |
|----------|-------------|--------|
| workitem | Work Item | Issue |
| pbi | Product Backlog Item (PBI) | Issue (labeled as "enhancement" or "feature") |
| task | Task | Issue (labeled as "task" or sub-issue) |
| bug | Bug | Issue (labeled as "bug") |
| epic | Epic | Issue (labeled as "epic") |
| feature | Feature | Issue (labeled as "feature") |

## Version Control

| SDO Term | Azure DevOps | GitHub |
|----------|-------------|--------|
| repository | Repository | Repository |
| branch | Branch | Branch |
| pr | Pull Request | Pull Request |
| commit | Commit | Commit |
| tag | Tag | Tag |

## CI/CD and Automation

| SDO Term | Azure DevOps | GitHub |
|----------|-------------|--------|
| pipeline | Pipeline | Actions Workflow |
| build | Build | Actions Run |
| release | Release | Release |
| artifact | Artifact | Artifact |
| deployment | Deployment | Deployment |

## Project Management

| SDO Term | Azure DevOps | GitHub |
|----------|-------------|--------|
| organization | Organization | Organization |
| project | Project/Team Project | Repository |
| team | Team | Team |
| sprint | Iteration/Sprint | Milestone |
| backlog | Backlog | Project Board |
| board | Board | Project Board |

## User and Permissions

| SDO Term | Azure DevOps | GitHub |
|----------|-------------|--------|
| user | User | User |
| group | Group/Security Group | Team |
| permission | Permission | Permission/Role |
| role | Role | Role |

## Notes

- **SDO** represents the unified terminology used by the SDO CLI tool
- **Azure DevOps** uses formal work item types and project structures
- **GitHub** primarily uses Issues with labels to categorize work items
- When creating workflows, use SDO terms as the primary reference and map to platform-specific terms as needed
- For GitHub, sub-issues can be represented using issue relationships or project board hierarchies

## Usage in Workflows

When writing workflow documentation:

1. Use SDO terms as the primary terminology
2. Provide platform-specific mappings when necessary
3. Reference this document for consistency
4. Update this mapping when new terms are introduced

## Example Usage

```markdown
# Create a new work item (SDO term)
# Maps to: PBI in Azure DevOps, Issue in GitHub

sdo work-items create --title "New Feature" --type pbi
```

This mapping ensures that all documentation and tooling can work across multiple platforms while maintaining clarity and consistency.</content>
<parameter name="filePath">c:\source\.github\.temp\prompts\platform-mapping.md