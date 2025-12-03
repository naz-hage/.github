# Daily Standup Reference Guide

This guide provides a standardized format for daily standup meetings that works across different development teams and project types. The format is designed to be concise, actionable, and focused on progress and impediments.

## Overview

Daily standups are brief, focused meetings where team members share:
- What they accomplished since the last standup
- What they plan to work on next
- Any blockers or impediments they're facing

## Standard Standup Format

### Three Key Questions

**1. What did you accomplish yesterday?**
- Focus on completed work and deliverables
- Be specific about what was delivered
- Include relevant technical details
- Mention any challenges overcome

**2. What will you work on today?**
- Outline planned tasks and goals
- Be specific about deliverables
- Consider dependencies and priorities
- Keep commitments realistic

**3. Are there any blockers or impediments?**
- Identify issues preventing progress
- Be specific about what's blocking you
- Ask for help when needed
- Note if you need input from others

## Standup Templates

### Basic Template

```markdown
## Daily Standup - [Date]

**Yesterday:**
- [Completed task 1]
- [Completed task 2]
- [Completed task 3]

**Today:**
- [Planned task 1]
- [Planned task 2]
- [Planned task 3]

**Blockers:**
- [Blocker 1 or "No blockers"]
```

### Detailed Template

```markdown
## Daily Standup - [Date] - [Your Name]

**Yesterday:**
- Completed [feature/task]: [brief description of what was delivered]
- Fixed [issue/bug]: [what was broken and how it was resolved]
- Reviewed/merged [PR/issue]: [what was accomplished]
- [Other accomplishments]

**Today:**
- Will work on [feature/task]: [specific goal for today]
- Plan to [action]: [what will be delivered]
- Need to [coordinate]: [dependencies on others]
- [Other planned work]

**Blockers/Questions:**
- Blocked by [issue]: [specific description of what's preventing progress]
- Need clarification on [requirement/decision]: [specific question]
- Waiting for [resource/access]: [what's needed]
- No blockers
```

## Language-Specific Examples

### Python Development Team

```markdown
## Daily Standup - October 20, 2025

**Yesterday:**
- Implemented user authentication module with JWT token validation
- Added comprehensive unit tests for authentication service (85% coverage)
- Fixed database connection pooling issue in production environment
- Completed API documentation for authentication endpoints

**Today:**
- Implement password reset functionality with email notifications
- Add integration tests for authentication workflow
- Review security implications of new authentication approach
- Update deployment scripts for new authentication service

**Blockers:**
- Need access to email service API for password reset testing
- Awaiting security team review of authentication implementation
```

### JavaScript/TypeScript Development Team

```markdown
## Daily Standup - October 20, 2025

**Yesterday:**
- Built React dashboard component with real-time data visualization
- Implemented TypeScript interfaces for API data models
- Fixed memory leak in chart rendering component
- Added unit tests for dashboard state management

**Today:**
- Integrate dashboard with REST API for live data updates
- Add error boundaries and loading states to dashboard
- Implement responsive design for mobile devices
- Write integration tests for dashboard API calls

**Blockers:**
- API endpoints not yet available from backend team
- Need design approval for mobile layout changes
```

### Java Development Team

```markdown
## Daily Standup - October 20, 2025

**Yesterday:**
- Implemented Spring Boot microservice for order processing
- Added JPA entities and repositories for order management
- Configured Hibernate mappings and database migrations
- Created REST controllers with proper error handling

**Today:**
- Implement order validation business logic
- Add integration with payment service
- Write unit and integration tests for order processing
- Set up CI/CD pipeline for microservice deployment

**Blockers:**
- Waiting for payment service API documentation
- Need database access for integration testing
```

### C#/.NET Development Team

```markdown
## Daily Standup - October 20, 2025

**Yesterday:**
- Built ASP.NET Core Web API for customer management
- Implemented Entity Framework Core data models
- Added input validation and error handling middleware
- Created Swagger documentation for API endpoints

**Today:**
- Implement authentication and authorization
- Add logging and monitoring capabilities
- Write comprehensive test suite (unit + integration)
- Prepare deployment package for staging environment

**Blockers:**
- Need clarification on authentication requirements
- Awaiting security team approval for authentication approach
```

