# Start Work Item Action

You are tasked with starting work on a new work item (Issue, PBI, or Task) using an automated workflow.

## Prerequisites

Before starting work, ensure:

### For All Work Items
- [ ] Work item exists and is assigned to you
- [ ] Acceptance criteria are clear and understood
- [ ] No blocking dependencies exist
- [ ] Required tools and environment are set up

### For Issues (GitHub)
- [ ] Issue is properly labeled and prioritized
- [ ] Related requirements are documented
- [ ] No duplicate issues exist

### For PBIs/Tasks (Azure DevOps)
- [ ] Parent work items are active
- [ ] Sprint/iteration is assigned
- [ ] Effort estimates are provided

## Verification Commands

**Check work item details:**
```bash
# For GitHub issues
sdo workitem show --id [ISSUE_NUMBER]

# For Azure DevOps work items
sdo workitem show --id [WORK_ITEM_ID]
```

**Check repository status:**
```bash
git status
git branch -a
```

## Work Item Types

### Issues (GitHub or Azure DevOps)
Create feature branch and start implementation following project standards.

### PBIs (Azure DevOps)
**PBI Preparation and Planning:**
- [ ] Validate PBI readiness and task breakdown
- [ ] Review task dependencies and implementation order
- [ ] Assign tasks to team members
- [ ] Start with Task 1 implementation

**PBI Readiness Checklist:**
- [ ] PBI state is "Committed"
- [ ] Related Tasks section shows ranked numbering
- [ ] All child Tasks created and properly linked
- [ ] Acceptance criteria are clear and testable

### Tasks (Azure DevOps)
**Task Preparation:**
- [ ] Read task requirements from Azure DevOps
- [ ] Review parent PBI context and acceptance criteria
- [ ] Analyze integration points and dependencies
- [ ] Plan implementation approach

**Implementation Focus:**
- [ ] One task, one focus - complete fully before next task
- [ ] Follow established code patterns in the codebase
- [ ] Implement with tests (TDD approach)
- [ ] Update documentation as you develop

## Branch Creation

**Create and switch to feature branch:**
```bash
# Create feature branch
git checkout -b [branch-name]

# Push to remote
git push -u origin [branch-name]
```

**Branch naming convention:**
- HitHub Issues: `[number]-issue`
- Azdo Tasks: `[number]-[task]`

## Initial Setup

**Update work item status:**
```bash
# Mark as In Progress
sdo workitem update --id [WORK_ITEM_ID] --state "In Progress"
```

**Create initial documentation:**
```bash
# Create work item documentation in .temp/
# File: .temp/start-[workitem-type]-[id].md
```

## Implementation Workflow

### Phase 1: Analysis and Design
**For All Work Items:**
- [ ] Review requirements and acceptance criteria
- [ ] Analyze integration points and dependencies
- [ ] Review existing code patterns
- [ ] Plan implementation approach

**For PBIs (Additional):**
- [ ] Validate task breakdown and dependencies
- [ ] Review sprint capacity and timeline
- [ ] Coordinate with team members

### Phase 2: Development Setup
**Environment Setup:**
```bash
# Set up development environment
pip install -r requirements.txt
pip install -e .
python -c "import [package]; print('Environment ready')"
```

**Code Quality Tools:**
```bash
# Run quality checks
make lint        # Code quality checks
make format      # Format code with Black and isort
```

### Phase 3: Implementation Approach
**Follow Code Patterns:**
- Reference established patterns in codebase
- Use type hints, docstrings, and proper error handling
- Implement features with comprehensive tests
- Update documentation as you develop

**TDD Approach:**
- Write tests first, then implement functionality
- Run tests frequently during development
- Ensure all acceptance criteria are covered by tests

### Phase 4: Progress Tracking
**Daily Updates:**
- Update work item status regularly
- Document progress and any blockers
- Communicate with stakeholders
- Ensure alignment with acceptance criteria

## Examples

### Start Issue Work
```bash
# Check issue details
sdo workitem show --id 123

# Create feature branch
git checkout -b issue-123-networth-command
git push -u origin issue-123-networth-command

# Update status
sdo workitem update --id 123 --state "In Progress"
```

### Start PBI Work
```bash
# Check PBI details
sdo workitem show --id 456

# Create feature branch
git checkout -b pbi-456-reports-enhancement
git push -u origin pbi-456-reports-enhancement

# Update status
sdo workitem update --id 456 --state "In Progress"
```

## Post-Start Workflow
- **Code**: Begin implementation following established patterns
- **Testing**: Write tests as you develop (TDD approach)
- **Documentation**: Update docs as features are implemented
- **Communication**: Keep stakeholders informed of progress
- **Quality**: Run linting and formatting regularly
- **Integration**: Test with existing functionality frequently

### For PBIs - Task Coordination
- **Sequential Execution**: Complete tasks in ranked order (Task 1, then Task 2, etc.)
- **Dependency Management**: Ensure task dependencies are met before starting dependent tasks
- **Integration Testing**: Test task integration at boundaries
- **Progress Tracking**: Update PBI status as tasks complete

### For Tasks - Implementation Focus
- **Complete Focus**: Finish one task fully before starting another
- **Code Review Ready**: Ensure code is review-ready throughout development
- **Acceptance Criteria**: Verify all criteria are met before completion
- **Documentation**: Update all relevant docs and comments

## Error Handling

### Common Issues:
1. **Branch already exists**: Use unique branch name
2. **Permission denied**: Check repository access
3. **Work item not found**: Verify work item ID
4. **Status transition blocked**: Check work item workflow

### Recovery Steps:
- If branch exists: Add timestamp or unique identifier
- If permission denied: Request access from repository admin
- If work item not found: Check work item platform and ID
- If status blocked: Verify work item state and permissions

## Notes
- Always create feature branches for work items
- Keep branches focused on single work items
- Update work item status promptly
- Follow project's coding and testing standards

---

## Summary
This action provides a streamlined workflow for starting work on work items across GitHub Issues and Azure DevOps work items using the unified SDO tool.

**Key Benefits:**
- **Standardized Process**: Consistent start workflow across platforms
- **Branch Management**: Proper feature branch creation and tracking
- **Status Tracking**: Clear work item state management
- **Documentation**: Initial setup and tracking

**Workflow Steps:**
1. Verify work item details and prerequisites
2. Create appropriately named feature branch
3. Update work item status to "In Progress"
4. Begin implementation work

Use this action consistently across all work item starts to maintain quality standards and proper tracking.</content>
<parameter name="filePath">c:\source\.github\.github\prompts\actions\start-workitem.md