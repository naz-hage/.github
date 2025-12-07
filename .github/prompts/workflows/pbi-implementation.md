# PBI Implementation Workflow

This workflow guides the coordination and management of Product Backlog Item (PBI) implementation across multiple Tasks. It focuses on PBI-level planning, progress tracking, and completion validation rather than individual coding work.

## Overview

The PBI implementation workflow manages the delivery of a complete feature or capability through coordinated execution of multiple Tasks. **This workflow focuses on PBI-level coordination** - ensuring all child Tasks are properly implemented, integrated, and tested to meet the PBI's acceptance criteria.

**Key Principle**: One PBI, coordinated delivery. Manage task execution, integration, and validation across the entire PBI scope.

**Note**: This workflow is for PBI-level coordination. For individual Task implementation (coding work), see `workflows/task-implementation.md`.

## Prerequisites

- [ ] PBI in "Committed" state with Related Tasks section populated
- [ ] All child Tasks created and linked to PBI
- [ ] Task breakdown follows ranked implementation order (Task 1, Task 2, etc.)
- [ ] Development team assigned and available
- [ ] Sprint capacity allocated for PBI work

## Input Parameters

```
PBI ID: [Azure DevOps PBI number, e.g., 165]
Related Tasks: [Task IDs in implementation order, e.g., 166, 167, 168, 169]
Sprint: [Target sprint for implementation]
Team: [Assigned development team]
```

## PBI Implementation Workflow

### Phase 1: PBI Preparation and Planning

#### 1.1 Validate PBI Readiness
Ensure PBI is properly prepared for implementation:

```bash
# Query PBI details and validate structure
sdo workitem show --id [PBI_ID]
```

**PBI Readiness Checklist:**
- [ ] PBI state is "Committed"
- [ ] Related Tasks section shows ranked numbering (Task 1, Task 2, etc.)
- [ ] All child Tasks created and properly linked
- [ ] Acceptance criteria are clear and testable
- [ ] Effort estimates are reasonable for sprint capacity

#### 1.2 Review Task Dependencies
Analyze task relationships and implementation order:

**Dependency Analysis:**
- [ ] Task 1 has no dependencies (starts implementation)
- [ ] Subsequent tasks depend on prior task completion
- [ ] No circular dependencies exist
- [ ] Parallel tasks identified where possible
- [ ] Integration points between tasks defined

#### 1.3 Assign Tasks to Team Members
Distribute work based on skills and availability:

```bash
# Update task assignments
az boards work-item update --id [TASK_ID] --fields "System.AssignedTo=[team-member-email]"
```

### Phase 2: Task Execution Management

#### 2.1 Start Implementation with Task 1
Begin with the first ranked task:

**Task 1 Initiation:**
- [ ] Update PBI status to show active work
- [ ] Assign Task 1 to team member
- [ ] Set Task 1 to "In Progress" status
- [ ] Monitor Task 1 progress daily

```bash
# Mark PBI as actively being worked
az boards work-item update --id [PBI_ID] --fields \
  "System.History=PBI implementation started. Beginning with Task 1."
```

#### 2.2 Sequential Task Execution
Manage task completion in ranked order:

**Task Execution Pattern:**
1. **Task N Implementation**: Follow `task-implementation.md` workflow
2. **Task N Validation**: Verify acceptance criteria met
3. **Integration Testing**: Test with previously completed tasks
4. **Task N+1 Initiation**: Start next task when Task N complete

**Progress Tracking:**
- [ ] Daily standup updates on task progress
- [ ] Task status updates in Azure DevOps
- [ ] Blockers identified and resolved promptly
- [ ] Quality gates passed before task completion

#### 2.3 Handle Task Dependencies
Manage dependencies between tasks:

**Dependency Management:**
- [ ] Task completion validated before starting dependent tasks
- [ ] Integration testing performed at task boundaries
- [ ] API contracts verified between tasks
- [ ] Shared components tested thoroughly

