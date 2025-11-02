# Task Closure Workflow

This workflow guides the final phase of task completion, ensuring proper closure of tasks after successful code review and merge. Task closure marks the end of the task lifecycle and updates parent PBI progress.

## Overview

Task closure is the final phase that occurs after a pull request has been reviewed, approved, and merged. This workflow ensures that tasks are properly marked as complete, parent PBIs are updated, and all related work items reflect the current state.

## Prerequisites

- [ ] Pull request merged successfully
- [ ] All CI/CD pipelines passed
- [ ] Code review completed and approved
- [ ] No outstanding issues or blockers
- [ ] Parent PBI identified and accessible

## Input Parameters

```
Task ID: [Azure DevOps Task number, e.g., 166]
PR ID: [Pull request number, e.g., 14]
Parent PBI ID: [Parent PBI number, e.g., 165]
Repository: [Repository name]
Branch: [Merged feature branch, e.g., azdo-166]
```

## Task Closure Workflow

### Phase 1: Verify Completion

#### 1.1 Confirm PR Merge Status
Verify the pull request was successfully merged:

```bash
# Check PR status
az repos pr show --id [PR_ID] --output table

# Verify merge commit exists
git log --oneline --grep="Merge pull request #[PR_ID]" -n 1
```

**Verification Checklist:**
- [ ] PR status shows as "completed" (merged)
- [ ] Merge commit exists in main branch
- [ ] **Squash merge created single consolidated commit** (see `workflows/pr-squash-merge.md`)
- [ ] No merge conflicts occurred
- [ ] CI/CD pipelines completed successfully

#### 1.2 Validate Acceptance Criteria
Ensure all task acceptance criteria were met:

```bash
# Review task details
az boards work-item show --id [TASK_ID] --output table

# Check PR description for completed items
az repos pr show --id [PR_ID] --query "{description:description, title:title}"
```

**Acceptance Criteria Verification:**
- [ ] All functional requirements implemented
- [ ] Code follows project standards
- [ ] Tests pass and coverage meets requirements
- [ ] Documentation updated
- [ ] No breaking changes introduced

### Phase 2: Update Work Items

#### 2.1 Mark Task as Closed
Update the task status to "Done":

```bash
# Close the task
az boards work-item update --id [TASK_ID] --fields "System.State=Done"

# Add closure comment
az boards work-item update --id [TASK_ID] --fields "System.History=Task completed successfully. PR #[PR_ID] merged and all acceptance criteria verified."
```

#### 2.2 Update Parent PBI Progress
Update the parent PBI to reflect task completion:

```bash
# Check current PBI status
az boards work-item show --id [PBI_ID] --output table

# Update PBI with task completion note
az boards work-item update --id [PBI_ID] --fields "System.History=Task #[TASK_ID] completed and merged via PR #[PR_ID]."

# If all tasks complete, consider updating PBI state
# az boards work-item update --id [PBI_ID] --fields "System.State=Done"
```

### Phase 3: Cleanup and Documentation

#### 3.1 Branch Cleanup
Clean up the merged feature branch:

```bash
# Delete local branch
git branch -d azdo-[TASK_ID]

# Delete remote branch
git push azure --delete azdo-[TASK_ID]

# Verify cleanup
git branch -a | grep [TASK_ID]
```

#### 3.2 Update Local Documentation
Ensure any local task files are updated:

```bash
# Mark task file as completed (if applicable)
# Update any local tracking documents
```

#### 3.3 Verify Integration
Ensure the merged changes integrate properly:

```bash
# Pull latest changes
git checkout main
git pull azure main

# Run integration tests
# [Run appropriate integration test commands]
```

### Phase 4: Transition to Next Task

#### 4.1 Assess PBI Status
Determine if the parent PBI is ready for the next task:

```bash
# Check remaining tasks in PBI
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Task' AND [System.Parent] = [PBI_ID]"

# Review PBI acceptance criteria
az boards work-item show --id [PBI_ID] --query "{title:title, state:fields.'System.State'}"
```

#### 4.2 Plan Next Steps
Prepare for the next task in the PBI:

**Next Steps Planning:**
- [ ] Identify next task in PBI breakdown
- [ ] Ensure development environment is ready
- [ ] Review any dependencies or blockers
- [ ] Update sprint board if applicable

## Error Handling

### Common Issues and Solutions

**PR Not Merged:**
- Verify all required reviews are complete
- Check for failing CI/CD pipelines
- Resolve any merge conflicts
- Re-request reviews if needed

**Task Status Issues:**
- Ensure proper permissions to update work items
- Verify task ID is correct
- Check Azure DevOps authentication

**PBI Update Failures:**
- Confirm PBI exists and is accessible
- Verify relationship between task and PBI
- Check for any workflow validation rules

## Success Metrics

**Task Closure Quality:**
- [ ] Task properly marked as "Done"
- [ ] Parent PBI updated with completion details
- [ ] Feature branch cleaned up
- [ ] All acceptance criteria verified
- [ ] No outstanding issues or follow-ups needed

**Process Compliance:**
- [ ] All closure checklist items completed
- [ ] Proper documentation maintained
- [ ] Work item relationships preserved
- [ ] Clean transition to next work

## Related Workflows

- **Task Creation**: `workflows/task-creation.md`
- **Task Implementation**: `workflows/task-implementation.md`
- **Code Review**: `workflows/code-review.md`
- **PBI Implementation**: `workflows/pbi-implementation.md`

This workflow ensures tasks are properly closed and the development process maintains traceability and progress visibility throughout the project lifecycle.