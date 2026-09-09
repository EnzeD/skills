---
name: yeet
description: >
  Review finished work with an independent subagent, fix findings, commit, push,
  open or update a GitHub PR, and merge automatically after CI and review pass.
  Use when explicitly invoked for this workflow, not for commit-only, push-only,
  or skill-editing requests.
license: Apache-2.0
---

# Yeet

**Review → fix → commit → push → PR → CI → merge.** Invoking this workflow authorizes
in-scope fixes and publication through merge. Honor narrower instructions such as
“leave the PR open.” Do not bypass hooks, required approvals, or repository rules.

## 1. Establish scope

- Read repository instructions; inspect the branch and intended staged, unstaged,
  and untracked changes. Preserve unrelated work. Use the existing checkout;
  create a branch from the current HEAD if detached or on the default branch.
- Resolve the PR base from the user's instruction, existing PR, or repository
  default. Fetch its remote ref; do not automatically rebase or merge it.
- Require `gh` and authenticated access. On macOS, a sandbox authentication failure
  may hide Keychain access: verify outside the sandbox when permitted before
  suggesting login. Distinguish access restrictions from invalid credentials.

## 2. Get an independent review

Spawn one read-only `code-reviewer` through the available subagent tool, in the same
task with fresh context. Supply the repository instructions, requirements, allowed
paths, base/head SHAs, and uncommitted scope. Ask it to inspect the complete diff
from the merge-base for bugs, regressions, and test gaps, returning actionable
findings with severity, file/line, failure scenario, and evidence—or no findings.

The reviewer must not edit, publish, or delegate. While it works, prepare PR metadata
without modifying reviewed files. The main agent fixes confirmed findings and
explains rejected ones with evidence. Send fixes and later code changes back for
focused review; reuse reviews only for unchanged code. If independent review is
unavailable, report the blocker and do not merge unless the user waives it.

## 3. Commit and publish

- Validate fixes with focused checks. Follow the repository commit workflow,
  including required release notes and normal hooks; avoid duplicating passing
  checks for unchanged inputs. Stage only intended paths and use Conventional
  Commits. Continue without an empty commit if work is already committed.
- Push with tracking: `git push -u origin HEAD`. Diagnose failures; never force-push
  or rewrite history merely to publish.
- Find the branch's open PR and update it, or create a draft against the resolved
  base. Distinguish “no PR” from API failure. Preserve existing PR content and
  review state until the merge phase; do not create duplicates.
- Follow the repository PR template when present. Explain why and what changed,
  using the final diff and useful behavioral evidence. Keep meaningful existing
  content, including images. Pass multiline descriptions via `--body-file`.

## 4. Follow CI

Watch all expected checks for the latest pushed revision, including checks not
marked required. Use bounded polling and brief updates. Missing checks are not
success; respect legitimate path filters. Inspect failed logs and review feedback,
fix in-scope issues, validate, commit, push, and follow the new revision.

Stop with a clear blocker when progress needs user input or external recovery,
or repeated failures yield no new diagnosis. Never weaken tests or gates to pass.
A subagent review does not substitute for required GitHub approval.

## 5. Merge and report

Refresh head/base SHAs, checks, approvals, and mergeability. Require review of the
final diff, resolved findings, and passing expected CI. Reassess changes if either
branch moved. Honor required update/merge-queue rules without admin overrides.

Unless asked to leave it open, mark the PR ready and merge without another
confirmation. Use a merge commit with a Conventional Commit subject, tied to the
verified head:

```sh
gh pr merge "$pr" --merge --match-head-commit "$sha" --subject "$subject"
```

If rules prevent a merge, report the blocker. If queued, wait for confirmation or
report queued status. Verify the actual outcome and return the PR link, merge
commit, review summary, and CI result. Do not delete branches/worktrees or launch
separate release/deployment commands unless requested; do not claim post-merge
checks or deployment have completed.

---
Adapted and condensed from OpenAI's yeet skill, with independent review and
automatic merging added. Distributed under [Apache-2.0](LICENSE.txt).
