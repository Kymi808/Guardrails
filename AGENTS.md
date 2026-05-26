# AGENTS.md

Guidance for AI coding agents working in this repository.

`CONTRIBUTING.md` is canonical for public contribution workflow: issues,
assignment, pull requests, refactors, changelogs, validation, commits, and DCO.
`AI_POLICY.md` is canonical for public AI-assisted contribution policy. This
file translates those policies into operational instructions for agents.

## Quick Rules

- Use Poetry for Python commands: `poetry run python ...`,
  `poetry run pytest ...`, `poetry run pre-commit ...`.
- Check `git status --short` before editing and before finishing.
- Do not open issues, PRs, or draft PRs through browser automation, the GitHub
  API, `gh`, or similar tooling. Draft text for humans to review and submit.
- Do not push branches, open PRs, create GitHub draft PRs, or prepare PR-ready
  work unless the linked issue is triaged and assigned to the human contributor.
- Do not implement refactors unless a maintainer has approved the plan and
  assigned the work.
- Never edit `CHANGELOG.md` or `CHANGELOG-Colang.md` manually.
- Do not commit secrets, credentials, raw provider payloads, proprietary
  prompts, fabricated results, fabricated approvals, or fabricated citations.
- Do not add generated media, large generated assets, or synthetic datasets
  without clear provenance and maintainer alignment.
- Unit tests must not call live LLM or provider services.
- Do not add license headers manually. Pre-commit handles license insertion.

## Repository Map

- Main package: `nemoguardrails/`
- Tests: `tests/`, plus doctest/example coverage from `docs/colang-2/examples`
  and `benchmark/tests` through `pytest.ini`
- Public docs: `docs/`
- Examples and sample configurations: `examples/`
- Default development branch: `develop`

## Setup

- Install development dependencies:

  ```bash
  poetry install --with dev
  ```

- Install documentation dependencies when working on docs:

  ```bash
  poetry install --with dev,docs
  ```

- Do not add dependencies to `pyproject.toml` or update `poetry.lock` unless the
  task requires it. For temporary local investigation, use:

  ```bash
  poetry run pip install <package-name>
  ```

## Validation

| Task | Command |
| --- | --- |
| Focused tests | `poetry run pytest path/to/test_file.py` |
| Full test suite | `poetry run pytest` |
| Makefile targeted test | `make test TEST_FILE=path/to/test_file.py` |
| Pre-commit hooks | `poetry run pre-commit run --all-files` |
| Docs build | `poetry run sphinx-build -b html docs _build/docs` |
| Ruff diagnosis | `poetry run ruff check path/to/file.py` |
| Ruff formatting diagnosis | `poetry run ruff format path/to/file.py` |
| Pyright diagnosis | `poetry run pyright` |

| Change type | Minimum validation |
| --- | --- |
| Docs or repository metadata only | `poetry run pre-commit run --files <changed files>`; build docs when rendering, links, examples, or docs configuration may be affected |
| Runtime bug fix | Focused regression test plus pre-commit on changed files; broaden when shared behavior is touched |
| Public API, config, or Colang behavior | Focused tests plus related docs/examples; add broader package tests when compatibility risk is meaningful |
| Server, streaming, tracing, actions, or generation | Targeted tests for the changed path and fallback/unsupported path |
| Packaging, dependencies, or lockfiles | Relevant install/package checks plus pre-commit; keep dependency diffs separate from unrelated changes |

- For PR-ready code changes, pre-commit is the authoritative lint, format,
  license-header, and type-checking path.
- Standalone Ruff, Ruff format, and Pyright runs are local diagnosis only. If
  pre-commit is skipped, report that explicitly in the handoff.
- Run the smallest meaningful tests first, then broaden when changes touch
  shared runtime behavior, public APIs, packaging, server behavior, tracing, or
  docs.
- See `CONTRIBUTING.md` for broader validation such as tox and package
  coverage.

## Contribution Workflow

- Follow `CONTRIBUTING.md` for issue, assignment, PR title, refactor, changelog,
  validation, commit, and DCO policy.
- Follow `AI_POLICY.md` for disclosure, human accountability, safety, and
  privacy requirements.
- For non-trivial features, API changes, refactors, or behavior changes without
  clear maintainer direction, stop at a proposal or implementation plan.
- Check related issues, PRs, docs, tests, and design notes before doing
  PR-shaped work. Do not duplicate existing work.
- If work is exploratory, draft an issue comment with the branch and relevant
  files instead of opening a PR.
- If an issue is unassigned or abandoned, draft a concise takeover comment with
  the proposed approach and validation plan. Wait for maintainer assignment
  before preparing PR-ready work.