### Go Development Team

```markdown
## Daily Standup - October 20, 2025

**Yesterday:**
- Implemented HTTP server with REST API endpoints
- Added database layer with PostgreSQL integration
- Created middleware for logging and error handling
- Wrote unit tests for core business logic

**Today:**
- Implement authentication with JWT tokens
- Add request validation and sanitization
- Create integration tests for API endpoints
- Optimize database queries for performance

**Blockers:**
- Need access to test database environment
- Waiting for security review of authentication implementation
```

## Best Practices

### Content Guidelines

**Be Specific and Action-Oriented:**
- ✅ "Implemented user login API with password hashing"
- ❌ "Worked on authentication"

**Focus on Outcomes:**
- ✅ "Fixed memory leak that was causing 500 errors"
- ❌ "Debugged some issues"

**Include Context:**
- ✅ "Updated Docker configuration for production deployment"
- ❌ "Did DevOps stuff"

**Be Honest About Blockers:**
- ✅ "Blocked by missing API documentation from team X"
- ❌ "Having some issues" (too vague)

### Time Management

**Keep It Brief:**
- Individual updates: 30-60 seconds
- Full team standup: 15 minutes maximum
- Prepare your update in advance

**Stick to the Format:**
- Answer the three questions directly
- Avoid side conversations during standup
- Save detailed discussions for after the meeting

### Remote Team Considerations

**For Distributed Teams:**
- Use video when possible for better communication
- Share screens when showing work or blockers
- Use collaborative tools for shared context
- Record standups for absent team members

**Asynchronous Standups:**
- Use shared documents or tools for written updates
- Schedule virtual standups at overlapping hours
- Include screenshots or links when relevant

## Common Standup Patterns

### Sprint Planning Context

```markdown
**Yesterday:**
- Completed feature: "As a user, I can filter search results"
- Fixed 3 bugs from previous sprint
- Updated component documentation

**Today:**
- Start work on feature: "As a user, I can export search results"
- Review pull requests from yesterday
- Attend architecture planning meeting

**Blockers:**
- Need design mockups for export feature
```

### Bug-Fixing Focused

```markdown
**Yesterday:**
- Fixed critical authentication bug affecting 15% of users
- Implemented temporary workaround for payment processing
- Added monitoring alerts for similar issues

**Today:**
- Investigate root cause of authentication bug
- Implement permanent fix for payment processing
- Add regression tests for both fixes

**Blockers:**
- Need access to production logs for root cause analysis
```

### Research/Spike Work

```markdown
**Yesterday:**
- Researched 3 options for caching layer implementation
- Created proof-of-concept for Redis caching solution
- Documented findings and recommendations

**Today:**
- Implement chosen caching solution
- Integrate with existing codebase
- Performance test the implementation

**Blockers:**
- Need infrastructure team approval for Redis deployment
```

### Maintenance/Release Focused

```markdown
**Yesterday:**
- Updated dependencies and resolved security vulnerabilities
- Performed database maintenance and cleanup
- Prepared release notes for version 2.1.0

**Today:**
- Deploy version 2.1.0 to staging environment
- Monitor deployment and performance metrics
- Begin planning for version 2.2.0 features

**Blockers:**
- Awaiting security team approval for production deployment
```

## Tools and Integration

### Standup Tracking Tools

**Digital Tools:**
- Azure DevOps Boards (for work item tracking)
- Jira (for issue and progress tracking)
- Slack/Teams channels for quick updates
- Shared Google Docs/OneNote for written standups

**Integration with Work Tracking:**
- Reference ticket/story numbers in updates
- Update work item status during standup
- Link commits and pull requests to work items

### Automated Standup Generation

**From Git History:**
```bash
# Generate standup from recent commits
git log --since="yesterday" --oneline --author="Your Name"
```

