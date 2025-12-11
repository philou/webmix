## Plan: Webmix (Agentic BDD Experiment)

We will build a Python CLI tool to crawl, extract (Reader Mode), and aggregate a website into a single Markdown file. We will use **pytest-bdd** for specs and **Trafilatura** for extraction. We will implement a **Fetcher Abstraction** to switch between a real HTTP client and a **Local Website Simulator** for fast, deterministic testing.

**Note on Sanitization:** `trafilatura` handles the heavy lifting of cleaning HTML (Reader Mode), so we don't need to implement complex sanitization logic ourselves.

### Testing Strategy (Split Approach)
*   **For Structural Logic (Discovery, Linking, Aggregation):** Use **Builders**.
    *   *Why:* We care about the graph/links, not the messy HTML content.
    *   *How:* `Given a site with pages: | url | title | content |` (Generates simple HTML on the fly).
*   **For Parsing Logic (Extraction):** Use **Hybrid (Fixtures + Assertions)**.
    *   *Why:* We need realistic, messy HTML (ads, scripts) to test `trafilatura`, but we also need readable tests.
    *   *How:* `Given the fixture "article_with_ads.html"` AND `And the page contains a sidebar with "Subscribe Now"` (Loads real file but asserts its content in the step to prevent drift).

### Steps
- [ ] **1. Project Scaffolding & Test Data**
    - [ ] Initialize Poetry project with `pytest`, `pytest-bdd`, `trafilatura`, `requests`, `typer`.
    - [ ] Create `README.md` and other meta info files.
    - [ ] **Action:** Download a small subset of the target site (or a dummy site) into `tests/data/sample_site` to serve as our "Simulator" data source.

- [ ] **2. Feature 1: Discovery & TOC**
    - [ ] **Spec:** `features/discovery.feature`. Scenario: "Given a website root, discover pages and generate a Table of Contents."
    - [ ] **Sub-step: Core Abstraction (The Fetcher)**
        - [ ] **Goal:** Define a `WebFetcher` protocol (interface) with methods like `get_html(url)` and `get_sitemap(url)`.
        - [ ] **Implementations:**
            - [ ] `HttpFetcher`: The real implementation using `requests`/`trafilatura`.
            - [ ] `LocalFetcher`: The simulator that maps URLs to files in `tests/data/sample_site`.
    - [ ] **Test:** Inject `LocalFetcher`. Verify it finds pages and returns a Markdown list of links to be used as the TOC.
    - [ ] **Refinement:** The output format should mimic `repomix` structure:
        1.  **File Summary** (Purpose, Format, Usage)
        2.  **Directory Structure** (Tree view of the site)
        3.  **Files** (The actual content sections)

- [ ] **3. Feature 2: Content Extraction (Reader Mode)**
    - [ ] **Spec:** `features/extraction.feature`. Scenario: "Given a raw HTML page, return clean Markdown."
    - [ ] **Test:** Use `LocalFetcher` to retrieve a specific HTML file and assert the Markdown output is clean (no nav/ads).

- [ ] **4. Feature 3: Link Rewriting**
    - [ ] **Spec:** `features/linking.feature`. Scenario: "Links between pages are converted to explicit textual references."
    - [ ] **Test:** Verify `[Link](page2.html)` becomes `Link (see: Page 2 Title)` or similar clear text in the final output.

- [ ] **5. Feature 4: Aggregation**
    - [ ] **Spec:** `features/aggregation.feature`.
    - [ ] **Test:** Verify the final output starts with a TOC and contains all sections concatenated.

### Parking
- [ ] **Contract Testing:** We can write a generic test suite `test_fetcher_contract.py` that runs against *both* `HttpFetcher` (checking a known live URL) and `LocalFetcher` to ensure the simulator accurately mimics the real world.
- [ ] **Rate Limiting:** The `HttpFetcher` should implement politeness (delays) which the `LocalFetcher` can ignore.
