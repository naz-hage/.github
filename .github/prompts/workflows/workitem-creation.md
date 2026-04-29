# Work Item Creation Workflow

> **Project Configuration**: See `.temp/sdo-config.yaml` for project-specific settings (organization, project, area paths, tools)

This workflow guides the creation of work items in Azure DevOps, including Product Backlog Items (PBIs) representing high-level features and Tasks representing specific implementation units.

## Overview

Work items are the core artifacts for tracking development work in Azure DevOps. PBIs capture business requirements and user needs, while Tasks break down PBIs into manageable, implementable units. Both are created during different phases of the development lifecycle but follow similar creation processes.

## Prerequisites

- Access to Azure DevOps project (see `sdo-config.yaml` for organization/project details)
- Understanding of business requirements (for PBIs) or parent PBI details (for Tasks)
- `sdo` CLI tool installed and available in PATH (see `sdo-config.yaml`)
- Azure DevOps authentication configured (see `sdo-config.yaml` for auth details)

## Work Item Creation Workflow

### Phase 1: Requirements Analysis

#### 1.1 Define Scope and Value
For **PBIs**: Define business value and requirements clearly:
- What problem does this solve?
- Who benefits from this feature?
- What is the expected outcome?

For **Tasks**: Review parent PBI acceptance criteria and identify specific implementation units.

#### 1.2 Identify Acceptance Criteria
Create **INVEST** criteria: Testable, Specific, Independent, Negotiable, Valuable, Estimable.

**Example:**
```
- Users can search work items by title, ID, or assignee
- Search results display within 2 seconds
- System handles invalid search terms gracefully
```

#### 1.3 Estimate Effort
**For PBIs**: Story points scale (see `sdo-config.yaml` for definitions):
- 1 point: <1 day
- 2 points: 1-2 days
- 3 points: 2-3 days
- 5 points: 3-5 days
- 8 points: 1-2 weeks
- 13+ points: needs breakdown

**For Tasks**: Time-based estimates:
- 2-4 hours: Simple fixes, documentation
- 4-8 hours: Single feature implementation
- 1-2 days: Complex feature with testing
- 2-3 days: Major component development

### Phase 2: Work Item Documentation

#### 2.1 Create Work Item File
Create temporary file in `.temp/` directory following the format examples:

**For different work item types**, see the formatting standards in [actions/create-workitem.md](../actions/create-workitem.md) and the template examples in [templates/](../templates/):
- **PBIs**: See [issue-azdo-pbi-example.md](../templates/issue-azdo-pbi-example.md)
- **Tasks**: See [issue-azdo-task-example.md](../templates/issue-azdo-task-example.md)
- **GitHub Issues**: See [issue-gh-example.md](../templates/issue-gh-example.md)
- **Bugs**: See [issue-azdo-bug-example.md](../templates/issue-azdo-bug-example.md)
- **Epics**: See [issue-azdo-epic-example.md](../templates/issue-azdo-epic-example.md)

Key fields to populate:
- **Target**: Platform (azure or github)
- **Description**: Clear explanation of business need or implementation requirement
- **Acceptance Criteria**: Specific, testable requirements
- **Dependencies**: Any prerequisites or related work items
- **For PBIs**: Include business value and story point estimate
- **For Tasks**: Include parent PBI reference and effort estimate

### Phase 3: Azure DevOps Integration

#### 3.1 Create Work Item in Azure DevOps
Follow the work item creation steps in `actions/create-workitem.md` using the appropriate file format.

**Quick Steps for PBI:**
1. Create `.temp/pbi.md` following the PBI format in `actions/create-workitem.md`
2. Run: `sdo workitem create --file-path .temp/pbi.md`

**Quick Steps for Task:**
1. Create `.temp/task.md` following the Task format in `actions/create-workitem.md`
2. Run: `sdo workitem create --file-path .temp/task.md`

The sdo command automatically links tasks to their parent PBI when the Parent ID is specified.

**After successful creation:**
- Work item exists in Azure DevOps (source of truth)
- Temp file can be deleted (optional - gitignored anyway)
- All tracking happens in Azure DevOps

#### 3.2 Update Related Work Items
For **PBIs**: Schedule refinement with team to clarify requirements.