**From IDE History:**
- Review files changed since last standup
- Check TODO comments and work-in-progress
- Review test results and code quality metrics

## Standup Facilitation

### Scrum Master/Facilitator Role

**Meeting Management:**
- Keep time and ensure everyone participates
- Note action items and follow-ups
- Identify cross-team dependencies
- Ensure remote participants can contribute

**Common Issues to Watch For:**
- Team members talking too long
- Side conversations derailing the meeting
- Lack of preparation leading to vague updates
- Blockers not being addressed promptly

### Follow-up Actions

**After Standup:**
- Create work items for blockers that need attention
- Schedule meetings to address impediments
- Update project boards with new information
- Send summary to absent team members

## Metrics and Improvement

### Standup Effectiveness Metrics

**Track These Indicators:**
- Average standup duration
- Number of blockers identified and resolved
- Team satisfaction with standup format
- Action items completion rate

**Continuous Improvement:**
- Regular retrospectives on standup effectiveness
- Adjust format based on team feedback
- Experiment with different tools and approaches
- Ensure standups remain valuable and not just routine

## Conclusion

Effective daily standups are:
- **Concise**: 15 minutes or less for the whole team
- **Focused**: Three questions, specific answers
- **Actionable**: Clear next steps and identified blockers
- **Inclusive**: Everyone participates, remote-friendly
- **Valuable**: Drives team coordination and removes impediments

The format should be adapted to your team's needs while maintaining the core structure of sharing progress, plans, and impediments.
- Pay attention to questions asked or decisions that need validation
- Consider the broader context of the project (CI/CD, quality gates, DevOps workflows)
- Infer logical next steps from the current state of work

---

**Usage:** Invoke this prompt at the end of your work session or at the start of standup to generate your update automatically.

## Saving Your Daily Standup

After generating your standup summary, save it to the daily standup folder with the following structure:

### Folder Structure

```
C:\source\workspace\daily-standup\
├── 2025\
│   ├── 01-january\
│   │   ├── 2025-01-15-monday.md
│   │   ├── 2025-01-16-tuesday.md
│   │   └── ...
│   ├── 02-february\
│   ├── 03-march\
│   ├── ...
│   ├── 10-october\
│   │   ├── 2025-10-20-monday.md    ← Today's standup
│   │   ├── 2025-10-21-tuesday.md
│   │   └── ...
│   └── 12-december\
├── README.md
└── archive\
    └── 2024\
```

### File Naming Convention

**Format:** `YYYY-MM-DD-dayofweek.md`

**Examples:**
- `2025-10-20-sunday.md`
- `2025-10-21-monday.md`
- `2025-12-25-wednesday.md`

### Steps to Save

1. **Verify the current date** (important for correct file naming):
   ```powershell
   Get-Date | Select-Object -Property Date, DayOfWeek
   # Verify this matches today's actual date before proceeding
   ```

