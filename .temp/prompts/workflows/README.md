# Generic Workflow Documentation

Complete guide to Product Backlog Item (PBI) and Task management workflows using the SDO CLI tool. These workflows are designed to work across different project management platforms while leveraging SDO as the primary interface.

## Overview

This documentation provides a comprehensive workflow system for managing development work across different platforms (Azure DevOps, GitHub, Jira), from initial feature planning through to deployment. The workflows are organized into three categories:

- **PBI Workflows**: Feature-level planning and delivery
- **Task Workflows**: Individual work item execution
- **Quality Workflows**: Cross-cutting validation processes

**Primary Tool**: SDO CLI - Unified interface for Azure DevOps, GitHub, and Jira
**Configuration**: See `project-config.yaml` for platform-specific settings

## Quick Start Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│ What do you need to do?                                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ 🆕 New Feature Idea?                                         │
│    └─→ PBI Creation (1)                                      │
│                                                               │
│ 📋 Ready for Sprint Planning?                               │
│    └─→ PBI Breakdown (2)                                     │
│                                                               │
│ 💻 Time to Code?                                             │
│    └─→ Task Implementation (6)                               │
│                                                               │
│ ✅ Finished Coding?                                          │
│    ├─→ Testing (9)                                           │
│    └─→ Code Review (8)                                       │
│                                                               │
│ 🎯 Feature Complete?                                         │
│    └─→ PBI Closure (4)                                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### SDO CLI Tool Setup
```bash
# Install SDO (recommended)
pip install sdo
# or
pip install -e .  # if developing SDO

# Configure for your platform (see project-config.yaml for actual values)
sdo config set azure_devops.organization "[AZURE_DEVOPS_ORG]"
sdo config set azure_devops.pat "$AZURE_DEVOPS_PAT"
```

### Alternative Tools
If SAZ is not available, workflows include alternative commands for:
- **Azure DevOps**: `az boards`, `az repos`, `az pipelines`
- **GitHub**: `gh issue`, `gh pr`, `gh workflow`
- **Jira**: `jira issue`, `jira sprint`

## Quick Navigation

### PBI Workflows (Product Backlog Items)

Feature-level lifecycle management:

1. **[PBI Creation](pbi-creation.md)** - Define new features
   - Business value analysis
   - Acceptance criteria definition
   - Story point estimation

2. **[PBI Breakdown](pbi-breakdown.md)** - Sprint planning
   - Decompose into tasks
   - Capacity planning
   - Task sequencing

3. **[PBI Implementation](pbi-implementation.md)** - Execution coordination
   - Multi-task delivery
   - Integration testing
   - Progress tracking

4. **[PBI Closure](pbi-closure.md)** - Validation and completion
   - Acceptance verification
   - End-to-end testing
   - Product Owner approval

### Task Workflows

Individual work item execution:

5. **[Task Creation](task-creation.md)** - Define implementation tasks

6. **[Task Implementation](task-implementation.md)** - Execute development work

7. **[Task Closure](task-closure.md)** - Validate and complete tasks

### Quality & Collaboration Workflows

Cross-cutting validation processes:

8. **[Code Review](code-review.md)** - PR creation and review
   - Create PR from `.temp/pr.md` (standardized temp location)
   - Use `sdo pr create --file .temp/pr.md --work-item <id>`
   - Work item linking
   - References [PR Squash Merge](actions/pr-squash-merge.md) workflow

9. **[PR Squash Merge](actions/pr-squash-merge.md)** - Squash merge guidance
   - Consolidate multiple commits into meaningful messages
   - Generate squash commit messages
   - Execute merge with GitHub CLI

10. **[Testing](testing.md)** - Quality assurance
   - Unit/integration testing
   - Cross-platform validation
   - Performance/security checks

## Complete Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         PRODUCT BACKLOG ITEM (PBI)                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1️⃣  CREATE PBI          2️⃣  BREAKDOWN         3️⃣  IMPLEMENT           │
│  ┌──────────┐           ┌──────────┐          ┌──────────┐              │
│  │ Business │──────────→│  Sprint  │─────────→│ Execute  │              │
│  │  Value   │           │ Planning │          │  Tasks   │              │
│  └──────────┘           └──────────┘          └──────────┘              │
│      ↓                       ↓                      ↓                     │
│  [New PBI]              [Committed]            [Active]                  │
│                              │                      │                     │
│                              ↓                      ↓                     │
│                     ┌────────────────┐    ┌────────────────┐            │
│                     │ Create Tasks:  │    │ For each task: │            │
│                     │  • Task 1      │    │  5️⃣  Create    │            │
│                     │  • Task 2      │    │  6️⃣  Implement │            │
│                     │  • Task 3      │    │  9️⃣  Test      │            │
│                     │  • ...         │    │  8️⃣  Review    │            │
│                     │  • Task N      │    │  7️⃣  Close     │            │
│                     └────────────────┘    └────────────────┘            │
│                                                   │                       │
│                                                   ↓                       │
│                                           All Tasks Done?                │
│                                                   │                       │
│  4️⃣  CLOSE PBI                                    ↓                       │
│  ┌──────────┐                              Yes → Validate               │
│  │ Validate │←───────────────────────────────────┘                       │
│  │ & Deploy │                                                            │
│  └──────────┘                                                            │
│      ↓                                                                    │
│  [Done]                                                                  │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘

