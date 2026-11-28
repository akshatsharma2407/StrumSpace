---
name: create-branch
description: Safely create a new Git task branch from the repository's synchronized primary branch. Use when the user asks to create a branch from main/master or when a new implementation task requires one. Do not use for branching from another feature branch.
argument-hint: "[branch-name]"
disable-model-invocation: false
user-invocable: true
---

# Create a Task Branch

## Purpose and scope

Create and check out one new branch from the repository's primary branch, only after verifying that the primary branch matches its remote and obtaining the project owner's explicit approval.

This skill may be invoked by the user as `/create-branch [branch-name]` or by Claude when the current task requires a new branch from the primary branch. Do not use it to branch from a feature branch. Do not implement the task, commit its changes, merge the new branch, or publish the new branch as part of this workflow.

## Optional argument

Requested branch name: `$ARGUMENTS`

- If a non-empty branch name was explicitly provided, use that exact name as the candidate. Do not generate or silently modify it.
- If no name was provided, read `CLAUDE.md` and the active phase document it references. Identify the current task and propose a concise name, such as `feat/enquiry-schemas`, `fix/database-session`, `test/enquiry-module`, `refactor/configuration`, or `docs/enquiry-module`.
- If the current task or supplied name is unclear, ask the user. Do not guess.
- Treat the argument as data, not a shell command. Require exactly one valid branch name. Reject option-like names and unsafe shell interpolation; quote or pass the validated name as a literal argument to Git.
- Obtain explicit approval for the final branch creation, including its exact name, even if a name was supplied. Do not propose a different name unless the supplied name is invalid or unavailable and the user agrees to change it.

## Non-negotiable safety rules

- Follow `CLAUDE.md` and existing repository instructions.
- Never automatically stash, commit, discard, reset, rebase, merge divergent history, force-push, delete branches, or overwrite existing branches.
- Never pull or push without explicit approval for that specific operation.
- Never create a branch until the primary branch is clean, fully synchronized, and the final branch name is approved.
- A user request to create a branch is not permission to pull, push, or repair Git history.
- If a check fails, a command fails, or approval is denied, stop and explain the issue. Do not bypass the check or silently choose another approach.
- Inspect actual Git output and exit status; do not infer success merely because a command was issued.
- Do not disable or bypass Claude Code's normal tool permissions.

## Workflow

### 1. Identify repository, current branch, and primary branch

Run from the project repository:

```bash
git rev-parse --show-toplevel
git branch --show-current
git remote -v
git status --porcelain=v1 --untracked-files=all
git status
```

- Stop if this is not a Git working tree, the current HEAD is detached, or a merge, rebase, cherry-pick, revert, bisect, or other unfinished Git operation is in progress.
- Stop if there are staged, unstaged, or untracked changes. Show a short summary and ask the user to resolve them. Do not switch branches with pending changes.
- Use `origin` if it is the repository's confirmed intended remote. If the intended remote is missing or ambiguous, ask the user.
- Identify the primary branch using the remote's advertised default branch and relevant project instructions. For example:

```bash
git ls-remote --symref origin HEAD
```

- Do not assume the branch is named `main` or `master`. If the default cannot be established, conflicts with project instructions, or is missing locally, stop and ask the user.

### 2. Fetch and check the current branch before switching

```bash
git fetch origin
```

Fetching updates remote-tracking information without merging into local branches or changing tracked working files. It is part of the requested workflow; it does not imply permission to pull or push.

If currently on a non-primary branch:

- Determine its upstream using `git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'`.
- Confirm that the upstream belongs to the intended remote and has been refreshed; if not, stop for clarification.
- Compare the current branch with its upstream using:

```bash
git rev-list --left-right --count 'HEAD...@{upstream}'
```

- The first count is local-only commits (ahead); the second is upstream-only commits (behind).
- If the branch contains unpushed commits, has diverged, or lacks a verifiable upstream, stop and ask the user to resolve or explicitly clarify its synchronization status before leaving it. Do not publish a feature branch automatically.
- A non-primary branch that is only behind its verified upstream can be left without pulling it. Do not modify unrelated branches.