### Phase 3: Integration and Testing

#### 3.1 End-to-End Integration
Test complete PBI functionality:

**Integration Testing:**
- [ ] All tasks integrated successfully
- [ ] End-to-end workflows tested
- [ ] Performance requirements validated
- [ ] Security requirements verified
- [ ] User acceptance criteria tested

#### 3.2 PBI Acceptance Validation
Verify all PBI acceptance criteria are met:

**Acceptance Validation:**
- [ ] Each acceptance criterion mapped to completed tasks
- [ ] Functional requirements verified
- [ ] Non-functional requirements tested
- [ ] Documentation updated and accurate
- [ ] No outstanding bugs or issues

### Phase 4: PBI Completion

#### 4.1 Final Validation
Ensure PBI is ready for release:

**Completion Checklist:**
- [ ] All child tasks in "Done" state
- [ ] All acceptance criteria verified
- [ ] Integration testing passed
- [ ] Documentation complete
- [ ] Code reviewed and approved

#### 4.2 Update PBI Status
Mark PBI as completed:

```bash
# Update PBI to "Done" status
az boards work-item update --id [PBI_ID] --fields "System.State=Done"

# Add completion summary
az boards work-item update --id [PBI_ID] --fields \
  "System.History=PBI implementation completed successfully. All acceptance criteria met."
```

#### 4.3 Sprint Retrospective
Review PBI implementation effectiveness:

**Retrospective Topics:**
- [ ] Task breakdown effectiveness
- [ ] Effort estimation accuracy
- [ ] Dependencies managed well
- [ ] Communication and coordination
- [ ] Process improvements identified

## PBI vs Task Implementation

### PBI Implementation Focus
- **Coordination**: Managing multiple tasks and dependencies
- **Integration**: Ensuring tasks work together as complete feature
- **Validation**: Verifying PBI-level acceptance criteria
- **Planning**: Sprint planning and capacity management
- **Stakeholder Management**: Communication with product owners

### Task Implementation Focus
- **Coding**: Individual feature development
- **Unit Testing**: Component-level testing
- **Code Quality**: Following coding standards
- **Documentation**: Code and API documentation
- **Technical Implementation**: Specific technology implementation

## Success Metrics

### Delivery Quality
- [ ] All PBI acceptance criteria met
- [ ] No critical bugs in production
- [ ] Code review feedback addressed
- [ ] Documentation accurate and complete

### Process Effectiveness
- [ ] Tasks completed in ranked order
- [ ] Dependencies managed without delays
- [ ] Daily progress tracking maintained
- [ ] Sprint goals achieved

### Team Performance
- [ ] Clear communication maintained
- [ ] Blockers resolved quickly
- [ ] Knowledge shared effectively
- [ ] Process improvements implemented

## Error Handling and Recovery

### Common PBI Implementation Issues

**Task Dependencies Issues:**
- Identify and resolve circular dependencies
- Adjust task sequence if needed
- Consider parallel development paths

**Integration Problems:**
- Perform early integration testing
- Define clear API contracts between tasks
- Implement continuous integration

**Capacity Over-commitment:**
- Monitor sprint burndown regularly
- Adjust scope or timeline as needed
- Communicate changes to stakeholders

**Quality Gates Failures:**
- Implement additional testing rounds
- Address root causes of failures
- Update acceptance criteria if needed

## Related Workflows

- **Task Implementation**: `workflows/task-implementation.md` (individual task coding)
- **PBI Breakdown**: `workflows/pbi-breakdown.md` (creating task breakdown)
- **Code Review**: `workflows/code-review.md` (PR review process)
- **Testing**: `workflows/testing.md` (comprehensive testing approaches)
- **Work Item Closure**: `workflows/workitem-closure.md` (PBI completion validation)

This workflow ensures PBIs are delivered successfully through coordinated task execution while maintaining quality and meeting stakeholder expectations.