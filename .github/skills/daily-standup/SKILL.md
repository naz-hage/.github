---
name: daily-standup
description: "Write a concise daily stand-up summary from workspace activity and agent conversation. Use when the user asks for a daily stand up, daily standup, yesterday/today summary, blockers, or parking lot notes."
argument-hint: "Provide the destination folder for daily-<date>.md"
---

# Daily Stand-up

Create a short Markdown stand-up document from the current workspace repository activity and the related agent conversation.

## Required Input

- Use the folder path provided by the user as the output directory.
- If no destination folder is provided, ask for it before creating a file.
- Do not write outside the requested folder.

## Time Window

Use the user's local date and time:

- Start: yesterday at 10:30 AM
- End: today at 10:00 AM

Use an inclusive start and an exclusive end. Resolve "yesterday" and "today" from the current date at execution time, not from the file name.

## Workflow

1. Identify the workspace repository and destination folder from the request.
2. Search repository activity within the time window:
   - Git commits, changed files, and relevant branch activity.
   - Current worktree changes when they help explain active work.
3. Search the session history for agent conversations associated with the workspace repository and limited to the same time window.
   - Use the session history query tool rather than guessing from unrelated conversations.
   - Prefer exact workspace/repository matches and the relevant user/agent turns.
4. Combine the evidence into a concise summary. Omit implementation details, file lists, commit hashes, and long explanations.
5. Write the result to:

   `daily-<date>.md`

   where `<date>` is today's local date in `YYYY-MM-DD` format.
6. Preserve any existing file unless the user explicitly asks to replace it. If the target already exists, ask whether to overwrite it.
7. Confirm the created path and report only a brief summary of the output.

## Output Format

Use exactly these headings:

```markdown
# Daily Stand-up - YYYY-MM-DD

## What did I do yesterday?
- Concise summary

## What will I be doing today?
- Concise summary

## Are there blockers?
- None identified

## What should I bring to the parking lot?
- None identified
```

## Example

Example request:

```text
Write my daily stand-up using workspace activity and agent conversation. Save it in C:\work\standups.
```

Example output file, `C:\work\standups\daily-2026-10-13.md`:

```markdown
# Daily Stand-up - 2026-10-13

## What did I do yesterday?
- Completed the planned workspace updates and reviewed related agent work.

## What will I be doing today?
- Continue the current implementation and validate the remaining changes.

## Are there blockers?
- None identified

## What should I bring to the parking lot?
- Follow-up discussion on work planned for the next iteration.
```

## Writing Rules

- Keep the summary high-level and brief; do not include implementation details.
- Use plain language and short bullets.
- Group related work instead of listing every activity.
- Distinguish completed work from planned work.
- Report blockers only when supported by the activity or conversation evidence.
- Put unresolved ideas, follow-up discussions, or deferred decisions in the parking lot section.
- Use `None identified` when there is no reliable evidence for blockers or parking-lot items.
- Correct obvious wording errors in the headings while preserving the requested meaning.
