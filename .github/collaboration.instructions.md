# Collaboration Instructions

These instructions define how agents should collaborate and communicate through artifacts (code, specs, docs) to ensure context is preserved for successor agents.

## Core Philosophy: Context Maximization

Your output is the input for the next agent. Always write artifacts in a way that provides the right context to your successor without them needing to re-derive information.

### For Spec Writers (Handing off to Developers)
- **Self-Explanatory Features**: Write features that contain all necessary data.
- **Explicit Data**: Use Examples tables and DocStrings to provide concrete test data. Do not rely on the developer to "invent" valid data.
- **Clear Intent**: The `Feature` description and `Rule` statements should explain *why* this behavior exists, so the developer understands the business goal, not just the mechanics.

### For Developers (Handing off to Reviewers/Maintainers)
- **Storytelling Code**: Write code and tests that tell a story. Prefer explicit variable names and clear control flow over clever one-liners.
- **Why-Comments**: Leave comments explaining *why* a decision was made, not just *what* the code does.
- **Traceability**: Ensure step definitions clearly map back to the feature file steps.
- **Clean History**: Write commit messages that explain the context of the change (using the risk-aware convention).

### General Rules
- **Ubiquitous Language**: Strictly adhere to the terms defined in `GLOSSARY.md`. If you introduce a new concept, add it to the glossary immediately.
- **Explicit Assumptions**: If you make an assumption, document it in the code or the feature file context section.
