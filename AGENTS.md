# AGENTS.md

Guidance for AI coding agents working in this repository.

`CONTRIBUTING.md` is canonical for public contribution workflow, including
issues, assignment, pull requests, refactors, changelogs, validation, commits,
and DCO. `AI_POLICY.md` is canonical for public AI-assisted contribution policy.
This file translates those policies into operational instructions for coding
agents.

## Repository Orientation

- Main package code lives under `nemoguardrails/`.
- Tests live under `tests/`, with additional doctest/example coverage in
  `docs/colang-2/examples` and `benchmark/tests` through `pytest.ini`.
- Public documentation lives under `docs/`; examples and sample
  configurations live under `examples/`.
- The default development branch is `develop`.

## Environment

- Use Poetry for dependency management and command execution.
- Install development dependencies with:

  ```bash
  poetry install --with dev
  ```

- Install documentation dependencies when working on docs:

  ```bash
  poetry install --with dev,docs
  ```

- Run Python tools through Poetry:

  ```bash
  poetry run python ...
  poetry run pytest ...
  ```

- Do not add dependencies to `pyproject.toml` or update `poetry.lock` unless the
  change requires it. For temporary local investigation, prefer the documented
  `poetry run pip install ...` workflow and do not commit those environment-only
  changes.

## Before You Start

- Follow `CONTRIBUTING.md` for public issue, assignment, PR, refactor,
  changelog, validation, commit, and DCO policy.
- Follow `AI_POLICY.md` for public AI-assisted contribution requirements.
- Understand whether the task is ready for implementation. For non-trivial
  features, API changes, any refactor, or behavior changes without clear
  maintainer direction, stop at a proposal or implementation plan unless a
  maintainer has approved and assigned the work.
- Do not submit public contribution objects yourself: no browser automation,
  GitHub API, `gh issue create`, `gh pr create`, or similar tooling for opening
  issues or PRs. You may draft issue text, issue comments, PR descriptions, and
  validation summaries for a human to review and submit.
- Do not open PRs, create GitHub draft PRs, push PR branches, or prepare
  PR-ready work unless the linked issue is triaged and assigned to the human
  contributor who will submit the PR.
- Refactors are maintainer-led. For unapproved refactors, stop at a refactor
  proposal or implementation plan. Implement refactors only when a maintainer
  has approved the plan and assigned the work.
- Check for related issues, PRs, docs, tests, and prior design notes when the
  task is PR-shaped or changes public behavior. Do not submit duplicate work.
- Decline or redirect low-value mechanical work such as isolated formatting,
  typo churn, or broad cleanup unless it is tied to a substantive change.
- If the requested change would remove intentional behavior, narrow public
  compatibility, add a required dependency, or expand live-service usage, stop
  and make the tradeoff explicit before editing.
- Read enough of the relevant files to understand the local design. Search
  snippets are useful for navigation, not a substitute for reading the code that
  will be changed.

## Verification Commands

- Focused tests:

  ```bash
  poetry run pytest path/to/test_file.py
  ```

- Full test suite:

  ```bash
  poetry run pytest
  ```

- Makefile test alias:

  ```bash
  make test TEST_FILE=path/to/test_file.py
  ```

- For PR-ready code changes, pre-commit hooks are the authoritative lint,
  format, license-header, and type checking path:

  ```bash
  poetry run pre-commit run --all-files
  ```

- Treat standalone Ruff, Ruff format, or Pyright runs as local diagnosis only.
  They do not replace pre-commit for PR-ready code changes; if pre-commit is
  skipped, report that explicitly in the handoff.
- See `CONTRIBUTING.md` for broader validation commands such as tox and package
  coverage.
- Use individual tools such as Ruff or Pyright only for targeted diagnosis or
  faster local iteration. Run them through Poetry:

  ```bash
  poetry run ruff check path/to/file.py
  poetry run ruff format path/to/file.py
  poetry run pyright
  ```

- Documentation build:

  ```bash
  poetry run sphinx-build -b html docs _build/docs
  ```

- Do not run broad verification for docs-only or repository-metadata changes
  unless requested. For runtime, test, build, or packaging changes, run the
  smallest meaningful tests first, then broaden to pre-commit and wider tests
  when the change touches shared behavior.

## Pull Requests and Reviews

- Follow `CONTRIBUTING.md` for branch, PR title, assignment, DCO, and commit
  policy.
- Follow `AI_POLICY.md` for disclosure and human accountability requirements.
- Do not open PRs or push branches unless the user explicitly asks and the
  policy preconditions in `CONTRIBUTING.md` are satisfied.
- If work is still exploratory, draft an issue comment describing the branch and
  relevant files instead of opening a PR.
- If an issue is unassigned or the author is not implementing it, help draft a
  concise takeover comment with proposed approach and validation plan. Wait for
  maintainer assignment before preparing PR-ready work.
- Use the Conventional Commit-style titles described in `CONTRIBUTING.md`. PR
  titles become merge commit messages and feed release automation.
- Address all coding-agent review comments before handing work to human
  maintainers. If a review comment is intentionally not addressed, document the
  reason clearly in the handoff.
- Do not prefix PR titles or commit messages with agent markers.
- In final handoffs, report tests/checks run, skipped checks, unresolved risks,
  and any reviewer comments intentionally left unresolved.

## Generated Files

- Follow `CONTRIBUTING.md` for generated changelog policy. Operationally, never
  update `CHANGELOG.md` or `CHANGELOG-Colang.md` manually; put release-note
  context in the issue or PR draft instead.
