# Update PR Message Template Workflow

Update pull request template with current branch changes.

## Prerequisites
- `.temp/<issue-number>-pr-message.md` exists (created by `sdo wi start`)
- On feature branch created by `sdo wi start`
- Changes exist on branch

## Workflow

1. **Verify template exists**: `.temp/<issue-number>-pr-message.md`
2. **Analyze changes**: `git diff origin/main --name-only`, `git diff origin/main --stat`
3. **Update template** (Preserve template structure):
   - **Title**: `###: ` + descriptive text of changes
   - **Description**: Explain what changed and why
   - **Changes**: Preserve section name. As bulleted items, list changes and note key files modified
   - **Why**: Preserve section name. As bulleted items, explain why the changes were made
4. **Commit**: `git add .` and `git commit -m "Implementation: [description]"`
5. **Verify**: All sections filled, markdown valid, ready for `sdo pr create`

## Checklist

- [ ] Template file exists at `.temp/<issue-number>-pr-message.md`
- [ ] On correct feature branch
- [ ] Title updated with actual changes (keep issue prefix)
- [ ] All modified files documented
- [ ] Markdown syntax valid

## Next Steps

Execute: `sdo pr create -f .temp/<issue-number>-pr-message.md`

## Example

```powershell
# Verify template exists
Get-ChildItem ".temp/*-pr-message.md"

# Review changes
git diff origin/main --name-only
git diff origin/main --stat

# Update template with actual changes and commit
git add .
git commit -m "Feat: Implementation description"

# Ready for PR creation
sdo pr create -f .temp/123-pr-message.md
```

## Notes
- Always update title (keep issue prefix `###`)
- Fill all template sections with actual changes
- Template file must exist before updating
- Branch must match issue number
