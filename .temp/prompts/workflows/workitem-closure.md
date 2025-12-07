# Work Item Closure Workflow

This workflow guides the final phase of work item completion, ensuring proper closure of tasks, PBIs, and issues after successful implementation, testing, and validation. Work item closure marks the end of the work item lifecycle and updates related items and stakeholders.

## Overview

Work item closure validates that requirements have been fully implemented, tested, and are ready for production use. This involves verifying acceptance criteria are met, conducting appropriate testing, obtaining stakeholder approval, and ensuring proper documentation and knowledge transfer.

## Prerequisites

### For All Work Items
- [ ] Implementation completed and tested
- [ ] Code reviewed and approved (if applicable)
- [ ] Pull requests merged (if applicable)
- [ ] All acceptance criteria verified
- [ ] Documentation updated
- [ ] No outstanding issues or blockers

### For Tasks (Azure DevOps)
- [ ] Pull request merged successfully
- [ ] All CI/CD pipelines passed
- [ ] Parent PBI identified and accessible

### For PBIs (Azure DevOps)
- [ ] All child tasks completed and closed
- [ ] End-to-end testing completed
- [ ] Product Owner approval obtained

### For Issues (GitHub/Azure DevOps)
- [ ] Issue resolution implemented and tested
- [ ] Stakeholder validation completed

## Input Parameters

```
Work Item ID: [Issue/PBI/Task number, e.g., 166, 174, #123]
Work Item Type: [Task|PBI|Issue]
Platform: [github|azdo]
Repository: [Target repository]
Branch: [Main/production branch]
Assignee/Product Owner: [PO name/email for PBIs, assignee for tasks/issues]
Stakeholders: [List of stakeholders to notify]
PR ID: [Pull request number, if applicable]
Parent PBI ID: [For tasks, parent PBI number]
```

## Work Item Closure Validation Workflow

### Phase 1: Pre-Closure Verification

#### 1.1 Work Item Type-Specific Validation

**For Tasks:**
Verify task completion requirements:

```bash
# Check PR status
az repos pr show --id [PR_ID] --output table

# Verify merge commit exists
git log --oneline --grep="Merge pull request #[PR_ID]" -n 1
```

**Task Verification Checklist:**
- [ ] PR status shows as "completed" (merged)
- [ ] Merge commit exists in main branch
- [ ] No merge conflicts occurred
- [ ] CI/CD pipelines completed successfully
- [ ] Task acceptance criteria verified

**For PBIs:**
Verify all child tasks are properly completed:

```bash
# Query all child tasks for this PBI
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo] FROM WorkItems WHERE [System.WorkItemType] = 'Task' AND [System.Parent] = [PBI_ID]" --output table

# Verify each task is in Done state
az boards query --wiql "SELECT COUNT(*) FROM WorkItems WHERE [System.WorkItemType] = 'Task' AND [System.Parent] = [PBI_ID] AND [System.State] <> 'Done'" --output table
```

**PBI Verification Checklist:**
- [ ] All child tasks in "Done" state
- [ ] No tasks remain in "In Progress", "To Do", or "New"
- [ ] Task acceptance criteria verified
- [ ] Task documentation complete
- [ ] No outstanding issues or blockers

**For Issues:**
Verify issue resolution:

```bash
# Check if issue exists and review resolution
gh issue view [ISSUE_NUMBER] --repo [OWNER/REPO]

# Verify linked PRs are merged (if applicable)
gh pr list --state merged --search "closes #[ISSUE_NUMBER]"
```

**Issue Verification Checklist:**
- [ ] Issue description and requirements understood
- [ ] Resolution implemented and tested
- [ ] Acceptance criteria met
- [ ] No remaining questions or concerns

#### 1.2 Acceptance Criteria Validation
Verify all work item-level requirements have been met:

