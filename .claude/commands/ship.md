Run the full git workflow: commit staged/unstaged changes, push the current branch, and open a PR to master.

**Steps:**

1. Run `git status` and `git diff` to understand what changed.
2. Run `git log --oneline -5` to match the commit style of the repo.
3. Check the current branch with `git branch --show-current`. If it is `master`, create and switch to a new branch with a name derived from the staged/unstaged changes (e.g. `feat/add-price-alert`, `fix/scraper-timeout`). Use a short, kebab-case name that reflects *what* changed.
4. Stage all modified tracked files (`git add` by name — avoid `git add -A` to prevent accidentally staging sensitive files).
5. Write a concise commit message focused on *why*, following the repo's convention. Use a HEREDOC to pass the message.
6. Push the branch to origin with `-u` if not yet tracking a remote.
7. Create a PR to `master` using `gh pr create` with a short title and a markdown body (Summary + Test plan bullets).

**Guardrails:**
- Never skip hooks (`--no-verify`).
- Never force-push.
- If there is nothing to commit, skip straight to push + PR (the branch may already have commits ahead of master).
- Return the PR URL at the end.
