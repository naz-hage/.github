# PBI Breakdown and Sprint Planning Workflow

This workflow guides the process of breaking down a committed PBI into implementable Tasks, ensuring each acceptance criterion becomes a specific, actionable work item that can be implemented independently.

## Overview

When a PBI is committed to a sprint, it needs to be decomposed into smaller, manageable Tasks. Each Task represents a specific implementation unit that can be completed within a few days and clearly contributes to meeting the PBI's acceptance criteria.

## Prerequisites

- PBI exists and is in "Committed" state
- PBI has clear, specific acceptance criteria
- Sprint capacity known
- Development environment ready

## Breakdown Workflow

### Phase 1: PBI Analysis

#### 1.1 Review PBI Details
```bash
az boards work-item show --id [PBI_ID] --output table
```

Verify: PBI state is "Committed", acceptance criteria are specific and testable.

#### 1.2 Analyze Acceptance Criteria
Break down each criterion into technical requirements, identify dependencies and risks.

#### 1.3 Assess Technical Complexity
Evaluate: new vs existing functionality, database/API/UI changes, testing needs.

### Phase 2: Task Creation

#### 2.1 Define Task Structure
Create tasks following **INVEST** principles:
- **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall (1-3 days), **T**estable

#### 2.2 Create Implementation Tasks
Follow `workflows/workitem-creation-workflow.md` to create task markdown files in `.temp/` (temporary location).

**Create each task:**
```bash
# Create .temp/task.md following workitem-creation-workflow.md template
saz workitem create --file-path .temp/task.md
```

**Update PBI Related Tasks Section in Azure DevOps:**
```markdown
## Related Tasks
- [Task 1](https://dev.azure.com/.../_workitems/edit/166): Create work_items module
- [Task 2](https://dev.azure.com/.../_workitems/edit/167): Add REST API methods
- [Task 3](https://dev.azure.com/.../_workitems/edit/168): Update CLI commands
```

**Implementation Order:** Tasks executed in ranked order (Task 1, Task 2, Task 3...).

**Note:** All task tracking happens in Azure DevOps (source of truth). Local `.temp/task.md` is only used for creation.

#### 2.3 Task Examples

**Example: "Add Work Item Management Commands"**
- Task 1: Implement work item query API methods (2 days)
- Task 2: Create CLI command handlers (3 days)
- Task 3: Add error handling (1 day)
- Task 4: Implement tests >80% coverage (2 days)
- Task 5: Update documentation (1 day)

### Phase 3: Sprint Capacity Planning

#### 3.1 Calculate Sprint Capacity
Determine available effort for the sprint:

**Capacity Calculation:**
- Team size × working days × focus factor (0.6-0.8)
- Account for meetings, reviews, and overhead
- Consider team member availability
- Include buffer for unexpected issues

#### 3.2 Prioritize and Sequence Tasks
Order tasks for optimal delivery:

**Task Sequencing Strategies:**
- **Dependency-based**: Complete prerequisites first
- **Risk-based**: Address high-risk items early
- **Value-based**: Deliver high-value features first
- **Learning-based**: Tackle unknowns early for learning

#### 3.3 Assign Tasks to Team Members
Distribute work based on skills and capacity:

**Assignment Considerations:**
- [ ] Team member availability and capacity
- [ ] Required skills and expertise
- [ ] Workload balance across sprint
- [ ] Knowledge sharing opportunities
- [ ] Risk mitigation (no single points of failure)

### Phase 4: Task Refinement and Commitment

#### 4.1 Refine Task Descriptions
Ensure each task is clearly defined:

**Task Definition Checklist:**
- [ ] Title clearly describes the work
- [ ] Description includes acceptance criteria
- [ ] Effort estimate is agreed upon
- [ ] Dependencies are documented
- [ ] Success criteria are defined

#### 4.2 Add Task Details in Azure DevOps
Populate all relevant fields:

```bash
# Update task with detailed information
az boards work-item update --id [TASK_ID] --fields \
  "System.Description=[Detailed description with acceptance criteria]" \
  "Microsoft.VSTS.Scheduling.Effort=[effort estimate]" \
  "System.AssignedTo=[team member email]" \
  "Microsoft.VSTS.Common.Priority=[priority 1-4]" \
  "System.Tags=[relevant tags]"
```

