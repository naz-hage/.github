# Task Creation Workflow

This workflow guides the creation of Tasks during PBI breakdown and sprint planning. Tasks are the specific, implementable work units that break down PBIs into manageable pieces of development work.

## Overview

Tasks represent concrete development activities that can be completed within a few days. They are created during the PBI breakdown phase when a PBI is committed to a sprint. Each Task should be independently implementable and contribute directly to meeting the parent PBI's acceptance criteria.

## Prerequisites

- Parent PBI in "Committed" state
- PBI breakdown analysis completed (see `pbi-breakdown.md`)
- Sprint capacity established
- Development environment ready

## Task Creation Workflow

### Phase 1: Task Definition

#### 1.1 Analyze PBI Requirements
Review parent PBI acceptance criteria and identify specific implementation units.

#### 1.2 Define Task Scope
Create focused tasks following **INVEST** principles:
- **S**ingle responsibility, **I**ndependent, **T**ime-boxed (1-3 days), **V**erifiable, **V**aluable

#### 1.3 Estimate Effort
- 2-4 hours: Simple fixes, documentation
- 4-8 hours: Single feature implementation
- 1-2 days: Complex feature with testing
- 2-3 days: Major component development

### Phase 2: Task Documentation

#### 2.1 Create Task File
Create `.temp/task.md` (temporary file for Azure DevOps creation):

```markdown
# Task-XXX: [Descriptive Title]

**Parent PBI:** #[PBI_ID] - [PBI Title]

## Target: azdo
## Project: Proto
## Area: Proto\Warriors
## Iteration: Proto\Sprint [XX]
## Parent ID: [PBI_ID]
## Assignee: [Team Member]
## Labels: task
## Work Item Type: Task

## Description
[What needs to be implemented and why]

## Implementation Details
[Technical approach and design decisions]

## Acceptance Criteria
- [ ] [Specific completion condition]
- [ ] [Include code, tests, documentation]
- [ ] [Cover edge cases and errors]

## Dependencies
- [ ] [Prerequisites from other tasks/systems]

## Testing Requirements
- [ ] [Unit/integration tests required]

## Definition of Done
- [ ] Code follows project standards
- [ ] Tests pass with adequate coverage
- [ ] Code reviewed and approved
- [ ] Documentation updated

## Effort Estimate: [X hours/days]
```

**Note:** This is a temporary file. Azure DevOps is the source of truth after creation.

### Phase 3: Azure DevOps Integration

#### 3.1 Create Task in Azure DevOps
```bash
sdo workitem create --file-path .temp/task.md
```

The saz command automatically links the task to its parent PBI when the Parent ID is specified in the markdown file.

**After successful creation:**
- Task exists in Azure DevOps (source of truth)
- Temp file can be deleted (optional - gitignored anyway)
- All tracking happens in Azure DevOps

#### 3.2 Update Parent PBI
Add task reference to PBI's Related Tasks section in Azure DevOps:
```markdown
## Related Tasks
- [Task 1](https://dev.azure.com/.../edit/[ID]): [Task title]
```
After successful creation:

1. **Rename file** to `azdo-[task-number]-[description].md`
2. **Update title** to include work item number
3. **Add Azure DevOps link** in header
4. **Update iteration** to current sprint

#### 3.3 Update Sprint Backlog
Add to sprint tracking:

```bash
# Update sprint capacity tracking
# Add to team's sprint board
# Update burndown charts if applicable
```

### Phase 4: Sprint Planning Integration

#### 4.1 Assign Task to Team Member
Based on skills and capacity:

**Assignment Considerations:**
- [ ] Team member availability in sprint
- [ ] Required technical skills and experience
- [ ] Workload balance across team
- [ ] Knowledge sharing opportunities
- [ ] Risk mitigation (backup resources)

#### 4.2 Set Task State
Initialize task status:

```bash
# Set to "To Do" state initially
az boards work-item update --id [TASK_ID] --fields "System.State=To Do"
```

#### 4.3 Update Sprint Capacity
Track remaining capacity:

**Capacity Tracking:**
- [ ] Update team sprint capacity
- [ ] Adjust for task assignments
- [ ] Identify potential bottlenecks
- [ ] Plan for carry-over if needed

## Task Types and Examples

### API Implementation Task
```
# Task-159: Implement Work Item Search API Client

## Description
Create Azure DevOps REST API client methods for searching work items by various criteria.

## Implementation Details
- Add search methods to AzureDevOpsClient class
- Implement query parameter handling
### Phase 4: Task Examples

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

If your project uses GitHub instead of Azure DevOps for issue tracking, use the issue creation workflow for tasks:

**Reference:** `actions/create-issue.md`

**Quick Steps:**
1. Create an issue message file following the format in `actions/create-issue.md`
2. Use the `sdo` tool to create the issue:
   ```powershell
   sdo issue create --file .temp/issue-message.md --type task
   ```
3. Create a branch using the issue number: `git checkout -b issue/[issue-number]-[description]`

## Next Steps

After task creation:
1. **Implement Task** - Follow `workflows/task-implementation.md`
2. **Track Progress** - Update task status regularly
3. **Close Task** - Follow `workflows/task-closure.md` after completion

## Related Workflows

- [PBI Breakdown](pbi-breakdown.md) - When tasks are created
- [Task Implementation](task-implementation.md) - How to implement tasks
- [Task Closure](task-closure.md) - Task completion validation
- [PBI Closure](pbi-closure.md) - PBI completion after all tasks done