**Functional Requirements:**
- [ ] All requirements implemented and working
- [ ] Business logic correctly implemented
- [ ] User interface meets specifications (if applicable)
- [ ] Integration points working correctly
- [ ] Data validation and error handling complete

**Quality Requirements:**
- [ ] Testing completed (unit/integration/end-to-end as appropriate)
- [ ] Performance requirements met (if specified)
- [ ] Security requirements satisfied (if applicable)
- [ ] Accessibility requirements met (if applicable)

**Non-Functional Requirements:**
- [ ] Scalability requirements met (if applicable)
- [ ] Reliability requirements satisfied
- [ ] Maintainability standards met
- [ ] Documentation complete and accurate

#### 1.3 Code Quality Verification (if applicable)
Ensure code meets quality standards:

```bash
# Run appropriate quality checks based on project
# Examples:
python -m flake8 [package]/ --max-line-length=100
python -m pylint [package]/
dotnet build --configuration Release
npm run lint
```

#### 1.4 Documentation Verification
Confirm all documentation is current and complete:

- [ ] Code comments/docstrings complete and accurate
- [ ] README updated with changes (if applicable)
- [ ] API documentation current (if applicable)
- [ ] User guides reflect changes (if applicable)
- [ ] Architecture diagrams updated (if applicable)

### Phase 2: Testing and Validation

#### 2.1 Testing Completion
Verify appropriate testing has been completed:

**For Tasks:**
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Code review completed

**For PBIs:**
- [ ] End-to-end functionality tested
- [ ] User acceptance testing completed
- [ ] Performance testing completed (if required)
- [ ] Security testing completed (if required)

**For Issues:**
- [ ] Resolution tested in appropriate environment
- [ ] Regression testing completed
- [ ] Stakeholder validation obtained

#### 2.2 Stakeholder Validation
Obtain approval from relevant stakeholders:

**Product Owner Approval (PBIs):**
- [ ] Demo conducted and approved
- [ ] Acceptance criteria validated
- [ ] Business value confirmed

**Assignee Validation (Tasks/Issues):**
- [ ] Implementation reviewed and approved
- [ ] Testing completed successfully
- [ ] No outstanding concerns

### Phase 3: Final Closure Steps

#### 3.1 Update Work Item Status

**For Tasks (Azure DevOps):**
```bash
# Close the task
az boards work-item update --id [TASK_ID] --fields "System.State=Done"

# Add closure comment
az boards work-item update --id [TASK_ID] --fields "System.History=Task completed successfully. PR #[PR_ID] merged and all acceptance criteria verified."

# Update parent PBI progress
az boards work-item update --id [PBI_ID] --fields "System.History=Task #[TASK_ID] completed and merged via PR #[PR_ID]."
```

**For PBIs (Azure DevOps):**
```bash
# Update PBI to Done status with comprehensive closure summary
az boards work-item update --id [PBI_ID] --fields "System.State=Done" "System.History=🎉 PBI COMPLETED: [PBI Title]

✅ ACCEPTANCE CRITERIA VERIFIED:
- All [X] child tasks completed successfully
- End-to-end functionality tested and validated
- User acceptance testing completed with PO approval
- Performance and security requirements met
- Documentation updated and complete

🚀 FEATURE READY FOR PRODUCTION:
- Code merged and deployed
- Integration testing passed
- No outstanding issues or blockers
- Stakeholders notified and approved

📊 COMPLETION SUMMARY:
- Tasks Completed: [X]/[X]
- Test Coverage: [XX]%
- UAT Results: PASSED
- Performance: MET REQUIREMENTS
- Security: PASSED"
```

**For Issues (GitHub):**
```bash
# Close the issue with comment
gh issue close [ISSUE_NUMBER] --repo [OWNER/REPO] --comment "Issue resolved. All acceptance criteria met and implementation validated."
```

**For Issues (Azure DevOps):**
```bash
# Close the issue
az boards work-item update --id [ISSUE_ID] --fields "System.State=Closed" "System.History=Issue resolved. All requirements implemented and validated."
```

