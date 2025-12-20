# Webmix

> Convert entire websites into a single, LLM-friendly Markdown file.

Webmix is a Python CLI tool designed to crawl, extract, and aggregate website content. It turns scattered web pages into a structured, clean Markdown document optimized for Large Language Model (LLM) context windows.

Think of it as `repomix` but for websites.

## Why Webmix?

When working with LLMs, you often want to provide documentation or content from a website as context. Copy-pasting page by page is tedious, and raw HTML is noisy. Webmix solves this by:

1.  **Mirroring** a target website to a local directory (via `wget`).
2.  **Discovering** relevant HTML files in the local mirror.
3.  **Extracting** the main content using robust "Reader Mode" logic (powered by `trafilatura`), stripping away navigation, ads, and footers.
4.  **Rewriting Links** to preserve context by converting internal links to explicit textual references (e.g., `[Link](...) (see: Page Title)`).
5.  **Aggregating** everything into a single file with a clear Table of Contents and structure.

## Features

- **Batch Processing**: One-shot command to download and aggregate a site.
- **Smart Discovery**: Automatically finds pages within the local mirror.
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
- `wget` (for the batch script).

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/webmix.git
cd webmix
poetry install
```

## Usage

### Batch Mode (Recommended)

To download and convert a website in one go:

```bash
./webmix.sh <url> [output_file]
```

Example:
```bash
./webmix.sh https://example.com example_site.md
```

### Manual Mode

If you already have a local mirror of a website:

```bash
poetry run webmix <directory_path> --output <output_file>
```

## Development

Webmix uses **Agentic BDD** (Behavior Driven Development) with `pytest-bdd`.

### Running Tests

We use a split testing strategy with a **Local Website Simulator** to ensure fast, deterministic tests without hitting real endpoints.

```bash
# Run default tests (Fast & Offline)
poetry run pytest

# Run ALL tests (Including Slow & Network)
poetry run pytest -o "addopts="

# Run specific feature specs
poetry run pytest tests/features/discovery.feature
```

### Project Structure

- `webmix/`: Source code.
- `tests/`: BDD features and step definitions.
- `tests/data/sample_site/`: Local simulator data (real downloaded site).
- `webmix.sh`: Batch processing script.

## Roadmap

- [x] Project Scaffolding & Simulator Setup
- [x] Feature 1: Discovery & TOC
- [x] Feature 2: Content Extraction
- [x] Feature 3: Link Rewriting
- [x] Feature 4: Aggregation
- [x] Batch Script
- [ ] Alt text for images
- [ ] Breadcrumbs, hierarchical extraction (follow sitemap in ToC)
