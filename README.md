# Webmix

> Convert entire websites into a single, LLM-friendly Markdown file.

Webmix is a Python CLI tool designed to crawl, extract, and aggregate website content. It turns scattered web pages into a structured, clean Markdown document optimized for Large Language Model (LLM) context windows.

Think of it as `repomix` but for websites.

## Why Webmix?

When working with LLMs, you often want to provide documentation or content from a website as context. Copy-pasting page by page is tedious, and raw HTML is noisy. Webmix solves this by:

1.  **Crawling** a target website to discover relevant pages.
2.  **Extracting** the main content using robust "Reader Mode" logic (powered by `trafilatura`), stripping away navigation, ads, and footers.
3.  **Aggregating** everything into a single file with a clear Table of Contents and structure.

## Features

- **Smart Discovery**: Automatically finds pages within the same domain.
- **Clean Extraction**: Converts HTML to noise-free Markdown.
- **Link Rewriting**: Preserves context by converting internal links to explicit textual references.
- **Structured Output**: Generates a `repomix`-style output with:
    - File Summary
    - Directory Structure / Sitemap
    - Concatenated Content

## Getting Started

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management.

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/webmix.git
cd webmix
poetry install
```

## Usage

> [!NOTE]
> Webmix is currently under active development. The CLI commands below are planned.

To convert a website:

```bash
poetry run webmix https://example.com --output example_site.md
```

## Development

Webmix uses **Agentic BDD** (Behavior Driven Development) with `pytest-bdd`.

### Running Tests

We use a split testing strategy with a **Local Website Simulator** to ensure fast, deterministic tests without hitting real endpoints.

```bash
# Run all tests
poetry run pytest

# Run specific feature specs
poetry run pytest tests/features/discovery.feature
```

### Project Structure

- `webmix/`: Source code.
- `tests/`: BDD features and step definitions.
- `tests/data/sample_site/`: Local simulator data (real downloaded site).

## Roadmap

- [x] Project Scaffolding & Simulator Setup
- [ ] Feature 1: Discovery & TOC
- [ ] Feature 2: Content Extraction
- [ ] Feature 3: Link Rewriting
- [ ] Feature 4: Aggregation