2. **Create the folder structure** (if it doesn't exist):
   ```powershell
   $date = Get-Date
   $year = $date.ToString("yyyy")
   $month = $date.ToString("MM") + "-" + $date.ToString("MMMM").ToLower()
   $standupPath = "C:\source\workspace\daily-standup\$year\$month"
   New-Item -Path $standupPath -ItemType Directory -Force
   ```

3. **Generate the filename** (automatically includes correct day of week):
   ```powershell
   $fileName = $date.ToString("yyyy-MM-dd-dddd").ToLower() + ".md"
   $filePath = Join-Path $standupPath $fileName
   # This will automatically generate the correct day (e.g., "2025-10-25-saturday.md")
   ```

3. **Save the standup content**:
   ```powershell
   $standupContent | Out-File -FilePath $filePath -Encoding UTF8
   Write-Host "✅ Daily standup saved to: $filePath"
   ```

4. **Optional: Open the file**:
   ```powershell
   code $filePath
   ```

### Quick Save Script

Use this PowerShell one-liner to save your standup:

```powershell
# First verify today's date
Get-Date | Select-Object -Property Date, DayOfWeek

# After generating standup, save it with one command
$d = Get-Date; $p = "C:\source\workspace\daily-standup\$($d.ToString('yyyy'))\$($d.ToString('MM') + '-' + $d.ToString('MMMM').ToLower())"; New-Item -Path $p -ItemType Directory -Force | Out-Null; $f = Join-Path $p "$($d.ToString('yyyy-MM-dd-dddd').ToLower()).md"; @"
## Daily Standup - $($d.ToString('MMMM dd, yyyy'))

**Yesterday:**
- [Paste your generated content here]

**Today:**
- [Paste your generated content here]

**Blockers/Questions:**
- [Paste your generated content here]
"@ | Out-File -FilePath $f -Encoding UTF8; Write-Host "✅ Saved: $f"; code $f
```

### Automated Save Helper Script

Create `Save-DailyStandup.ps1` in your workspace:

```powershell
param(
    [string]$StandupText
)

# Verify current date before proceeding
Write-Host "Current Date: $(Get-Date | Select-Object -ExpandProperty Date)" -ForegroundColor Yellow
Write-Host "Day of Week: $(Get-Date | Select-Object -ExpandProperty DayOfWeek)" -ForegroundColor Yellow
Read-Host "Press Enter to confirm date is correct, or Ctrl+C to cancel"

$date = Get-Date
$year = $date.ToString("yyyy")
$month = $date.ToString("MM") + "-" + $date.ToString("MMMM").ToLower()
$dayOfWeek = $date.ToString("dddd").ToLower()
$dateStr = $date.ToString("yyyy-MM-dd")

# Create folder structure
$standupPath = "C:\source\workspace\daily-standup\$year\$month"
New-Item -Path $standupPath -ItemType Directory -Force | Out-Null

# Generate filename
$fileName = "$dateStr-$dayOfWeek.md"
$filePath = Join-Path $standupPath $fileName

# Save content
if ($StandupText) {
    $StandupText | Out-File -FilePath $filePath -Encoding UTF8
} else {
    # Create template if no content provided
    @"
## Daily Standup - $($date.ToString('MMMM dd, yyyy'))

**Yesterday:**
- 

**Today:**
- 

**Blockers/Questions:**
- No blockers
"@ | Out-File -FilePath $filePath -Encoding UTF8
}

Write-Host "✅ Daily standup saved to: $filePath" -ForegroundColor Green
code $filePath
```

**Usage:**
```powershell
# IMPORTANT: Always verify the date first!
Get-Date | Select-Object -Property Date, DayOfWeek

# Option 1: Create template and fill in manually
.\Save-DailyStandup.ps1

# Option 2: Pipe generated content
$standupContent | .\Save-DailyStandup.ps1

# Option 3: Pass as parameter
.\Save-DailyStandup.ps1 -StandupText $generatedStandup
```

### Benefits of This Structure

✅ **Chronological Organization**: Easy to find standups by date
✅ **Archive Old Years**: Keep workspace clean by archiving past years
✅ **Searchable**: Use `grep` or `Select-String` to find past work
✅ **Backup Friendly**: Structured folders work well with Git/backups
✅ **Calendar Integration**: Date-based naming matches calendar views
✅ **Week Planning**: See all standups for a month at a glance

### Optional: Create README.md

Add a `README.md` in the daily-standup folder:

```markdown
# Daily Standup Notes

This folder contains daily standup summaries organized by year and month.

## Structure
- Each year has its own folder (2025, 2026, etc.)
- Within each year, months are organized as `MM-MonthName`
- Files are named `YYYY-MM-DD-dayofweek.md`

## Quick Search
```powershell
# Find all standups mentioning "Azure DevOps"
Get-ChildItem -Path . -Recurse -Filter "*.md" | Select-String -Pattern "Azure DevOps"

# List all standups from October 2025
Get-ChildItem -Path "2025/10-october" -Filter "*.md" | Sort-Object Name
```

## Archive Policy
- Current year: Keep in main folder
- Previous years: Move to `archive/` folder annually
```