#### 4.3 Commit Sprint Plan
Finalize the sprint commitment:

**Sprint Commitment Checklist:**
- [ ] All tasks are estimated and assigned
- [ ] Total effort fits within sprint capacity
- [ ] Dependencies are understood and acceptable
- [ ] Risks are identified and mitigated
- [ ] Team confidence in commitment is high
- [ ] Stakeholders agree with plan

### Phase 5: Sprint Start Preparation

#### 5.1 Update PBI Status
Mark PBI as actively being worked:

```bash
# Update PBI to show work has started
az boards work-item update --id [PBI_ID] --fields \
  "System.History=Sprint planning complete. [X] tasks created and assigned. Development beginning."
```

#### 5.2 Set Up Development Environment
Ensure team is ready to start:

**Environment Preparation:**
- [ ] Development branches created
- [ ] Access permissions verified
- [ ] Development tools installed
- [ ] Testing environments ready
- [ ] CI/CD pipelines configured

#### 5.3 Schedule Sprint Ceremonies
Plan the sprint execution:

**Sprint Rhythm:**
- Daily standups: [time and format]
- Mid-sprint check-in: [date and focus]
- Sprint review preparation: [approach]
- Retrospective planning: [format]

## Task Breakdown Patterns

### Pattern 1: Feature Implementation
**PBI**: "Add user authentication to CLI"

**Tasks Created:**
1. **API Client Methods** (2 days)
   - Implement login/logout API calls
   - Add token storage and refresh logic

2. **CLI Commands** (2 days)
   - Add `saz auth login` command
   - Add `saz auth logout` command

3. **Configuration Management** (1 day)
   - Store auth tokens securely
   - Handle token expiration

4. **Error Handling** (1 day)
   - Authentication error messages
   - Token refresh failure handling

5. **Testing** (2 days)
   - Unit tests for auth logic
   - Integration tests with Azure DevOps

### Pattern 2: Infrastructure Changes
**PBI**: "Add database support for caching"

**Tasks Created:**
1. **Database Schema** (1 day)
   - Design cache table structure
   - Create migration scripts

2. **Data Access Layer** (2 days)
   - Implement cache read/write operations
   - Add connection pooling

3. **Cache Logic** (2 days)
   - Implement cache invalidation
   - Add cache size limits

4. **Configuration** (1 day)
   - Database connection settings
   - Cache policy configuration

5. **Testing** (2 days)
   - Database integration tests
   - Performance testing

## Quality Gates

### Task Quality Standards
- [ ] **Size**: 1-3 days effort maximum
- [ ] **Independence**: Can be implemented without other tasks
- [ ] **Testability**: Clear acceptance criteria
- [ ] **Value**: Delivers measurable business value
- [ ] **Clarity**: Unambiguous requirements

### Sprint Planning Quality
- [ ] **Capacity**: Total effort ≤ 80% of available capacity
- [ ] **Dependencies**: No circular dependencies
- [ ] **Risks**: High-risk items addressed first
- [ ] **Balance**: Work distributed across team
- [ ] **Commitment**: Team confidence ≥ 7/10

## Error Handling and Recovery

### Common Issues

**Over-sized Tasks:**
- Break into smaller, independent tasks
- Focus on single responsibility principle
- Consider vertical slicing over horizontal

**Unclear Acceptance Criteria:**
- Collaborate with product owner
- Create examples and mockups
- Define negative test cases

**Capacity Over-commitment:**
- Reduce scope or extend timeline
- Re-prioritize based on business value
- Consider carry-over to next sprint

**Technical Dependencies:**
- Spike to investigate unknowns
- Consider parallel development paths
- Plan integration testing early

## Next Steps

After PBI breakdown, proceed to:
1. **Task Implementation** - Follow `workflows/task-implementation.md` for each task
2. **PBI Implementation** - Track multi-task coordination with `workflows/pbi-implementation.md`
3. **PBI Closure** - Validate completed PBI with `workflows/pbi-closure.md`

## Related Workflows

- [Work Item Creation](workitem-creation-workflow.md) - Creating PBIs
- [Work Item Creation](workitem-creation-workflow.md) - Detailed task creation
- [Task Implementation](task-implementation.md) - Individual task execution
- [PBI Implementation](pbi-implementation.md) - Multi-task coordination
- [PBI Closure](pbi-closure.md) - PBI completion validation