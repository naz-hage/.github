# PBI Creation Workflow

> **Project Configuration**: See `.github/project-config.yaml` for project-specific settings (organization, project, area paths, tools)

This workflow guides the creation of new Product Backlog Items (PBIs) in Azure DevOps, representing high-level features, user stories, or epics that deliver business value.

## Overview

PBIs are the primary planning artifacts that capture business requirements and user needs. They represent complete, valuable increments of functionality that can be developed, tested, and deployed independently. PBIs are created during backlog refinement and product planning activities.

## Prerequisites

- Access to Azure DevOps project (see `project-config.yaml` for organization/project details)
- Understanding of business requirements
- `saz` CLI tool installed and available in PATH (see `project-config.yaml`)
- Azure DevOps authentication configured (see `project-config.yaml` for auth details)

## PBI Creation Workflow

### Phase 1: Requirements Analysis

#### 1.1 Define Business Value
Use the user story template:
```
As a [user type],
I want [functionality],
So that [business value/benefit].
```

#### 1.2 Identify Acceptance Criteria
Create **INVEST** criteria: Testable, Specific, Independent, Negotiable, Valuable, Estimable.

**Example:**
```
- Users can search work items by title, ID, or assignee
- Search results display within 2 seconds
- System handles invalid search terms gracefully
```

#### 1.3 Estimate Effort
Story points scale (see `project-config.yaml` for definitions):
- 1 point: <1 day
- 2 points: 1-2 days
- 3 points: 2-3 days
- 5 points: 3-5 days
- 8 points: 1-2 weeks
- 13+ points: needs breakdown

### Phase 2: PBI Documentation

#### 2.1 Create PBI File
Create temporary file at location specified in `project-config.yaml` (default: `.temp/pbi.md`):

```markdown
# PBI-XXX: [Descriptive Title]

## Target: azdo
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
## Iteration: [FROM project-config.yaml: azure_devops.default_iteration]
## Assignee: [Product Owner or value from project-config.yaml]
## Work Item Type: PBI

## Description
[Clear description of business need and expected outcome]

## Business Value
[Why this PBI matters - impact on users/business]

## Acceptance Criteria
- [ ] [Specific, testable requirement]
- [ ] [Cover functional, performance, usability]
- [ ] [Include error handling scenarios]

## Dependencies
- [ ] [External systems/APIs required]
- [ ] [Other PBIs that must complete first]

## Story Points: [Estimate]
```

**Note:** This is a temporary file. Azure DevOps is the source of truth after creation.

### Phase 3: Azure DevOps Integration

#### 3.1 Create PBI in Azure DevOps
Use the saz CLI tool to create the PBI (saz must be available in PATH):
```bash
# Create PBI using saz workitem create command
saz workitem create --file-path .temp/pbi.md
```

**Example:**
```bash
saz workitem create --file-path .temp/pbi.md
```

**After successful creation:**
- PBI exists in Azure DevOps (source of truth)
- Temp file can be deleted (optional - gitignored anyway)
- All tracking happens in Azure DevOps

### Phase 4: Backlog Refinement

Schedule refinement with team to:
- Clarify requirements and acceptance criteria
- Adjust story point estimates
- Identify dependencies and risks
- Determine when PBI is ready for sprint commitment

**Note:** All PBI updates happen in Azure DevOps (source of truth).
```
# PBI-XXX: Refactor Authentication Module

## Description
Current authentication code has high coupling and is difficult to maintain.

## Business Value
Reduces development time for future authentication features and improves system reliability.

## Acceptance Criteria
- [ ] Authentication logic separated into independent modules
- [ ] Unit test coverage increased to 90%
- [ ] Code complexity reduced by 50%
- [ ] No breaking changes to existing functionality
```

## Error Handling and Recovery

### Common Issues

**Template Validation Errors:**
- Ensure all required sections are completed
- Check markdown formatting is correct
- Verify file naming convention

**Azure DevOps Creation Failures:**
- Verify PAT token is valid and has correct permissions
- Check project and area path exist
- Ensure work item type is available

**Permission Issues:**
- Confirm user has PBI creation permissions
- Verify area path permissions
- Check project access rights

## Success Metrics

### PBI Quality Metrics
- [ ] Acceptance criteria pass rate > 95% on first attempt
- [ ] Story point accuracy within 20% of actual effort
- [ ] PBI cycle time < 2 weeks from creation to completion
- [ ] Team satisfaction with PBI clarity > 4/5

### Process Metrics
- [ ] PBI creation time < 30 minutes
- [ ] Backlog refinement sessions < 1 hour per PBI
- [ ] Time to "Ready" state < 1 week
- [ ] Sprint commitment confidence > 8/10

## Integration with Development Workflow

### Relationship to Tasks
## PBI Examples

### Feature PBI
```markdown
# PBI-XXX: Add User Search Functionality

## Description
Enable work item search by title, ID, or assignee

## Business Value
Improves productivity by reducing manual browsing time

## Acceptance Criteria
- [ ] Search by title, ID, assignee
- [ ] Results within 2 seconds
- [ ] Handles invalid search gracefully

## Story Points: 5
```

### Bug Fix PBI
```markdown
# PBI-XXX: Fix Authentication Timeout

## Description
Users experiencing premature session timeouts

## Business Value
Reduces user frustration and support requests

## Acceptance Criteria
- [ ] 8-hour inactivity timeout
- [ ] Warning 5 minutes before timeout
- [ ] Session extension without re-auth

## Story Points: 3
```

## Next Steps

After PBI creation:
1. **Backlog Refinement** - Review with team, clarify requirements
2. **Sprint Planning** - Commit PBI to sprint
3. **PBI Breakdown** - Follow `workflows/pbi-breakdown.md` to create tasks

## Related Workflows

- [PBI Breakdown](pbi-breakdown.md) - Create tasks from PBI
- [PBI Implementation](pbi-implementation.md) - Track multi-task execution
- [PBI Closure](pbi-closure.md) - Validate completed PBI