### 3. Switch to the primary branch

If not already on the confirmed primary branch:

```bash
git switch <primary-branch>
```

The angle-bracket notation in command examples denotes a placeholder; substitute the actual validated value, not the placeholder itself.

Verify the current branch and clean working tree again. Confirm the primary branch tracks the expected remote branch (for example, `origin/master`). Stop if the upstream is missing or points elsewhere.

### 4. Compare the primary branch with its remote

Fetch again if necessary to ensure the comparison is current. Confirm that the primary branch still exists on the intended remote, rather than relying on a potentially stale tracking ref.

```bash
git rev-list --left-right --count 'HEAD...@{upstream}'
```

Handle the results:

| Local ahead | Remote ahead | Action |
|---|---|---|
| 0 | 0 | Synchronized; proceed. |
| >0 | 0 | Stop. Report the number of unpushed commits and ask whether to push the primary branch. |
| 0 | >0 | Stop. Report the number of incoming commits and ask whether to pull. |
| >0 | >0 | Stop. Explain the divergence and ask the user to resolve it manually. |

If the user explicitly approves pushing, use a normal non-force push to the confirmed remote primary branch, for example:

```bash
git push origin <primary-branch>:<primary-branch>
```

If the user explicitly approves pulling, use a fast-forward-only pull from the confirmed remote primary branch:

```bash
git pull --ff-only origin <primary-branch>
```

After an approved synchronization operation, fetch again, verify that the working tree remains clean, and repeat the comparison. Continue only when both counts are zero. If synchronization is refused or unsuccessful, stop without creating a branch.

### 5. Resolve and validate the new branch name

Use the explicitly supplied name, or propose one based on the active phase and task as described above.

Validate the candidate with Git:

```bash
git check-ref-format --branch <branch-name>
```

Require that the validated output is exactly the candidate; do not accept names that Git expands (for example, `@{-1}`).

Check for existing local and remote branches, including conflicting ref prefixes where relevant. Use exact ref names, for example:

```bash
git show-ref --verify refs/heads/<branch-name>
git ls-remote --exit-code --heads origin refs/heads/<branch-name>
```

For the local check, distinguish a missing ref from a command error. For `git ls-remote --exit-code`, exit code 2 means no matching ref; other failures must not be interpreted as availability. Inspect branch names for prefix conflicts when needed.

If the branch already exists locally or remotely, or conflicts with an existing ref, stop and ask for a different name or let the user decide how to handle the existing branch outside this skill. Never reuse, overwrite, or delete it automatically.

### 6. Request final approval

Report:

- Primary branch and remote.
- Working tree status.
- Synchronization state (ahead/behind counts).
- Active phase/task, if known.
- Proposed or user-supplied branch name and availability.

Ask whether to create the exact branch from the confirmed primary branch. Wait for explicit approval; a generated proposal is not approval. If the user supplies a different name, repeat the name validation and availability checks.

### 7. Create and switch to the approved branch

Immediately before creation, recheck that the active branch is the primary branch, the working tree is clean, the remote primary branch is synchronized (fetch and compare again), and the approved name remains available locally and remotely. If anything changed, return to the relevant check and approval step.

Record the current primary-branch commit with `git rev-parse HEAD`, then execute:

```bash
git checkout -b <approved-branch-name>
```

This creates the branch and switches to it in one operation. Do not issue an unnecessary second checkout. Do not push the new branch.

### 8. Verify and report

```bash
git branch --show-current
git rev-parse HEAD
git status --short --branch
```

Confirm the active branch exactly matches the approved name and its starting commit matches the recorded primary-branch commit. Verify that the working tree is clean.

Report a concise summary:

- Base branch and remote
- New branch name
- Starting commit
- Synchronization and working tree status
- Whether creation and checkout succeeded

Stop here. Do not start implementation or perform any other Git operation automatically.
