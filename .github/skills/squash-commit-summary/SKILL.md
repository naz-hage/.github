---
name: squash-commit-summary
description: "Summarize commit messages provided by the user into a concise, non-redundant bullet list ready to present in the UI for a squash-and-merge action. Use when the user provides commit messages and asks for a squash summary or prepared merge message."
argument-hint: "Paste the commit messages to summarize"
user-invocable: true
disable-model-invocation: false
---

# Squash Commit Summary

## Purpose

Turn only the commit messages supplied by the user into a concise summary for review before a UI squash-and-merge action.

This skill prepares text only. It does not inspect repositories, retrieve commits, modify files, run commands, call GitHub, or perform merge operations.

## When to Use

Use when the user:

- Pastes one or more commit messages.
- Asks to summarize commits for squash and merge.
- Requests a prepared squash commit message for the UI.
- Wants redundant, temporary, or procedural commit messages removed.

## Input Rules

1. Use only the commit messages in the user's request.
2. Do not run Git commands or use GitHub CLI.
3. Do not inspect the repository, branches, pull requests, diffs, or files.
4. Do not infer implementation details that are not supported by the supplied messages.
5. If no commit messages are supplied, ask the user to paste them.

## Summarization Rules

- Identify the primary outcome across the messages.
- Remove duplicate messages and intermediate wording.
- Combine related implementation, test, and documentation messages.
- Omit temporary work, merge noise, typo fixes, and process-only messages unless they describe a user-visible outcome.
- Preserve meaningful bug fixes, behavior changes, migrations, tests, and documentation updates.
- Use imperative mood: `Add`, `Fix`, `Update`, `Refactor`, `Improve`, or `Remove`.
- Keep the subject concise, ideally 50-72 characters.
- Prefer a short subject followed by a small number of bullets.
- Do not invent issue numbers, component names, rationale, or validation results.

## Output Format

Present the result directly to the user in this format:

```text
Prepared squash summary:

<Imperative subject>

- <Distinct outcome or behavior change>
- <Distinct implementation or migration change>
- <Relevant test or documentation change, if supported>
```

Use only the bullets justified by the supplied messages. Omit empty categories.

## Example

Input:

```text
Fix report browser startup
Use writable WebView2 folder
Add net-worth report HTML test
Fix typo in report log
Update WebView2 setup for retirement report
```

Output:

```text
Prepared squash summary:

Fix WebView2 report rendering in protected environments

- Use writable WebView2 user-data folders for report rendering
- Apply the shared environment to net-worth and retirement reports
- Add coverage for HTML report startup
```

## Final Check

Before presenting the summary, verify:

- Every bullet is supported by the user-provided messages.
- Redundant commits have been consolidated.
- Temporary and process-only messages have been removed.
- No Git, GitHub, repository, or merge action was performed.
