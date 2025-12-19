---
title: BDD & Gherkin Specification Instructions
description: Guidelines for writing maintainable, business-focused feature files using EARS and Rules.
applyTo: '**/*.feature'
---

# BDD & Gherkin Specification Instructions

When writing or updating `.feature` files, you must follow these guidelines to ensure specifications are clear, maintainable, and focused on business value.

## Cheat Sheet

| Concept | Pattern/Usage |
| :--- | :--- |
| **EARS Rules** | **Ubiquitous** (The system shall...), **Event** (When...), **State** (While...), **Unwanted** (If...), **Optional** (Where...) |
| **Tags** | `@slow` (skip by default), `@network` (skip by default), `@wip` (local only), `@batch` (shell script) |
| **Structure** | Feature → Background (optional) → Rule → Scenario / Scenario Outline |
| **Filenames** | `kebab-case.feature` (e.g., `link-rewriting.feature`) |
| **Run Tests** | `pytest -m "not slow and not network"` (Fast default) |

---

## 1. Quality Checklists

Before finalizing a feature file, verify it against these checklists.

### Rule Checklist
*   [ ] **Atomic:** Does the Rule describe a single behavior or constraint?
*   [ ] **EARS Format:** Is it written using one of the 5 EARS patterns?
*   [ ] **Coverage:** Are there 2–5 scenarios illustrating this Rule? (Split if >5).
*   [ ] **Negative Cases:** Are error conditions handled in their own "If..." Rules?
*   [ ] **Independence:** Does the Rule stand alone without hidden dependencies?

### Scenario Checklist
*   [ ] **Declarative:** Does it describe *what* happens, not *how* (UI clicks)?
*   [ ] **Single Action:** Is there exactly one `When` step?
*   [ ] **Observable:** Does the `Then` step assert a visible outcome (output, state change)?
*   [ ] **Deterministic:** Are inputs and outputs fixed (no timestamps/randomness)?
*   [ ] **Domain Language:** Does it use terms from the **Glossary** (e.g., "Subscriber" vs "User")?

### Background Checklist
*   [ ] **Minimal:** Does it contain *only* context common to ALL rules?
*   [ ] **Stable:** Is the setup static (e.g., "Given the site configuration is loaded")?
*   [ ] **No Variables:** Does it avoid setting specific data that varies per scenario?

---

## 2. Feature Structure & Naming

*   **Directory:** `tests/features/<area>/<feature>.feature`
*   **Filename:** `kebab-case.feature` (e.g., `content-extraction.feature`)
*   **Formatting:** 2-space indentation, 80–100 char line limit.

```gherkin
Feature: <Short, Active Title>

  <Free text description>
  - Context: Why is this feature needed?
  - Value: What benefit does it provide?
  - Actors: Who is involved?
  - References: Related ADRs or tickets.

  Background:
    Given <context common to all rules>

  Rule: <EARS Statement>
    Scenario: <Concrete Example>
      Given ...
      When ...
      Then ...
```

## 3. The `Rule` Keyword & EARS Syntax

We use the `Rule` keyword to group scenarios. Each Rule **MUST** be written using the **EARS** (Easy Approach to Requirements Syntax) format.

### EARS Patterns
*   **Ubiquitous (Always true):**
    *   `The <system> shall <response>`
    *   *Ex:* `Rule: The system shall log every transaction.`
*   **Event-Driven (When something happens):**
    *   `When <trigger>, the <system> shall <response>`
    *   *Ex:* `Rule: When a user submits a valid form, the system shall create an account.`
*   **State-Driven (While in a specific state):**
    *   `While <state>, the <system> shall <response>`
    *   *Ex:* `Rule: While the site is in maintenance mode, the system shall reject all requests.`
*   **Unwanted Behavior (Error handling):**
    *   `If <trigger>, then the <system> shall <response>`
    *   *Ex:* `Rule: If the payment fails, then the system shall display a retry option.`
*   **Optional Feature (Configuration):**
    *   `Where <feature is present>, the <system> shall <response>`
    *   *Ex:* `Rule: Where the 'verbose' flag is set, the system shall output debug logs.`

## 4. Scenarios & Outlines

### Scenarios (Example Mapping)
Scenarios are **concrete examples** that illustrate the Rule.
*   **Title:** Describe the specific condition or variation.
*   **Style:** Declarative (Business intent), not Imperative (UI clicks).

### Scenario Outlines
Use `Scenario Outline` when the logic is identical but the data varies.
*   **When to use:** Testing boundaries, multiple input formats, or calculation rules.
*   **Template:**
    ```gherkin
    Scenario Outline: <Title>
      Given a file named "<filename>"
      When the file is processed
      Then the output format should be "<format>"

      Examples: Standard Cases
        | filename      | format |
        | image.png     | binary |
        | readme.md     | text   |

      Examples: Boundary Cases
        | filename      | format |
        | .hidden       | ignore |
        | very_long...  | text   |
    ```

## 5. Step Writing & Best Practices

### The "Given-When-Then" Flow
*   **Given (Context):** Setup the state. Use domain language.
    *   *Builders vs Fixtures:*
        *   **Structural Logic:** Use Builders (e.g., `Given a site with pages...`) to generate simple graphs.
        *   **Parsing Logic:** Use Fixtures (e.g., `Given the fixture "article.html"`) for realistic HTML.
*   **When (Action):** **ONE** single action per scenario.
    *   *Bad:* `When I login and click the button` (Two actions).
*   **Then (Outcome):** Assert the result. Avoid side effects.

### Step Definitions (Python/pytest-bdd)
*   **Readable Phrases:** Prefer natural language over complex regex.
*   **Reuse:** Check existing steps before writing new ones.
*   **Side-Effect Free:** Steps should not modify state unless it's the `When` step.

### Anti-Patterns (Avoid these!)
*   **UI Click-fests:** `Given I click "Submit"` → *Better:* `When the form is submitted`.
*   **Multiple Whens:** Indicates a scenario trying to test a workflow sequence rather than a rule. Split it.
*   **Incidental Details:** `Given a user named "Bob" with email "bob@example.com"` (unless email format matters) → *Better:* `Given a registered user`.
*   **Hidden Setup:** Don't hide critical setup in hooks that isn't visible in the Gherkin.

## 6. Tags & Execution Strategy

Use tags to manage test execution speed and reliability.

*   `@slow`: Tests that take >1s or involve heavy IO. (Excluded by default).
*   `@network`: Tests that hit real external URLs. (Excluded by default).
*   `@wip`: Work in progress. Use locally while developing. **Remove before merging.**
*   `@batch`: Tests for the batch processing script.

### Run Tips
*   **Fast (Default):** `pytest -m "not slow and not network"`
*   **Include Slow:** `pytest -m "not network"`
*   **Only WIP:** `pytest -m "wip"`

## 7. Example

```gherkin
Feature: Link Rewriting

  To ensure the aggregated document is navigable offline, we need to convert
  web links into internal references.

  Background:
    Given the site configuration is loaded

  Rule: When a link points to a page included in the aggregation, the system shall rewrite it as an internal anchor.

    Scenario: Link to a sibling page
      Given a page "index.html" with a link to "about.html"
      And "about.html" is part of the aggregation with title "About Us"
      When the content is aggregated
      Then the link in "index.html" should point to the anchor "#about-us"

  Rule: If a link points to an external resource, then the system shall keep it as is.

    Scenario Outline: External links are preserved
      Given a page with a link to "<url>"
      When the content is aggregated
      Then the link should remain "<url>"

      Examples:
        | url                     |
        | https://google.com      |
        | mailto:user@example.com |
```
