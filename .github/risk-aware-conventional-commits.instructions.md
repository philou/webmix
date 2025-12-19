---
description: Guidelines for writing risk-aware commit messages using Arlo's Commit Notation and Conventional Commits.
---
# Risk-Aware + Conventional Commit Messages Instructions

When generating commit messages, you must follow this specific format that combines [**Arlo's Commit Notation**](https://github.com/RefactoringCombos/ArlosCommitNotation) (Risk Assessment) and [**Conventional Commits**](https://www.conventionalcommits.org/).

## Cheat Sheet

| Risk | Meaning | Use Case |
| :--- | :--- | :--- |
| `. ` | **Proven Safe** | Covered by tests, formatting, renaming. |
| `^ ` | **Validated** | Manual verification, config changes. |
| `! ` | **Risky** | No tests, complex logic, dependency upgrades. |
| `@ ` | **WIP/Broken** | Saving state, sharing incomplete work. |

**Format**: `<risk> <type>(<scope>): <summary>`

---

## Format Structure

```text
<risk> <type>(<optional scope>): <summary>

<Why we did the change>
- <detail 1>
- <detail 2>
- ...

<footers>
```

## 1. Risk Assessment (`<risk>`)
The message **MUST** start with one of the following 2-character prefixes.

### Decision Guide
*   `. ` **Proven Safe**
    *   *Criteria:* Automated tests cover this change OR it is structurally safe refactoring.
    *   *Examples:* Renaming a private variable, formatting code, extracting a method (automated), adding a test case.
*   `^ ` **Validated**
    *   *Criteria:* Not fully covered by automated tests, but you have manually verified it works.
    *   *Examples:* UI tweaks, configuration changes, updating documentation, features verified via CLI/REPL.
*   `! ` **Risky**
    *   *Criteria:* Complex logic changes, dependency updates, or refactorings without full test coverage. Potential for regression.
    *   *Examples:* Upgrading a core library, rewriting a core algorithm, changing database schema without migration tests.
*   `@ ` **WIP / Broken**
    *   *Criteria:* Known to be broken or incomplete. Used for saving state or handing over work.
    *   *Examples:* "saving my place", "broken test", "partial implementation".

## 2. Conventional Commit Header (`<type>(<scope>): <summary>`)
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

*   **Types:**
    *   `feat`: A new feature
    *   `fix`: A bug fix
    *   `docs`: Documentation only changes
    *   `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
    *   `refactor`: A code change that neither fixes a bug nor adds a feature
    *   `perf`: A code change that improves performance
    *   `test`: Adding missing tests or correcting existing tests
    *   `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
    *   `ci`: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
    *   `chore`: Other changes that don't modify src or test files
    *   `revert`: Reverts a previous commit

*   **Scope:** (Optional)
    *   Use `kebab-case` or `snake_case`.
    *   Refers to the module, file, or architectural component affected (e.g., `extraction`, `cli`, `tests`, `webmix-sh`).
    *   Omit if the change is global or hard to scope.

*   **Summary:**
    *   Use imperative mood ("add" not "added", "fix" not "fixed").
    *   No period at the end.
    *   Keep the entire header (risk + type + scope + summary) under 72 characters if possible.

## 3. Body (`<Why>`)
*   **Mandatory:** Start with **Why** the change was made. Context is king.
*   Use a bulleted list for details of *what* changed if complex.
*   Separate from header with a blank line.

## 4. Footers
*   **BREAKING CHANGE:** Start the footer with `BREAKING CHANGE: ` followed by a description of what broke and migration instructions.
*   **References:** `Refs: #123`, `Closes: #456`.
*   **Co-authors:** `Co-authored-by: Name <email>`.

## 5. Special Cases
*   **Reverts:** Use `revert: <header of reverted commit>`. In the body, say "This reverts commit <hash>."
*   **WIP:** `@ ` commits should generally be squashed or cleaned up before merging to the main branch.
*   **TODO Updates:** When updating `TODO.md` or similar task lists:
    *   Do **not** list every checked item in the body (e.g., avoid "- Checked item A").
    *   Briefly mention structural changes (e.g., "- Added new tasks for X", "- Reordered steps").

---

## Examples by Type

**Feature (Validated)**
```text
^ feat(cli): add verbose flag to output

To help users debug connection issues.
- Added --verbose option to main command
- Wired up logger configuration
```

**Fix (Risky)**
```text
! fix(parser): handle malformed HTML tags

To prevent crashes on legacy websites.
- Added try/catch block around lxml parser
- Note: This might skip some valid content if nested deeply
```

**Docs (Safe)**
```text
. docs(readme): update installation steps

To reflect the switch to Poetry.
- Replaced pip commands with poetry commands
```

**Style (Safe)**
```text
. style(core): run black formatter

To enforce project style guidelines.
```

**Refactor (Safe)**
```text
. refactor(discovery): extract file walking logic

To improve testability and separate concerns.
- Moved os.walk logic to a dedicated function
- Added type hints
```

**Perf (Validated)**
```text
^ perf(extraction): cache regex compilation

To speed up processing of large pages.
- Moved regex compilation to module level
```

**Test (Safe)**
```text
. test(linking): add case for relative urls

To ensure we handle internal links correctly.
```

**Build (Safe)**
```text
. build(deps): bump trafilatura from 1.4 to 1.5

To get the latest security fixes.
```

**CI (Validated)**
```text
^ ci(github): add python 3.11 to matrix

To verify compatibility with the latest python version.
```

**Chore (Safe)**
```text
. chore: update .gitignore

To ignore local test artifacts.
```

**Revert (Safe)**
```text
. revert: ^ feat(cli): add verbose flag to output

This reverts commit 5f3a1b2.
The verbose flag was causing issues with pipe output.
```

**Breaking Change (Risky)**
```text
! refactor(api): rename fetch_url to get_page

To align with the new naming convention.

BREAKING CHANGE: `fetch_url` is removed. Use `get_page` instead.
```