For **Tasks**: Add task reference to parent PBI's Related Tasks section in Azure DevOps:
```markdown
## Related Tasks
- [Task 1](https://dev.azure.com/.../edit/[ID]): [Task title]
```

#### 3.3 Update Sprint Planning
For **PBIs**: Determine when PBI is ready for sprint commitment.

For **Tasks**: Add to sprint tracking, update capacity, assign to team members.

### Phase 4: Sprint Planning Integration

#### 4.1 Assign Work Item
Based on skills and capacity:

**Assignment Considerations:**
- [ ] Team member availability in sprint
- [ ] Required technical skills and experience
- [ ] Workload balance across team
- [ ] Knowledge sharing opportunities
- [ ] Risk mitigation (backup resources)

#### 4.2 Set Work Item State
Initialize status:

For **PBIs**: Set to "New" or "Approved" state.

For **Tasks**: Set to "To Do" state initially.

#### 4.3 Update Sprint Capacity
Track remaining capacity:
- [ ] Update team sprint capacity
- [ ] Adjust for assignments
- [ ] Identify potential bottlenecks
- [ ] Plan for carry-over if needed

## Work Item Types and Examples

### PBI Examples

#### Feature PBI
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

#### Bug Fix PBI
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

### Task Examples

#### API Development Task
```markdown
# Task-159: Implement Work Item Search API

## Description
Add search capabilities to work item query API

## Implementation Details
- Add search endpoint to REST API client
- Support filtering by title, ID, assignee
- Handle pagination for large result sets

## Acceptance Criteria
- [ ] Search by title, ID, assignee works
- [ ] Response parsing handles all field types
- [ ] Error handling for invalid queries
- [ ] Unit tests cover success/error cases

## Effort Estimate: 1 day
```

#### Documentation Task
```markdown
# Task-163: Update CLI Documentation

## Description
Document new search functionality in README and help

## Implementation Details
- Update README with search examples
- Add CLI help text
- Create usage tutorials

## Acceptance Criteria
- [ ] README includes search examples
- [ ] CLI --help shows search options
- [ ] Examples work as described

## Effort Estimate: 4 hours
```

## For GitHub Projects

If your project uses GitHub instead of Azure DevOps for issue tracking, use the issue creation workflow for features that would be PBIs or Tasks:

**Reference:** `actions/create-workitem.md`

**Quick Steps:**
1. Create an issue message file following the Issue format in `actions/create-workitem.md`
2. Use the `sdo` tool to create the issue:
   ```powershell
   sdo workitem create --file-path .temp/issue-message.md
   ```
3. Note the issue number for branch naming and PR linking

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
- Confirm user has work item creation permissions
- Verify area path permissions
- Check project access rights

## Success Metrics

### PBI Quality Metrics
- [ ] Acceptance criteria pass rate > 95% on first attempt
- [ ] Story point accuracy within 20% of actual effort
- [ ] PBI cycle time < 2 weeks from creation to completion
- [ ] Team satisfaction with PBI clarity > 4/5

### Task Quality Metrics
- [ ] Task completion rate > 90% within estimated time
- [ ] Code review pass rate > 95%
- [ ] Testing coverage meets requirements
- [ ] Definition of Done met for all tasks

### Process Metrics
- [ ] Work item creation time < 30 minutes
- [ ] Refinement sessions < 1 hour per work item
- [ ] Time to "Ready" state < 1 week
- [ ] Sprint commitment confidence > 8/10

## Next Steps

After **PBI** creation:
1. **Backlog Refinement** - Review with team, clarify requirements
2. **Sprint Planning** - Commit PBI to sprint
3. **PBI Breakdown** - Follow `workflows/pbi-breakdown.md` to create tasks

After **Task** creation:
1. **Implement Task** - Follow `workflows/workitem-start.md`
2. **Track Progress** - Update task status regularly
3. **Close Task** - Follow `workflows/workitem-closure.md` after completion

## Related Workflows

- [PBI Breakdown](pbi-breakdown.md) - When tasks are created from PBIs
- [Work Item Start](workitem-start.md) - Complete start workflow for all work item types
- [Work Item Closure](workitem-closure.md) - Task and PBI completion validation