#### 3.2 Branch Cleanup (for Tasks)
Clean up the merged feature branch:

```bash
# Delete local branch
git branch -d [feature-branch-name]

# Delete remote branch
git push origin --delete [feature-branch-name]

# Verify cleanup
git branch -a | grep [feature-branch-name]
```

#### 3.3 Update Related Work Items
Ensure parent/child relationships are properly maintained:

**Update Parent PBI (for Tasks):**
- [ ] Progress reflected in PBI
- [ ] Remaining tasks assessed
- [ ] PBI status updated if all tasks complete

**Update Sprint/Iteration Status:**
```bash
# Check sprint progress after work item closure
az boards query --wiql "SELECT [System.State], COUNT(*) FROM WorkItems WHERE [System.IterationPath] = '[ITERATION_PATH]' GROUP BY [System.State]" --output table
```

### Phase 4: Knowledge Transfer and Documentation

#### 4.1 Update Project Documentation
Ensure all project documentation reflects the changes:

- [ ] CHANGELOG.md updated with changes
- [ ] README.md updated (if applicable)
- [ ] Architecture documentation current
- [ ] Troubleshooting guides updated (if applicable)

#### 4.2 Stakeholder Communication
Notify all relevant stakeholders of work item completion:

**Completion Notification Template:**
```
🎉 [WORK_ITEM_TYPE] #[ID] COMPLETED: [Title]

✅ What was delivered:
- [Brief description of work completed]
- [Key functionality implemented]
- [Impact on users/developers]

📋 Completion details:
- Acceptance criteria: MET
- Testing: COMPLETED
- Documentation: UPDATED
- Stakeholders: NOTIFIED

🚀 Status: READY FOR PRODUCTION
```

#### 4.3 Retrospective Documentation (PBIs)
Capture lessons learned for process improvement:

**What Went Well:**
- [ ] Requirements clearly understood
- [ ] Implementation completed successfully
- [ ] Quality standards maintained
- [ ] Collaboration effective

**What Could Improve:**
- [ ] Requirements clarification needed earlier
- [ ] Testing could be more automated
- [ ] Documentation updates required sooner

## Error Handling

### Common Issues and Solutions

**Work Item Status Update Failures:**
- Verify proper permissions to update work items
- Check work item ID is correct
- Confirm Azure DevOps authentication

**PR Merge Verification Issues:**
- Ensure PR exists and is accessible
- Check repository permissions
- Verify merge commit in git history

**Stakeholder Approval Delays:**
- Follow up with stakeholders directly
- Provide additional context or demos
- Escalate through appropriate channels

### Reopening Procedures
If issues discovered after work item closure:

```bash
# Reopen work item with detailed reasoning
az boards work-item update --id [WORK_ITEM_ID] --fields "System.State=[Previous_State]" "System.History=🚨 WORK ITEM REOPENED: [Detailed reason for reopening]"

# Create follow-up tasks/issues for fixes
# Update stakeholders about reopening and remediation plan
```

## Success Metrics

### Quality Metrics
- [ ] Zero critical issues in production (post-implementation)
- [ ] Stakeholder satisfaction maintained
- [ ] Requirements fully implemented
- [ ] Documentation accuracy maintained

### Process Metrics
- [ ] Work item closure time appropriate to complexity
- [ ] Stakeholder approval obtained timely
- [ ] Reopen rate minimized
- [ ] Process compliance maintained

## Related Workflows

- **Work Item Creation**: `workflows/workitem-creation-workflow.md`
- **Task Implementation**: `workflows/task-implementation.md`
- **PBI Implementation**: `workflows/pbi-implementation.md`
- **Code Review**: `workflows/code-review.md`
- **PR Management**: `workflows/pr-squash-merge.md`

This workflow ensures thorough validation and proper closure of all work item types, maintaining project quality and delivering value while enabling continuous improvement of development processes.