- Use the Conventional Commit-style titles described in `CONTRIBUTING.md`. PR
  titles become merge commit messages and feed release automation.
- Do not prefix PR titles or commit messages with agent markers.

## Review Readiness

- Follow `CONTRIBUTING.md` for review-readiness policy, including CodeRabbit,
  Greptile, human review comments, and readiness labels.
- Before handoff, address every automated review comment or draft a clear reply
  explaining why no change is needed.
- Do not treat automated review comments as resolved until the tool confirms
  resolution when that workflow is supported.
- Do not resolve human reviewer conversations unless the reviewer who opened
  them explicitly asks.
- Do not request or apply `status: ready for maintainer review` while any review
  comment still needs author action.
- In final handoffs, report checks run, skipped checks, unresolved risks, and
  any review comments intentionally left unresolved.

## Code Changes

- Read the relevant code and tests before editing. Use `rg` and `rg --files` for
  navigation.
- Keep changes narrowly scoped. Avoid opportunistic refactors, formatting churn,
  typo sweeps, and broad cleanup unless tied to a substantive change.
- Preserve public APIs unless the task explicitly changes them. Treat public
  imports, constructor signatures, documented methods, config schemas, server
  request/response shapes, Colang behavior, examples, and shipped defaults as
  compatibility-sensitive.
- Keep sync and async API behavior aligned for `LLMRails`, `Guardrails`, and
  related public methods.
- Keep optional providers, frameworks, extras, and secret-bearing integrations
  optional. Do not move integration dependencies into the default install path
  unless the task is specifically about packaging policy.
- For maintainer-approved refactors, add or update characterization tests before
  changing subtle behavior.
- For bug fixes, include a regression test whenever practical.
- For new features, cover the public path and at least one failure or edge case.
- Prefer existing local patterns over new abstractions. Add an abstraction only
  when it removes real duplication or clarifies an existing boundary.
- Avoid broad filesystem walks, import-time side effects, and global state
  changes in runtime paths unless the surrounding code already establishes that
  pattern.
- Do not add comments unless explicitly requested. Prefer clear names and small
  functions.

## NeMo Guardrails Invariants

- `RailsConfig`, `LLMRails`, `Guardrails`, Colang runtimes, server APIs, and
  documented configuration formats are user-facing surfaces.
- Preserve documented behavior unless the task explicitly changes it.
- Prefer mocked, synthetic, recorded, or redacted fixtures for provider
  integrations.
- Recorded/live tests must keep credentials and provider responses out of the
  repository unless sanitized through established test machinery.
- When touching rails execution, action dispatch, generation, streaming, state,
  tracing, or server behavior, cover both the accepted path and fallback or
  unsupported path.
- Mark experimental behavior clearly in docs and keep it isolated from stable
  contracts.

## Documentation And Generated Files

- Update docs when changing user-visible behavior, public APIs, configuration
  syntax, examples, or installation requirements.
- Do not hand-edit generated files or lockfiles unless the task explicitly
  requires regenerating them with project tooling.
- Put release-note context in issue or PR draft text instead of changelog files.
- For notebook documentation, follow `CONTRIBUTING.md`. Do not run
  `build_notebook_docs.py` unless explicitly asked; it currently runs broad git
  staging and pre-commit commands. Use a clean worktree if it must be run.

## Review Mode

- Treat code review as a search for correctness risks, regressions, missing
  tests, public API drift, and dependency or packaging surprises.
- When reviewing a branch, compare against the merge base with `develop` and
  inspect tests as well as implementation.
- Report findings with file and line references, ordered by severity.
- Be explicit about residual risk when tests cannot be run or when coverage is
  intentionally narrow.

## Git Hygiene

- Stage explicit paths only. Do not use `git add .` or `git add -A`.
- Do not use broad pathspecs such as `.`, `:`, or repository-root
  restores/checkouts for staging, restoring, or cleanup.
- Do not run destructive cleanup commands such as `git reset --hard`,
  `git clean`, broad checkout/restore commands, or stash operations unless the
  user explicitly asks for that exact operation.
- Do not push branches, modify remotes, rebase, merge, force-push, or stash
  unless the user explicitly asks and the contribution-policy preconditions are
  satisfied.
- Do not revert or overwrite unrelated local changes.
- Resolve conflicts only in files you changed. If a conflict appears in an
  unrelated file, stop and ask for direction.
- Do not commit unless the user asks.
- Keep commits focused and descriptive, using the project commit conventions.
- Public contributions require DCO sign-off or GPG-signed commits, as described
  in `CONTRIBUTING.md`.