QUALITY GATES (Apply at each stage):
├─ 9️⃣  Testing: Unit → Integration → E2E
└─ 8️⃣  Code Review: PR → Review → Merge
```

## Task Implementation Detail

```
┌──────────────────────────────────────────────────────────────┐
│                    TASK LIFECYCLE                             │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  5️⃣  CREATE → 6️⃣  IMPLEMENT → 9️⃣  TEST → 8️⃣  REVIEW → 7️⃣  CLOSE  │
│                                                                │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌─────┐│
│  │ Define │──→│  Code  │──→│  Test  │──→│   PR   │──→│Done ││
│  │  Task  │   │ Change │   │  Pass  │   │ Merge  │   │     ││
│  └────────┘   └────────┘   └────────┘   └────────┘   └─────┘│
│       ↓            ↓            ↓            ↓                 │
│   [To Do]     [Active]     [Active]     [Review]      [Done] │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

## When to Use Each Workflow

| Situation | Workflow | Purpose |
|-----------|----------|---------|
| 💡 New feature idea | [PBI Creation](pbi-creation.md) | Define business value and requirements |
| 📅 Sprint planning | [PBI Breakdown](pbi-breakdown.md) | Break PBI into tasks |
| ✏️ Need new task | [Task Creation](task-creation.md) | Define specific work item |
| 💻 Ready to code | [Task Implementation](task-implementation.md) | Execute development |
| ✅ Code complete | [Testing](testing.md) → [Code Review](code-review.md) | Validate and review |
| 🎯 Task done | [Task Closure](task-closure.md) | Mark task complete |
| 🚀 Feature complete | [PBI Closure](pbi-closure.md) | Validate entire feature |
| 🔄 Track progress | [PBI Implementation](pbi-implementation.md) | Monitor multi-task delivery |

## Role-Based Quick Reference

### Product Owner
- Create PBIs: [PBI Creation](pbi-creation.md)
- Review completed work: [PBI Closure](pbi-closure.md)
- Approve features: [PBI Closure](pbi-closure.md) Phase 3

### Development Team
- Plan sprints: [PBI Breakdown](pbi-breakdown.md)
- Implement tasks: [Task Implementation](task-implementation.md)
- Validate code: [Testing](testing.md)
- Submit changes: [Code Review](code-review.md)
- Coordinate work: [PBI Implementation](pbi-implementation.md)

### Scrum Master
- Facilitate breakdown: [PBI Breakdown](pbi-breakdown.md)
- Track progress: [PBI Implementation](pbi-implementation.md)
- Remove blockers: All workflows

## Common Patterns

### New Feature Development
1. [PBI Creation](pbi-creation.md) - Product Owner defines feature
2. [PBI Breakdown](pbi-breakdown.md) - Team plans implementation
3. [Task Implementation](task-implementation.md) - Developers build (includes [Testing](testing.md))
4. [Code Review](code-review.md) - Submit PR for review
5. [PBI Closure](pbi-closure.md) - Validate and release

### Bug Fix
1. [PBI Creation](pbi-creation.md) - Define bug and impact
2. [Task Creation](task-creation.md) - Create fix task
3. [Task Implementation](task-implementation.md) - Implement fix (includes [Testing](testing.md))
4. [Code Review](code-review.md) - Submit PR for review
5. [PBI Closure](pbi-closure.md) - Verify fix

### Technical Debt
1. [PBI Creation](pbi-creation.md) - Document debt and impact
2. [PBI Breakdown](pbi-breakdown.md) - Plan refactoring
3. [Task Implementation](task-implementation.md) - Execute improvements (includes [Testing](testing.md))
4. [Code Review](code-review.md) - Submit PR for review
5. [PBI Closure](pbi-closure.md) - Validate improvements

## Best Practices

- **Follow the workflow order** - Each phase builds on the previous
- **Don't skip phases** - Each provides essential validation
- **Use cross-references** - Workflows link to related processes
- **Update regularly** - Keep Azure DevOps status current
- **Validate thoroughly** - Quality gates prevent issues

## Related Documentation

- [Code Review Workflow](code-review.md)
- [Copilot Development Guidelines](../../copilot-instructions.md)
- [SDO Architecture](../../../ARCHITECTURE.md)
- [SDO README](../../../README.md)

---

**Need help?** Each workflow includes detailed prerequisites, checklists, and examples.