- Do not hand-edit generated files or lockfiles unless the task explicitly
  requires regenerating them. Use the documented project tooling and keep those
  diffs separate from unrelated changes.

## Security and Secrets

- Follow `AI_POLICY.md` for public AI safety and privacy requirements.
- Do not commit API keys, tokens, credentials, private endpoints, or raw logs
  containing sensitive request or response data.
- Do not commit proprietary prompts or unsanitized provider request/response
  payloads.
- Do not fabricate test results, benchmark results, citations, maintainer
  approvals, or compatibility claims.
- Generated media, large generated assets, and synthetic datasets require clear
  provenance and maintainer alignment before inclusion.
- Prefer mocked, synthetic, or redacted fixtures for provider integrations.
- Keep optional provider integrations optional; do not make a secret-bearing or
  network-backed dependency part of the default test path.

## Working Practices

- Start by reading the relevant code and tests. Prefer `rg` and `rg --files` for
  navigation.
- Keep changes narrowly scoped to the requested behavior. Avoid opportunistic
  refactors, formatting churn, and unrelated cleanup.
- Preserve public APIs unless the task explicitly requires an API change.
  Pay special attention to `RailsConfig`, `LLMRails`, server APIs, Colang
  behavior, and documented configuration formats.
- Maintain backward compatibility for optional integrations. Optional providers,
  frameworks, and extras should not become required core dependencies.
- For maintainer-approved refactors, add or update characterization tests before
  changing behavior when the existing contract is subtle.
- For bug fixes, include a regression test whenever practical.
- For new features, cover the public path and at least one failure or edge case.
- Prefer existing local patterns over new abstractions. Add an abstraction only
  when it removes real duplication or clarifies an existing boundary.
- Avoid broad filesystem walks, import-time side effects, or global state changes
  in runtime paths unless the surrounding code already establishes that pattern.
- Do not add comments unless they clarify non-obvious behavior. Prefer clear
  names and small functions.
- Do not add license headers manually. The pre-commit hooks handle license
  insertion for Python files.

## Public API Compatibility

- Treat public imports, constructor signatures, documented methods, config
  schemas, Colang behavior, server request/response shapes, and examples as
  compatibility-sensitive.
- Before changing public APIs, inspect exports, docs, examples, and tests for
  existing usage. Prefer additive changes and keyword-only optional parameters
  over positional signature changes.
- Keep sync and async API behavior aligned for `LLMRails`, `Guardrails`, and
  related public methods.
- Do not change shipped defaults, config semantics, or return shapes without a
  clear migration reason and focused tests.
- Mark experimental behavior clearly in docs and keep it isolated from stable
  contracts.

## NeMo Guardrails Invariants

- `RailsConfig`, `LLMRails`, `Guardrails`, Colang runtimes, server APIs, and
  documented configuration formats are user-facing surfaces. Preserve behavior
  unless the task explicitly changes it.
- Optional integrations and provider-specific packages must remain optional.
  Do not move integration dependencies into the default install path unless the
  task is specifically about packaging policy.
- Unit tests should not call live LLM/provider services. Use existing mocks,
  fixtures, recorded tests, or provider abstractions.
- Recorded/live tests must keep credentials and provider responses out of the
  repository unless they are sanitized through the established test machinery.
- When touching rails execution, action dispatch, generation, streaming, state,
  tracing, or server behavior, cover both the accepted path and fallback or
  unsupported path.

## Review Expectations

- Treat code review as a search for correctness risks, regressions, missing
  tests, public API drift, and dependency or packaging surprises.
- When reviewing a branch, compare against the merge base with `develop` and
  inspect tests as well as implementation.
- Report findings with file and line references, ordered by severity.
- Be explicit about residual risk when tests cannot be run or when coverage is
  intentionally narrow.

## Testing Guidance

- Run the smallest meaningful test set first, then broaden when the change
  touches shared behavior.
- Use full-suite or broader package tests for changes in shared runtime,
  configuration loading, action dispatch, server behavior, tracing, or public
  APIs.
- Avoid relying on live external services in unit tests. Prefer existing mocks,
  fixtures, recorded tests, or provider abstractions.
- Keep async and sync API behavior aligned when touching async-first code paths.
- For streaming, state, or generation changes, test both the accepted path and
  the unsupported or fallback path.

## Documentation

- Update docs when changing user-visible behavior, public APIs, configuration
  syntax, examples, or installation requirements.
- For notebook documentation, follow `CONTRIBUTING.md`. Do not run
  `build_notebook_docs.py` unless explicitly asked, because it currently runs
  broad git staging and pre-commit commands. Use a clean worktree if it must be
  run.

## Git Hygiene

- Check `git status --short` before editing and before finishing.
- Before any state-changing git command, inspect `git status --short` and limit
  the operation to explicit paths.
- Do not revert or overwrite unrelated local changes.
- Stage explicit paths only. Do not use `git add .` or `git add -A`.
- Do not use broad pathspecs such as `.`, `:`, or repository-root
  restores/checkouts for staging, restoring, or cleanup.
- Do not run destructive cleanup commands such as `git reset --hard`,
  `git clean`, broad checkout/restore commands, or stash operations unless the
  user explicitly asks for that exact operation.
- Do not push branches, open PRs, modify remotes, rebase, merge, force-push, or
  stash unless the user explicitly asks and the contribution-policy
  preconditions are satisfied.
- Resolve conflicts only in files you changed. If a conflict appears in an
  unrelated file, stop and ask for direction.
- Do not commit unless the user asks.
- Keep commits focused and descriptive, using the project commit conventions.
- Public contributions require DCO sign-off or GPG-signed commits, as described
  in `CONTRIBUTING.md`.
